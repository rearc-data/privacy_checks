import pandas as pd
from pycanon import anonymity, report

class Checker:
    def __init__(
        self,
        qi: list,
        df: pd.DataFrame,
        sa: list = [],
        k_threshold: int = None,
        alpha_threshold: float = None,
        l_threshold: int = None,
        entropy_l_threshold: int = None,
        c_threshold: float = None,
        beta_threshold: float = None,
        enhanced_beta_threshold: float = None,
        t_threshold: float = None,
        delta_threshold: float = None
    ):
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")
        
        # Assign values to instance variables
        self.qi = qi
        self.df = df
        self.sa = sa
        self.k_threshold = k_threshold
        self.alpha_threshold = alpha_threshold
        self.l_threshold = l_threshold
        self.entropy_l_threshold = entropy_l_threshold
        self.c_threshold = c_threshold
        self.beta_threshold = beta_threshold
        self.enhanced_beta_threshold = enhanced_beta_threshold
        self.t_threshold = t_threshold
        self.delta_threshold = delta_threshold

    def check_k_anonymity(self):
        # Perform k-anonymity check on the DataFrame
        k = anonymity.k_anonymity(self.df, self.qi)
        if k < self.k_threshold:
            raise Exception('K-anonymity check has failed.  Either lower your k threshold or employ techniques to further anonymize this dataset if possible.')
        else:
            return (True, k)
    def check_alpha_k_anonymity(self):
        alpha_k = anonymity.alpha_k_anonymity(self.df, self.qi, self.sa)
        if not alpha_k:
            raise Exception('(alpha, k)-anonymity check has failed.')
        else if self.k_threshold < alpha_k:
            raise Exception(f'(alpha, k)-anonymity check has failed.  Either lower your k threshold or employ techniques to further anonymize this dataset if possible. (alpha, k)-anonymity value: {alpha_k}')
        else:
            return (True, alpha_k)

    def check_l_diversity(self):
        l_div = anonymity.l_diversity(self.df, self.qi, self.sa)
        if not l_div:
            raise Exception('l-diversity check has failed.')
        else if self.l_threshold < l_div:
            raise Exception(f'l-diversity check has failed.  Either lower your l threshold or employ techniques to further anonymize this dataset if possible. l-diversity value: {l_div}')
        else:
            return (True, l_div)

    def check_entropy_l_diversity(self):
        entropy_l_div = anonymity.entropy_l_diversity(self.df, self.qi, self.sa)
        if not entropy_l_div:
            raise Exception('entropy l-diversity check has failed.')
        else if self.entropy_l_threshold < entropy_l_div:
            raise Exception(f'entropy l-diversity check has failed.  Either lower your l threshold or employ techniques to further anonymize this dataset if possible. entropy l-diversity value: {entropy_l_div}')
        else:
            return (True, entropy_l_div)

    def check_c_l_diversity(self):
        c_l_div = anonymity.recursive_c_l_diversity(self.df, self.qi, self.sa)
        if not c_l_div:
            raise Exception('(c, l)-diversity check has failed.')
        else if self.c_threshold < c_l_div:
            raise Exception(f'(c, l)-diversity check has failed.  Either lower your l threshold or employ techniques to further anonymize this dataset if possible. (c, l)-diversity value: {c_l_div}')
        else:
            return (True, c_l_div)

    def check_basic_beta_likeness(self):
        beta_likeness = anonymity.basic_beta_likeness(self.df, self.qi, self.sa)
        if not beta_likeness:
            raise Exception('basic beta-likeness check has failed.')
        else if self.beta_threshold < beta_likeness:
            raise Exception(f'basic beta-likeness check has failed.  Either lower your beta threshold or employ techniques to further anonymize this dataset if possible. basic beta-likeness value: {beta_likeness}')
        else:
            return (True, beta_likeness)

    def check_enhanced_beta_likeness(self):
        enhanced_beta_likeness = anonymity.enhanced_beta_likeness(self.df, self.qi, self.sa)
        if not enhanced_beta_likeness:
            raise Exception('enhanced beta-likeness check has failed.')
        else if self.enhanced_beta_threshold < enhanced_beta_likeness:
            raise Exception(f'enhanced beta-likeness check has failed.  Either lower your beta threshold or employ techniques to further anonymize this dataset if possible. enhanced beta-likeness value: {enhanced_beta_likeness}')
        else:
            return (True, enhanced_beta_likeness)

    def check_t_closeness(self):
        t_closeness = anonymity.t_closeness(self.df, self.qi, self.sa)
        if not t_closeness:
            raise Exception('t-closeness check has failed.')
        else if self.t_threshold < t_closeness:
            raise Exception(f't-closeness check has failed.  Either lower your t threshold or employ techniques to further anonymize this dataset if possible. t-closeness value: {t_closeness}')
        else:
            return (True, t_closeness)

    def check_delta_disclosure_privacy(self):
        delta_disclosure_privacy = anonymity.delta_disclosure(self.df, self.qi, self.sa)
        if not delta_disclosure_privacy:
            raise Exception('delta-disclosure privacy check has failed.')
        else if self.delta_threshold < delta_disclosure_privacy:
            raise Exception(f'delta-disclosure privacy check has failed.  Either lower your delta threshold or employ techniques to further anonymize this dataset if possible. delta-disclosure privacy value: {delta_disclosure_privacy}')
        else:
            return (True, delta_disclosure_privacy)

    def run_tests_generate_report(self):
        tests = [
            (self.check_k_anonymity, 'K-anonymity'),
            (self.check_alpha_k_anonymity, '(alpha, k)-anonymity'),
            (self.check_l_diversity, 'l-diversity'),
            (self.check_entropy_l_diversity, 'entropy l-diversity'),
            (self.check_c_l_diversity, '(c, l)-diversity'),
            (self.check_basic_beta_likeness, 'basic beta-likeness'),
            (self.check_enhanced_beta_likeness, 'enhanced beta-likeness'),
            (self.check_t_closeness, 't-closeness'),
            (self.check_delta_disclosure_privacy, 'delta-disclosure privacy')
        ]
        
        for test_func, test_name in tests:
            try:
                result = test_func()
                if result[0] is not True:  # If the test function doesn't explicitly return True, consider it a failure.
                    print(f"{test_name} check failed, {test_name} value: {result[1]}")
                else: 
                    print(f"{test_name} check passed, {test_name} value: {result[1]}")
            except Exception as e:
                return f"{test_name} check failed with error: {str(e)}"
        
        return "All tests passed successfully."