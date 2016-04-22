class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []
        self._temp = 0

    def add_primary (self, var_in):
        self._temp += 1
        if var_in[0].isdigit():
            if "." in var_in:
                instr = "STOREF " + var_in + " $T" + str(self._temp) + "\n"
                return instr
            else:
                instr = "STOREI " + var_in + " $T" + str(self._temp) + "\n"
                return instr
        else:
            #print(var_in)
            return(var_in)

    def add_assign_expr(self, var_name):
        instr = "STOREI "  + " $T" + str(self._temp) + " " + var_name
        return instr

    def add_expr(self, l_side, r_side):
        instr = ""
        if len(l_side) > 1 and len(r_side) > 1:
            instr = "ADDI " + " $T" + str(self._temp-1) + " $T" + str(self._temp) + " $T" + str(self._temp+1)
            self._temp +=1
        elif(len(l_side) > 1 and len(r_side) <= 1):
            instr = "ADDI " + " $T" + str(self._temp-1) + " $T" + str(self._temp) + " $T" + str(self._temp+1)
            self._temp +=1
        elif(len(l_side) == 1 and len(r_side) == 1):
            instr = "ADDI " + l_side + " " + r_side +  " $T" + str(self._temp+1)
            self._temp += 1

        return instr
