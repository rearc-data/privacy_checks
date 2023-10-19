from pandas import DataFrame

class BasicChecker:

  def __init__(self, title) -> None:
    self.title = title
    pass


  def check_dataset(self, df: DataFrame) -> bool:
    return False

    # TODO: What does a response look like for a checker?
    # {
    #   message: str,
    #   title: str <k-anonmity control>,
    #   status: bool,
    #   value: float,
    #   threshold: float
    # }