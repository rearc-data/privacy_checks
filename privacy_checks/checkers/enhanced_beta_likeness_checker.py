class EnhancedBetaLikenessChecker(BasicChecker(title='Enhanced Beta-Likeness')):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        enhanced_beta_threshold: float = None,
    ):
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.enhanced_beta_threshold = enhanced_beta_threshold

    def check_dataset(self, df: DataFrame):
        enhanced_beta_likeness = anonymity.enhanced_beta_likeness(df, self.qi, self.sa)
        if not enhanced_beta_likeness:
            return {
                'message': 'Enhanced Beta-Likeness check has failed.',
                'title': 'Enhanced Beta-Likeness control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.enhanced_beta_threshold < enhanced_beta_likeness:
            return {
                'message': 'Enhanced Beta-Likeness check has failed. Either lower your enhanced beta threshold or employ techniques to further anonymize this dataset if possible. Enhanced Beta-Likeness value: {enhanced_beta_likeness}',
                'title': 'Enhanced Beta-Likeness control',
                'status': False,
                'value': enhanced_beta_likeness,
                'threshold': self.enhanced_beta_threshold
            }
        else:
            return {
                'message': 'Enhanced Beta-Likeness check has passed.',
                'title': 'Enhanced Beta-Likeness control',
                'status': True,
                'value': enhanced_beta_likeness,
                'threshold': self.enhanced_beta_threshold
            }