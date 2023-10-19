from pandas import DataFrame
from pycanon import anonymity, report
from .basic_checker import BasicChecker


class PyCanonChecker(BasicChecker):
    def __init__(
        self,
        qi: list,
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
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
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

    def check_k_anonymity(self, df: DataFrame):
        # Perform k-anonymity check on the DataFrame
        k = anonymity.k_anonymity(df, self.qi)
        if k < self.k_threshold:
            return (False, k, 'K-anonymity check has failed.  Either lower your k threshold or employ techniques to further anonymize this dataset if possible.')
        else:
            return (True, k, 'Success')

    def check_alpha_k_anonymity(self, df: DataFrame):
        alpha_k = anonymity.alpha_k_anonymity(df, self.qi, self.sa)
        if not alpha_k:
            return (False, 0, '(alpha, k)-anonymity check has failed.')
        else if self.k_threshold < alpha_k:
            return (False, alpha_k, f'(alpha, k)-anonymity check has failed.  Either lower your k threshold or employ techniques to further anonymize this dataset if possible. (alpha, k)-anonymity value: {alpha_k}')
        else:
            return (True, alpha_k, 'Success')

    def check_l_diversity(self, df: DataFrame):
        l_div = anonymity.l_diversity(df, self.qi, self.sa)
        if not l_div:
            return (False, 0, 'l-diversity check has failed.')
        else if self.l_threshold < l_div:
            return (False, l_div, f'l-diversity check has failed.  Either lower your l threshold or employ techniques to further anonymize this dataset if possible. l-diversity value: {l_div}')
        else:
            return (True, l_div, 'Success')

    def check_entropy_l_diversity(self, df: DataFrame):
        entropy_l_div = anonymity.entropy_l_diversity(df, self.qi, self.sa)
        if not entropy_l_div:
            return (False, 0, 'entropy l-diversity check has failed.')
        elif self.entropy_l_threshold < entropy_l_div:
            return (False, entropy_l_div, f'entropy l-diversity check has failed. Either lower your l threshold or employ techniques to further anonymize this dataset if possible. entropy l-diversity value: {entropy_l_div}')
        else:
            return (True, entropy_l_div, 'Success')

    def check_c_l_diversity(self, df: DataFrame):
        c_l_div = anonymity.recursive_c_l_diversity(df, self.qi, self.sa)
        if not c_l_div:
            return (False, 0, '(c, l)-diversity check has failed.')
        elif self.c_threshold < c_l_div:
            return (False, c_l_div, f'(c, l)-diversity check has failed. Either lower your l threshold or employ techniques to further anonymize this dataset if possible. (c, l)-diversity value: {c_l_div}')
        else:
            return (True, c_l_div, 'Success')

    def check_basic_beta_likeness(self, df: DataFrame):
        beta_likeness = anonymity.basic_beta_likeness(df, self.qi, self.sa)
        if not beta_likeness:
            return (False, 0, 'basic beta-likeness check has failed.')
        elif self.beta_threshold < beta_likeness:
            return (False, beta_likeness, f'basic beta-likeness check has failed. Either lower your beta threshold or employ techniques to further anonymize this dataset if possible. basic beta-likeness value: {beta_likeness}')
        else:
            return (True, beta_likeness, 'Success')

    def check_enhanced_beta_likeness(self, df: DataFrame):
        enhanced_beta_likeness = anonymity.enhanced_beta_likeness(df, self.qi, self.sa)
        if not enhanced_beta_likeness:
            return (False, 0, 'enhanced beta-likeness check has failed.')
        elif self.enhanced_beta_threshold < enhanced_beta_likeness:
            return (False, enhanced_beta_likeness, f'enhanced beta-likeness check has failed. Either lower your beta threshold or employ techniques to further anonymize this dataset if possible. enhanced beta-likeness value: {enhanced_beta_likeness}')
        else:
            return (True, enhanced_beta_likeness, 'Success')

    def check_t_closeness(self, df: DataFrame):
        t_closeness = anonymity.t_closeness(df, self.qi, self.sa)
        if not t_closeness:
            return (False, 0, 't-closeness check has failed.')
        elif self.t_threshold < t_closeness:
            return (False, t_closeness, f't-closeness check has failed. Either lower your t threshold or employ techniques to further anonymize this dataset if possible. t-closeness value: {t_closeness}')
        else:
            return (True, t_closeness, 'Success')

    def check_delta_disclosure_privacy(self, df: DataFrame):
        delta_disclosure_privacy = anonymity.delta_disclosure(df, self.qi, self.sa)
        if not delta_disclosure_privacy:
            return (False, 0, 'delta-disclosure privacy check has failed.')
        elif self.delta_threshold < delta_disclosure_privacy:
            return (False, delta_disclosure_privacy, f'delta-disclosure privacy check has failed. Either lower your delta threshold or employ techniques to further anonymize this dataset if possible. delta-disclosure privacy value: {delta_disclosure_privacy}')
        else:
            return (True, delta_disclosure_privacy, 'Success')

    def check_dataset(self, df: DataFrame):
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

        results = []
        for test_func, test_name in tests:
            try:
                results += test_func(df) + (test_name,)
                # If the test function doesn't explicitly return True, consider it a failure.
                # if result[0] is not True:
                #     print(
                #         f"{test_name} check failed, {test_name} value: {result[1]}")
                # else:
                #     print(
                #         f"{test_name} check passed, {test_name} value: {result[1]}")

            except Exception as e:
                return f"{test_name} check failed with error: {str(e)}"

        return results
