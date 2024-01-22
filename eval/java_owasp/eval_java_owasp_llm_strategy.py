

analysis_answer_default = \
    '''
    {
        "Vulnerability Existence": "No",
        "Vulnerability Type": "None",
        "Comment": "No issues found"
    }
    '''


class LLMStrategy:
    def __init__(self, p_name="BaseLLM"):
        self.name = p_name
        
    def sec_eval_by_llm(self, p_analyzers):
        pass



