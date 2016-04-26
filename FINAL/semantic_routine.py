class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []
        self._r_num = 0

    def add_primary (self, var_in):
        if var_in[0].isdigit():
            self._r_num += 1
            if "." in var_in:
                instr = [["STOREF ", var_in + self._r_num]]
                return instr
            else:
                instr = [["STOREF ", var_in , self._r_num]]
                return instr
        else:
            #print(var_in)
            return([[var_in]])

    def add_assign_expr(self, var_name):
        instr = ["STOREI " , self._r_num, var_name]
        return instr

    def add_mul_op(self, l_side, r_side):
        """This method is used in p_assign_expr, p_expr_prefix, p_factor, and
            p_factor_prefix. This correctly builds add and mul commands
            """
        self._r_num += 1
        if l_side[-1] == '+':
            ret = self.make_op(l_side, r_side)
            instr = [["ADDI ", ret[1], ret[2], self._r_num]]
            return ret[0] + instr
        elif l_side[-1] == '-':
            ret = self.make_op(l_side, r_side)
            instr = [["SUBI ", ret[1], ret[2], self._r_num]]
            return ret[0] + instr

        elif l_side[-1] == '*':
            ret = self.make_op(l_side, r_side)
            instr = [["MULI ", ret[1], ret[2], self._r_num]]
            return ret[0] + instr

        elif l_side[-1] == '/':
            ret = self.make_op(l_side, r_side)
            instr = [["DIVI ", ret[1], ret[2], self._r_num]]
            return ret[0] + instr

    def make_op(self, l_side, r_side):
        l_reg = 0
        r_reg = 0

        if len(l_side[-2]) > 1:
            l_reg = l_side[-2][-1]
            del l_side[-1]
        else:
            l_reg = l_side[-2]
            del l_side[-1]
            del l_side[-1]

        if len(r_side[-1]) > 1:
            r_reg = r_side[-1][-1]
            l_side = l_side + r_side
        else:
            r_reg = r_side[-1]

        return (l_side, l_reg, r_reg)


        return instr
