class tree2f:
    def __init__ (self):
        self.stack = []
        self.brackets=[]
    def push (self, p):
        if p in ['add', 'sub', 'mul', 'safe_div']:
            if p=='add':
                p='+'
            elif p=='sub':
                p='-'
            elif p=='mul':
                p='*'
            elif p=='safe_div':
                p='/'
            op1 = self.stack.pop()
            op2 = self.stack.pop()
            self.stack.append('(%s%s%s)' % (op1, p, op2))
        elif p == '!':
            op = self.stack.pop()
            self.stack.append ('%s!' % (op) )
        elif p in ['sin', 'cos', 'tan', 'mylog', 'tanh','mysqrt', 'mypower2', 'mypower3']:
            op = self.stack.pop()
            self.stack.append('%s(%s)' % (p, op))
        else:
            self.stack.append (p)

    def push_r(self, p):
        if p in ['add', 'sub', 'mul', 'safe_div']:
            self.stack.append('%s(' % (p))
            self.brackets.append(')')
        elif p == '!':
            op = self.stack.pop ()
            self.stack.append('%s!' % (op) )
        elif p in ['sin', 'cos', 'tan', 'mylog','tanh','mysqrt']:
            self.stack.append('%s(' % (p))
            self.brackets.append(')')
        else:
            op= self.stack.pop()
            if not op in ['add(', 'sub(', 'mul(', 'safe_div(','sin(', 'cos(', 'tan(', 'mylog(','tanh(','mysqrt(']:
                self.stack.append('%s%s),' % (op,p))
                self.brackets.pop()
            else:
                self.stack.append('%s' % (op))
                self.stack.append('%s,' % (p))


            #self.stack.append(p)

    def convert(self, l):
        l.reverse()
        for e in l:
            self.push(e)
        return self.stack.pop()
    def convert_r(self, l):
        #l.reverse()
        for e in l:
            self.push_r(e)
        cadena=''.join(self.stack)
        cadena = cadena[:-1]
        cadena2=''.join(self.brackets)
        cad=cadena+cadena2
        return cad