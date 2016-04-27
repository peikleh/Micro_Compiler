class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []
        self._r_num = 0
        self._label = 0
        self._type_list = ["ADDI ", "SUBI ", "MULI ", "DIVI ", "STOREI " ]

    def add_primary (self, var_in):
        if var_in[0].isdigit():
            self._r_num += 1
            if "." in var_in:
                instr = [["STOREI ", var_in , self._r_num]]
                return instr
            else:
                instr = [["STOREI ", var_in , self._r_num]]
                return instr
        else:
            #print(var_in)
            return([[var_in]])

    def add_assign_expr(self, expr, var_name):
        instr = [["STOREI " , expr[-1][-1], var_name]]
        if len(expr[-1]) < 2:
            del expr[-1]
        instr = expr + instr

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
            l_reg = l_side[-2][0]
            del l_side[-1]
            del l_side[-1]

        if len(r_side[-1]) > 1:
            r_reg = r_side[-1][-1]
            l_side = l_side + r_side
        else:
            r_reg = r_side[-1][0]

        return (l_side, l_reg, r_reg)

    def add_cond(self, l_side, compop, r_side):
        get_reg = self.make_op(l_side + [compop], r_side)
        l_reg = get_reg[1]
        r_reg = get_reg[2]
        self._label += 1
        instr = ''

        if compop == '<':
            instr = [["JGE ", l_reg, r_reg, self._label]]

        elif compop == '>':
            instr = [["JLE", l_reg, r_reg, self._label]]

        elif compop == '=':
            instr = [["JNE ", l_reg, r_reg, self._label]]

        elif compop == '!=':
            instr = [["JEQ", l_reg, r_reg, self._label]]

        elif compop == '<=':
            instr = [["JGT ", l_reg, r_reg, self._label]]

        elif compop == '>=':
            instr = [["JLT ", l_reg, r_reg, self._label]]

        return get_reg[0] + instr

    def add_else(self):
        self._label += 1
        return [["JUMP ", self._label]]

    def get_label(self):
        self._label += 1
        return [['LABEL ', self._label]]

    def write_list(self, id_list):
        instr_list =[]
        for i in id_list:
            instr_list += [["WRITE ", i]]
        return instr_list

    def read_list(self, id_list):
        instr_list =[]
        for i in id_list:
            instr_list += [["READ ", i]]
        return instr_list

    def change_type(self, code, d_type):
        if d_type[0] == 'FLOAT':
            for lists in code:
                if lists[0] in self._type_list:
                    st = lists[0][:-2]
                    lists[0] = st + "F "
        return code
