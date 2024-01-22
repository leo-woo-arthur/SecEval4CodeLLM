# This is a Python project used to benchmark the security of different programming languages generated
#   by various LLM models.


import configparser

from eval.java_owasp.eval_java_owasp import eval_llm_by_java_owasp


def read_config(p_cfg_file):
    config = configparser.ConfigParser()
    config.read(p_cfg_file)
    return config


cfg_datasets = [dataset.strip() for dataset in read_config('config.ini').get('General', 'datasets').split(',')]
cfg_llm_strategies = [strategy.strip() for strategy in read_config('config.ini').get('General', 'llm_strategies').split(',')]


if __name__ == '__main__':
    datasets_map_eval = {
        'java_owasp': eval_llm_by_java_owasp
    }
    
    for cur_dataset in cfg_datasets:
        if cur_dataset in datasets_map_eval:
            datasets_map_eval[cur_dataset](cfg_llm_strategies)

