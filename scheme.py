from antlr4 import *
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from schemeVisitor import schemeVisitor
import sys

class EvalVisitor(schemeVisitor):

    def __init__(self):
        self.tfs = {}
        self.ts = [{}]    # es una pila

    def visitRoot(self,ctx):
        res = self.visitChildren(ctx)
        if 'main' in self.tfs: 
           res = self.visitFunction2('main',[])
        return res

    def visitParentesi(self, ctx):
        children = list(ctx.getChildren())  

        if children[0].getText() == '(':
                
            if len(children) > 0 and children[1].getText() == 'display': self.visitDisplay(ctx)
            
            elif len(children) > 0 and children[1].getText() in {'+', '-', '*', '/', '^', '>', '<', '=', '<>', 'and', 'or', 'not', 'mod'}:
                return self.visitOperador(children[1:-1]) # Elimina '(' i ')'

            elif len(children) > 0 and children[1].getText() == 'define':
                if(children[2].getText()[0] == '('): return self.visitDefine(ctx) 
                else: 
                    constType = children[3].getText()[0]
                    if (constType == "'"): 
                        return self.defineLlista(ctx)
                    else: 
                        return self.defineConstant(ctx)

            elif len(children) > 0 and children[1].getText() == 'if':
                return self.visitIf(ctx) 

            elif len(children) > 0 and children[1].getText() == 'cond':
                return self.visitCond(ctx)

            elif len(children) > 0 and children[1].getText() == 'car':
                return self.visitCar(ctx)

            elif len(children) > 0 and children[1].getText() == 'cdr':
                return self.visitCdr(ctx)

            elif len(children) > 0 and children[1].getText() == 'cons':
                return self.visitCons(ctx)

            elif len(children) > 0 and children[1].getText() == 'null?':
                return self.visitNull(ctx)

            elif len(children) > 0 and children[1].getText() == 'let':
                return self.visitLet(ctx)
            
            elif len(children) > 0 and children[1].getText() == 'read':
                return self.visitRead(ctx)
            
            elif len(children) > 0 and children[1].getText() == 'newline':
                return self.visitNewLine(ctx)

            # crida a funcio
            elif len(children) > 0 and children[1].getText() in self.tfs or children[1].getText() in self.ts[-1]:
                return self.visitFunction(ctx)

            elif len(children) > 0:
                llista = [child.getText() for child in children] 
                return llista
                
            elif len(children) == 1:    # Si només hi ha una expressió, visita-la
                return self.visit(children[0])
            else:   # Parèntesi buit retorna 0
                return 0

        else:   # atomics 
            atomic = children[0].getText()
            if atomic.isdigit(): return self.visitNumero(ctx)
            if atomic == "'(": return self.visitLlista(ctx)
            if atomic == "#t" or atomic == "#f": return atomic == "#t"
            if atomic[0] == '"' and atomic[-1] == '"': return atomic[1:-1] #string
            else: return self.visitId(atomic)

    # OPERACIONS

    def visitOperador(self, ctx):
        # op a b
        operador = ctx[0].getText() 
        operands = [self.visit(child) for child in ctx[1:]]  # Avaluar cada operand

        d = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '/': lambda x, y: x / y,
            '*': lambda x, y: x * y,
            '^': lambda x, y: x ** y,
            '>': lambda x, y: x > y,
            '<': lambda x, y: x < y, 
            '=': lambda x, y: x == y, 
            '<>': lambda x, y: x != y,
            'mod': lambda x, y: x%y,
            'and': lambda x, y: x and y, 
            'or': lambda x, y: x or y, 
            'not': lambda x: not x
        }

        if(operador == 'not'):
            a = operands[0]
            result = d[operador](a)
        else:
            a = operands[0]
            b = operands[1]
            result = d[operador](a, b)

        return result

    # DEFINE

    def defineConstant(self,ctx):
        # ( define nom valor )
        children = list(ctx.getChildren())
        name = children[2]
        value = children[3]
        self.ts[0][name.getText()] = self.visitParentesi(value)

    def defineLlista(self,ctx):  
        # ( define nom expr )   
        children = list(ctx.getChildren())
        nom = children[2]
        llista = children[3]
        valors = list(llista.getChildren())[1:-1]
        l = []
        for v in valors:
            l.append(self.visitParentesi(v))
        self.ts[0][nom.getText()] = l

    def getInfoFunction(self,ctx):
        children = list(ctx.getChildren()) 
        define = children[0]
        name = children[1]
        args = children [2:-1]
        params = [arg.getText() for arg in args]
        return [name,params]

    def visitDefine(self, ctx):
        # ( define (nom arg1 arg2 ...) expr1 expr2 ... )
        children = list(ctx.getChildren())
        funcio = children[2]
        [name,params] = self.getInfoFunction(funcio)
        exprs = children[3:-1] 

        self.tfs[name.getText()] = (params, exprs)

    # CONDICIONALS

    def visitIf(self, ctx):
        # ( if cond expr1 expr2 )list(ctx.getChildren())
        children = list(ctx.getChildren())
        cond = children[2]
        expr1 = children[3]
        expr2 = children[4]
        if (self.visitParentesi(cond)):
            return self.visitParentesi(expr1)
        else:
            return self.visitParentesi(expr2)

    def visitCond(self,ctx):
        # ( cond expr1 expr2 ...)
        children = list(ctx.getChildren())
        cond = children[1]
        exprs = children[2:]
        for e in exprs:
            # ( cond cos ) 
            [par, cond, cos, par2] = e.getChildren()
            if(self.visitParentesi(cond)): return self.visitParentesi(cos)
        
    # OPERACIONS AMB LLISTES

    def visitCar(self,ctx):
        # ( car name )
        children = list(ctx.getChildren())
        llista = self.visitParentesi(children[2])
        return llista[0]

    def visitCdr(self,ctx):
        # ( cdr name )
        children = list(ctx.getChildren())
        llista = self.visitParentesi(children[2])
        return llista[1:]

    def visitCons(self,ctx):
        # ( cdr elem name )
        children = list(ctx.getChildren())
        elem = self.visitParentesi(children[2])
        llista = self.visitParentesi(children[3])
        llista.insert(0,elem)
        return llista        

    def visitNull(self,ctx):  
        # ( null? name )
        children = list(ctx.getChildren())
        llista = self.visitParentesi(children[2])
        return len(llista) == 0

    # LET

    def visitLet(self,ctx):
        # ( let variables expr )
        children = list(ctx.getChildren())
        # ( expr1 expr2 ... )
        variables = list(children[2].getChildren())[1:-1]
        varLoc = []
        for v in variables:
            # ( variable valor )
            [par3,var,val,par4] = list(v.getChildren())
            self.ts[-1][var.getText()] = self.visitParentesi(val)
            varLoc.append(var.getText())

        exprs = list(ctx.getChildren())[3:-1]
        ret = None
        for e in exprs:
            ret = self.visitParentesi(e)
            if(ret != None): return ret

        # eliminem les variables locals de la taula de simbols
        for var in varLoc: 
            del self.ts[-1][var]

        return ret

    # ENTRADA/SORTIDA

    def visitRead(self,ctx):
        x = int(input())
        return x

    def visitNewLine(self,ctx): 
        print()     # salt de linia

    def visitDisplay(self,ctx):
        # ( display expr )
        children = list(ctx.getChildren())
        expr = children[2]
        print(self.visitParentesi(expr))

    # FUNCIONS

    def getParameters(self, exprs):
        params = []
        for e in exprs: 
            if(e.getText() in self.tfs):
                info = self.tfs[e.getText()] 
                params.append(info)
            else: 
                params.append(self.visitParentesi(e)) 
        return params

    def getArgs(self, f):
        if f in self.tfs: 
            func = self.tfs[f]
            variables = func[0]
            cos = func[1]
        elif f in self.ts[-1]:
            func = self.ts[-1][f]
            variables = func[0]
            cos = func[1]
        return [variables,cos]


    def visitFunction(self, ctx):
        # ( name expr1 expr2 ...)
        children = list(ctx.getChildren())
        exprs = self.getParameters(children[2:-1])
        name = children[1].getText()
        return self.visitFunction2(name, exprs)

    def visitFunction2(self,name,exprs):
        [variables,cos] = self.getArgs(name)

        # Asignar parametres
        tsact = {}
        for variable, expression in zip(variables, exprs):
            tsact[variable] = expression
        self.ts.append(tsact)

        for expr in cos: 
            x = self.visitParentesi(expr)
            if (x != None):
                self.ts.pop()
                return x 
        self.ts.pop()

    # ATOMICS

    def visitIdentificador(self, ctx):
        variable = list(ctx.getChildren())
        tsact = self.ts[-1]
        return int(tsact[variable[0].getText()])

    def visitString(self,ctx):
        [children] = list(ctx.getChildren())
        return children.getText()

    def visitNumero(self, ctx):
        numero = list(ctx.getChildren())
        return int(numero[0].getText())

    def visitId(self,name):
        if (name in self.ts[-1]):
            return self.ts[-1][name]
        else: 
            if(name in self.ts[0]):
                return self.ts[0][name]
            else: 
                return name

    def visitLlista(self,ctx):
        # '( expr )
        elems = list(ctx.getChildren())[1:-1] #elements de la llista
        l = []
        for elem in elems:
            l.append(self.visitParentesi(elem))
        
        return l

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scheme.py <archivo.scm>")
        sys.exit(1)

input_stream = FileStream(sys.argv[1], encoding="utf-8")
lexer = schemeLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = schemeParser(token_stream)
tree = parser.root()

evaluator = EvalVisitor()
evaluator.visit(tree)