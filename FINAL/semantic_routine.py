class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []

    def add_var (self, input):
        print input
