import pandas as pd
from datetime import datetime

from eval.java_owasp.eval_java_owasp_llm_strategy_of_chatgpt40 import LLMStrategy4ChatGpt40
from eval.java_owasp.eval_java_owasp_llm_strategy_of_neb import LLMStrategy4Neb
from eval.java_owasp.eval_java_owasp_model import JavaOwaspAnalyzer
from utils.logger_factory import logger
from utils.utils import fetch_file_content, fetch_xml_content


def gen_file_path_of_test_case(p_num_of_test_case):
    test_case_path = "./datasets/java_owasp/BenchmarkTest"
    file_of_java = f"{test_case_path}{p_num_of_test_case}.java"
    file_of_xml = f"{test_case_path}{p_num_of_test_case}.xml"
    return file_of_java, file_of_xml


def analysis_statistics(p_data_frame):
    tp = (( True  == p_data_frame['AnalyticalExistence'] ) & ( True  == p_data_frame['ExpectedExistence'] )).sum()
    tn = (( False == p_data_frame['AnalyticalExistence'] ) & ( False == p_data_frame['ExpectedExistence'] )).sum()
    fp = (( True  == p_data_frame['AnalyticalExistence'] ) & ( False == p_data_frame['ExpectedExistence'] )).sum()
    fn = (( False == p_data_frame['AnalyticalExistence'] ) & ( True  == p_data_frame['ExpectedExistence'] )).sum()
    
    logger.info(f"Func[analysis_statistics]: True  Positives: {tp}")
    logger.info(f"Func[analysis_statistics]: True  Negatives: {tn}")
    logger.info(f"Func[analysis_statistics]: False Positives: {fp}")
    logger.info(f"Func[analysis_statistics]: False Negatives: {fn}")


def run_batch_test_cases(p_llm_strategy, p_nums_of_test_cases):
    analyzers = []
    for cur_num in p_nums_of_test_cases:
        path_of_java, path_of_xml = gen_file_path_of_test_case(cur_num)
        case_code, case_metadata = fetch_file_content(path_of_java), fetch_xml_content(path_of_xml)
        analyzers.append(JavaOwaspAnalyzer(cur_num, case_code, case_metadata))
    p_llm_strategy.sec_eval_by_llm(analyzers)

    return [cur_analyzer.compare_analytical_with_expected() for cur_analyzer in analyers]


def run_all_test_cases(p_llm_strategy, p_total_of_test_cases):
    df = pd.DataFrame()
    
    # Format the test case number as a 5-digit string (e.g., '00001', '00002', etc.)
    nums_of_test_cases = [f"{cur_num + 1:05d}" for cur_num in range(p_total_of_test_cases)]
    batch_size = 16
    for i in range(0, len(nums_of_test_cases), batch_size):
        nums_of_test_case_to_run = nums_of_test_cases[i : i + batch_size]
        cases_result = run_batch_test_cases(p_llm_strategy, nums_of_test_case_to_run)
        df = df.append(cases_result, ignore_index=True)
    
    output_file_name = f"benchmark_results[{p_llm_strategy.name}]-temperature[default]-datetime[{datetime.now()}].csv"
    df.to_csv(output_file_name, index=False)
    
    analysis_statistics(df)
    

def eval_llm_by_java_owasp(p_llm_strategies):
    total_of_test_cases = 2740  # Total: 2740
    
    llm_strategies_map_call = {
        'chatgpt_40': LLMStrategy4ChatGpt40(),
        'neb': LLMStrategy4Neb(),
        # Add strategies for more types of LLMs
    }
    
    for cur_strategy in p_llm_strategies:
        if cur_strategy in llm_strategies_map_call:
            run_all_test_cases(llm_strategies_map_call[cur_strategy], total_of_test_cases)



