from fuzzywuzzy import fuzz
from utils.logger_factory import logger


class JavaOwaspAnalyzer:
    def __init__(self, p_case_num, p_case_code, p_case_metadata):
        self.case_num = p_case_num
        self.case_code = p_case_code
        self.case_metadata = p_case_metadata
        
        self.analytical_existence = 'no'
        self.analytical_type = 'none'
        self.analytical_comment = 'no issues found'
        
        self.expected_existence = 'no'
        self.expected_type = 'none'
        
        
    def gen_analytical(self, p_analytical_existence, p_analytical_type, p_analytical_comment):
        self.analytical_existence = p_analytical_existence.lower() if 0 != len(p_analytical_existence) else 'no'
        self.analytical_type = p_analytical_type.lower() if 0 != len(p_analytical_type) else 'none'
        self.analytical_comment = p_analytical_comment.lower() if 0 != len(p_analytical_comment) else 'no issues found'
    
    
    def gen_expected(self):
        self.expected_existence = self.case_metadata.find('vulnerability').text.lower()
        self.expected_type = self.case_metadata.find('category').text.lower()


    def is_vulnerability_analytical_existence(self):
        return 'yes' == self.analytical_existence


    def is_vulnerability_expected_existence(self):
        return 'true' == self.expected_existence


    def is_type_match(self):
        return 80 < fuzz.partial_ratio(self.expected_type, self.analytical_type)


    def compare_analytical_with_expected(self):
        self.gen_expected()
        
        ret_comparison = {
            'No.': self.case_num,
            'AnalyticalExistence': self.is_vulnerability_analytical_existence(),
            'ExpectedExistence': self.is_vulnerability_expected_existence(),
            'AnalyticalType': self.analytical_type,
            'ExpectedType': self.expected_type,
            'TypeMatches': self.is_type_match(),
            'AnalyticalComment': self.analytical_comment
        
        }
        logger.debug(f"Func[compare_analytical_with_expected]: case_num[{self.case_num}], ret_comparison: {ret_comparison}")
        return ret_comparison



