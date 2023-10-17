class BasicBetaLikenessChecker(BasicChecker(title='Basic Beta-Likeness')):
    def __init__(
        self,
        qi: list,
        sa: list = [],
        beta_threshold: float = None,
    ):
        if not isinstance(qi, list):
            raise TypeError("qi must be a list.")
        if not isinstance(sa, list):
            raise TypeError("sa must be a list.")

        # Assign values to instance variables
        self.qi = qi
        self.sa = sa
        self.beta_threshold = beta_threshold

    def check_dataset(self, df: DataFrame):
        beta_likeness = anonymity.basic_beta_likeness(df, self.qi, self.sa)
        if not beta_likeness:
            return {
                'message': 'Basic Beta-Likeness check has failed.',
                'title': 'Basic Beta-Likeness control',
                'status': False,
                'value': 0,
                'threshold': None
            }
        elif self.beta_threshold < beta_likeness:
            return {
                'message': 'Basic Beta-Likeness check has failed. Either lower your beta threshold or employ techniques to further anonymize this dataset if possible. Basic Beta-Likeness value: {beta_likeness}',
                'title': 'Basic Beta-Likeness control',
                'status': False,
                'value': beta_likeness,
                'threshold': self.beta_threshold
            }
        else:
            return {
                'message': 'Basic Beta-Likeness check has passed.',
                'title': 'Basic Beta-Likeness control',
                'status': True,
                'value': beta_likeness,
                'threshold': self.beta_threshold
            }