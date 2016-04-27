class Symbol_Table():
    """This class is used in parser.py to create the symbol table
    """
    def __init__(self):
        self._stack = [{}]
        self._output = []
        self._failed = (False, '')
        self._block_cnt = 1

    def add_var(self, v_type, var):
        for lists in var:
            self.add_to_scope(v_type, lists, False, '')

    def add_str(self, var, string):
        self.add_to_scope('STRING', var, True, string)

    def func_start(self, name):
        self._output.append("\nSymbol table " + name)
        self._stack.append({})

    def func_end(self):
        self._stack.pop()

    def block_start(self):
        self._stack.append({})
        self._output.append("\nSymbol table BLOCK " + str(self._block_cnt))
        self._block_cnt += 1

    def block_end(self):
        self._stack.pop()

    def print_output(self):
        if self._failed[0] == False:
            print ("Symbol table GLOBAL")
            for lists in self._output:
                print (lists)
        else:
            print ('DECLARATION ERROR ' + self._failed[1])

    def add_to_scope(self, v_type, name , is_str, str_value):
        if self._failed[0] == False:

            if name in self._stack[-1]:
                self._failed = [True, name]

            else:
                if is_str == True:
                    self._output.append('name ' + name + ' type STRING ' + 'value ' + str_value)
                    self._stack[-1][name] = ['STRING', str_value]
                    
                else:
                    self._output.append('name ' + name + ' type ' + v_type)
                    self._stack[-1][name] = [v_type]

    def search(self, ide):
        return self._stack[0][ide]
