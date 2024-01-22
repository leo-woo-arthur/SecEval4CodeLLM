import json

from eval.java_owasp.eval_java_owasp_llm_strategy import LLMStrategy, analysis_answer_default
from provider.llm.llm_of_chatgpt40 import call_chatgpt40_api
from utils.logger_factory import logger


class LLMStrategy4ChatGpt40(LLMStrategy):
    def __init__(self, p_name="ChatGpt40"):
        self.name = p_name
        self.default_answer_json = json.loads(analysis_answer_default, strict=False)
        self.func_desc = [
            {
                "name": "find_security_issues_and_generate_fix",
                "description": "Scan the code and find any security vulnerabilities and generate code fix",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Vulnerability Existence": {
                            "type": "string",
                            "description": " 'Yes' if there is a security vulnerability in code or 'No' if the code doesn't have security vulnerability",
                        },
                        "Vulnerability Type": {
                            "type": "string",
                            "description": "The type of vulnerability found in the code or 'None' ",
                        },
                        "Vulnerable Code": {
                            "type": "string",
                            "description": "The code that is vulnerable to the security issue or 'None' ",
                        },
                        "Fixed Code": {
                            "type": "string",
                            "description": "Code fix for the vulnerable code or 'None' ",
                        },
                        "Comment": {
                            "type": "string",
                            "description": "Comment that describes the issue and fix or 'No issues found' ",
                        },
                    },
                    "required": ["Vulnerability Existence", "Vulnerability Type", "Vulnerable Code", "Fixed Code", "Comment"],
                },
            }
        ]


    @staticmethod
    def _gen_prompt(p_code):
        return p_code

    @staticmethod
    def _gen_answer(p_analyzer, p_raw_answer):
        analytical_existence = p_raw_answer['Vulnerability Existence'].lower()
        analytical_type = p_raw_answer['Vulnerability Type'].lower()
        analytical_comment = p_raw_answer['Comment'].lower()
        
        p_analyzer.gen_analytical(analytical_existence, analytical_type, analytical_comment)

    def sec_eval_by_llm(self, p_analyzers):
        logger.debug(f"Func[sec_eval_by_llm]: call api of [{self.name}]")
        ret_resp = self.default_answer_json
        for cur_analyzer in p_analyzers:
            raw_resp = call_chatgpt40_api(self.func_desc, self._gen_prompt(cur_analyzer.case_code))
            try:
                ret_resp = json.loads(raw_resp.additional_kwargs['function_call']['arguments'], strict=False)
            except Exception as e:
                logger.error(f"Func[sec_eval_by_llm]: Error in json.loads: {raw_resp}\n    except: {e}")
            self._gen_answer(cur_analyzer, ret_resp)



