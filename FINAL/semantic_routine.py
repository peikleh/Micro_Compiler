class Semantic_Routine():
    """This class is used to convert the source code into IR code. It will then
    turned into tiny code by another class
    """

    def __init__(self):
        self._output = []
        self._r_num = 0
        self._label = 0
        self._type_list = ["ADDI ", "SUBI ", "MULI ", "DIVI ", "STOREI " ]
        self._jump_list = ["JGEI ", "JNEI ", "JEQI ", "JGTI ", "JLTI ", "JLEI "]

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

    def add_cond(self, l_side, compop, r_side, d_type):
        get_reg = self.make_op(l_side + [compop], r_side)
        l_reg = get_reg[1]
        r_reg = get_reg[2]
        self._label += 1
        instr = ''

        if compop == '<':
            instr = [["JGEI ", l_reg, r_reg, self._label]]

        elif compop == '>':
            instr = [["JLEI ", l_reg, r_reg, self._label]]

        elif compop == '=':
            instr = [["JNEI ", l_reg, r_reg, self._label]]

        elif compop == '!=':
            instr = [["JEQI ", l_reg, r_reg, self._label]]

        elif compop == '<=':
            instr = [["JGTI ", l_reg, r_reg, self._label]]

        elif compop == '>=':
            instr = [["JLTI ", l_reg, r_reg, self._label]]

        instr = get_reg[0] + instr
        instr = self.change_type(instr, d_type)

        return instr

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
                if lists[0] in self._type_list or lists [0] in self._jump_list:
                    st = lists[0][:-2]
                    lists[0] = st + "F "
        return code
class IR_To_Tiny():
    """Converts IR code to tiny code"""
    def __init__(self, IR):
        self.IR = IR
        self.cur_reg = 1
        self.reg_offset = -1

        self.i_list = []
        self._type_list = ["ADDI ", "SUBI ", "MULI ", "DIVI ", "ADDF ",\
         "SUBF ", "MULF ", "DIVF " ]
        self._jump_list = ["JGEI ", "JNEI ", "JEQI ", "JGTI ", "JLTI ", "JLEI ",\
        "JGEF ", "JNEF ", "JEQF ", "JGTF ", "JLTF ", "JLEF "]

        for lists in IR:
            print lists
            if lists[0] == "STOREF " or lists[0] == "STOREI ":
                lists = self.to_move(lists)
            elif lists[0] in self._type_list:
                self.to_add(lists)
            elif lists[0] in self._jump_list:
                self.to_jump(lists)
            elif lists[0] == "LABEL ":
                self.to_label(lists)
            elif lists[0] == "JUMP ":
                self.to_jmp(lists)

        for lists in self.i_list:
            print lists


    def to_move(self, instr):
        if self.is_id(instr[1]) and self.is_id(instr[2]):
            instr1 ="move " + instr[1] + " r" + str(self.cur_reg + self.reg_offset + 1)
            instr2 = "move r" + str(self.cur_reg + self.reg_offset + 1) + " " \
             + instr[2]

            self.reg_offset += 1
            self.i_list.append(instr1)
            self.i_list.append(instr2)

        else:
            instr = "move " + self.is_reg(instr[1]) + " " + self.is_reg(instr[2])
            self.i_list.append(instr)


    def to_add(self, instr):
        instr1 = ''
        instr2 = ''

        if not self.is_id(instr[1]):
            instr1 = "move " + "r" + str(instr[1]+self.reg_offset) + " r" + str(instr[3] + self.reg_offset)
        else:
            instr1 = "move " + str(instr[1]) + " r" + str(instr[3] + self.reg_offset)

        if not self.is_id(instr[2]):
            instr2 = self.op_to_ir(instr[0]) + "r" + str(instr[2] + self.reg_offset) + " r" + str(instr[3] + self.reg_offset)
        else:
            instr2 = self.op_to_ir(instr[0]) + str(instr[2]) + " r" + str(instr[3] + self.reg_offset)

        self.is_reg(instr[3])
        self.i_list.append(instr1)
        self.i_list.append(instr2)

    def to_jump(self, instr):
        instr = self.add_reg(instr)

        if instr[0][-2] == 'I':
            instr1 = "cmpi " + self.is_reg(instr[1]) + " " + self.is_reg(instr[2])
        else:
            instr1 = "cmpr " + self.is_reg(instr[1]) + " " + self.is_reg(instr[2])
        self.i_list.append(instr1)
        instr2 = self.strip_type(instr[0]) + "label" + str(instr[3])
        self.i_list.append(instr2)

    def to_label(self, instr):
        instr1 = "label " + "label" + str(instr[1])
        self.i_list.append(instr1)

    def to_jmp(self, instr):
        instr1 = "jmp " + "label" + str(instr[1])
        self.i_list.append(instr1)

    def add_reg(self, instr):
        if self.is_id(instr[1]) and self.is_id(instr[2]):
            m_instr = "move " + instr[1] + " r" + str(self.cur_reg + self.reg_offset + 1)
            instr = [instr[0], self.cur_reg + self.reg_offset + 1, instr[2], instr[3]]
            self.reg_offset += 1
            self.i_list.append(m_instr)
            return instr
        else:
            return instr

    def op_to_ir(self, op):
        if op[-2] == 'I':
            return op.lower()
        else:
            op = op[:-2]
            op = op +"R "
            return op.lower()

    def strip_type(self, op):
        op = op[:-2]
        op = op + " "
        return op.lower()

    def is_reg(self, p_reg):
        if isinstance(p_reg, int):
            if p_reg > self.cur_reg:
                self.cur_reg = p_reg
            return "r" + str(p_reg + self.reg_offset)

        else:
            return p_reg

    def is_id(self, p_id):
        if isinstance(p_id, str):
            if p_id[0].isalpha():
                return True
        return False
