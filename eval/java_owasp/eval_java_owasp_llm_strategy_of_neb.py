import json
import asyncio
import re
import time

from eval.java_owasp.eval_java_owasp_llm_strategy import LLMStrategy, analysis_answer_default
from provider.llm.llm_of_neb import call_neb_apis
from utils.logger_factory import logger


class LLMStrategy4Neb(LLMStrategy):
    def __init__(self, p_name="Neb"):
        self.name = p_name
        self.default_answer_json = json.loads(analysis_answer_default, strict=False)


    @staticmethod
    def _gen_prompt(p_code):
        instruction = "Please scan the code and find any security vulnerabilities, answer according to the following JSON format template:"
        output_file_template = {
            "Vulnerability Existence": " 'Yes' if there is a security vulnerability in code or 'No' if the code doesn't have security vulnerability",
            "Vulnerability Type": "The type of vulnerability found in the code or 'None' ",
            "Comment": "Comment that describes the issue and fix or 'No issues found' ",
        }
        return f"{p_code} {instruction} {output_file_template}"

    
    def _gen_json_from_answer(self, p_raw_answer):
        ret_answer_json = self.default_answer_json
        
        key_str = "```json"
        idx_start = p_raw_answer.find(key_str)
        idx_end = p_raw_answer.find("```", idx_start + len(key_str))
        if -1 != idx_start and -1 != idx_end:
            json_text = p_raw_answer[idx_start + len(key_str) : idx_end - 1]
            try:
                ret_answer_json = json.loads(json_text, strict=False)
            except Exception as e:
                logger.error(f"Func[_gen_json_from_answer]: Error in json.loads: {json_text}\n    except: {e}")
        else:
            logger.error(f"Func[_gen_json_from_answer]: Cannot find json in: {p_raw_answer}")
        
        return ret_answer_json


    def _gen_analytical_from_answer(self, p_analyzer, p_raw_answer):
        # p_str_or_list = "Path Traversal" OR ["SQL Injection", "Cross-site Scripting (XSS)"]
        def transfer_to_str(p_str_or_list):
            ret_str = p_str_or_list
            if isinstance(p_str_or_list, list):
                ret_str = ", ".join(p_str_or_list)
            return str(ret_str)

        
        def gen_value_from_answer(p_answer):
            value_existence, value_type, value_comment = '', '', ''
            pattern_existence, pattern_type, pattern_comment = r'.*Existence.*', r'.*Type.*', r'.*Comment.*'
            
            for cur_key in p_answer.keys():
                if re.search(pattern_existence, cur_key):
                    value_existence = transfer_to_str(p_answer[cur_key]).lower()
                if re.search(pattern_type, cur_key):
                    value_type = transfer_to_str(p_answer[cur_key]).lower()
                if re.search(pattern_comment, cur_key):
                    value_comment = transfer_to_str(p_answer[cur_key]).lower()
            return [value_existence, value_type, value_comment]
        
        
        logger.debug(f"Func[_gen_analytical_from_answer]: case_num[{p_analyzer.case_num}], raw_answer: {p_raw_answer}")
        answer_json = self._gen_json_from_answer(p_raw_answer)
        
        ret_existence, ret_type, ret_comment = '', '', ''
        if isinstance(answer_json, dict):
            [ret_existence, ret_type, ret_comment] = gen_value_from_answer(answer_json)
        elif isinstance(answer_json, list):
            if len(answer_json) > 0:
                for cur_answer in answer_json:
                    [tmp_existence, tmp_type, tmp_comment] = gen_value_from_answer(cur_answer)
                    ret_type += tmp_type
                    ret_comment += tmp_comment
            else:
                logger.error(f"Func[_gen_analytical_from_answer]: 0 == len(answer_json): {answer_json}")
        else:
            logger.error(f"Func[_gen_analytical_from_answer]: error type: {answer_json}")

        p_analyzer.gen_analytical(ret_existence, ret_type, ret_comment)


    def sec_eval_by_llm(self, p_analyzers):
        analyzers_to_process = p_analyzers
        
        retries, max_retries, retry_interval = 0, 3, 60
        while retries < max_retries:
            logger.debug(f"Func[sec_eval_by_llm]: retries[{retries}] total_of_analyzers_to_process: [{len(analyzers_to_process)}] call api of [{self.name}]")
            
            raw_answers = asyncio.get_event_loop().run_until_complete(call_neb_apis(analyzers_to_process, self._gen_prompt))
            raw_answers_dict = {}
            for [cur_num_of_case, cur_raw_answer] in raw_answers:
                raw_answers_dict[cur_num_of_case] = cur_raw_answer
            
            for cur_analyzer in analyzers_to_process:
                self._gen_analytical_from_answer(cur_analyzer, raw_answers_dict[cur_analyzer.case_num])
        
            analyzers_to_process = [cur_analyzer for cur_analyzer in analyzers_to_process if False == cur_analyzer.is_vulnerability_analytical_existence()]
            retries += 1
            time.sleep(retry_interval)



