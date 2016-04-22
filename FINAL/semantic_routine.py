class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []
        self._temp = 1

    def add_primary (self, var_in):
        if var_in[0].isdigit():
            if "." in var_in:
                instr = "STOREF" + var_in + " $T" + str(self._temp)
                print (instr)
                self._temp += 1
                return instr
            else:
                instr = "STOREI" + var_in + " $T" + str(self._temp)
                print (instr)
                self._temp += 1
                return instr
        else:
            print(var_in)
            return("IDENTIFIER")
