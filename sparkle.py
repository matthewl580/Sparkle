# Holds the code for the lanague
#################################
# ------------------ CONSTANTS
##################################
DIGITS = "0123456789"


#################################
# ------------------ Error
##################################


class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
   
    def as_string(self):
        result = "\n[*** Error! ***] \n"
        result += f' -- Summary:\n'
        result += f'  Type: {self.error_name} | Details: {self.details}'
        result += f'\n -- Location:\n'
        result += f'  File: {self.pos_start.fn} | Line: {self.pos_start.ln + 1} \n'
        result += "----------\n"
       
        return result


class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end, details):
        super().__init__(pos_start,pos_end,"Illegal Character",details)


#################################
# ------------------ POSITION
# idx: index
# ln: line number
# col: Collum number
#fn:file_name
# ftxt: file_text
##################################
class Position:
    def __init__(self, idx, ln,col,fn, ftxt):
        self.fn = fn
        self.ftxt = ftxt
        self.idx = idx
        self.ln = ln
        self.col = col
    def advance(self,current_char):
        self.idx +=1
        self.col +=1


        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
   
    def copy(self):
        return Position(self.idx, self.ln,self.col,self.fn, self.ftxt)


#################################
# ------------------ TOKENS
# TT: Token Type
##################################
TT_INT = "TT_INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "TT_LPAREN"
TT_RPAREN = "TT_RPAREN"


class Token:
    def __init__(self,type_,value=None):
        self.type = type_
        self.value = value


    def __repr__ (self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
   


#################################
# ------------------ Lexer
##################################
class Lexer:
    def __init__(self,fn,text):
            self.fn = fn
            self.text = text
            self.pos = Position(-1,0,-1,fn,text)
            self.current_char = None
            self.advance()


    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None


    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
               
            # Handle Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                # We don't find the charahcter we're looking for, return an error
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,"'"+char+"'")
        return tokens, None


    def make_number(self):
        num_str= ""
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()    
           
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


 #################################
# ------------------ Nodes
# tok: token
##################################
class NumberNode:
    def __init__(self,tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'
   
 # Binary Opperation Node  
# op_tok: Operation token


class BinOpNode:
    def __init__(self,left_node, op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
   
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
   
#################################
# ------------------ PARSER
##################################    
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()


    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx  < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
########################################################
    def parse(self):
        res = self.expr()
        return res






    def factor(self):
        tok = self.current_tok
        if tok.type in (TT_INT,TT_FLOAT):
            self.advance()
        return NumberNode(tok)


    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))


    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))


    def bin_op(self,func,ops):
        left = func()
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left


#################################
# ------------------ RUN
##################################


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return  None, error
# Generate Abtract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()


    return ast, error
# Holds the code for the lanague
#################################
# ------------------ CONSTANTS
##################################
DIGITS = "0123456789"


#################################
# ------------------ Error
##################################


class Error:
    def __init__(self,pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
   
    def as_string(self):
        result = "\n[*** Error! ***] \n"
        result += f' -- Summary:\n'
        result += f'  Type: {self.error_name} | Details: {self.details}'
        result += f'\n -- Location:\n'
        result += f'  File: {self.pos_start.fn} | Line: {self.pos_start.ln + 1} \n'
        result += "----------\n"
       
        return result


class IllegalCharError(Error):
    def __init__(self,pos_start,pos_end, details):
        super().__init__(pos_start,pos_end,"Illegal Character",details)


#################################
# ------------------ POSITION
# idx: index
# ln: line number
# col: Collum number
#fn:file_name
# ftxt: file_text
##################################
class Position:
    def __init__(self, idx, ln,col,fn, ftxt):
        self.fn = fn
        self.ftxt = ftxt
        self.idx = idx
        self.ln = ln
        self.col = col
    def advance(self,current_char):
        self.idx +=1
        self.col +=1


        if current_char == "\n":
            self.ln += 1
            self.col = 0
        return self
   
    def copy(self):
        return Position(self.idx, self.ln,self.col,self.fn, self.ftxt)


#################################
# ------------------ TOKENS
# TT: Token Type
##################################
TT_INT = "TT_INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "TT_LPAREN"
TT_RPAREN = "TT_RPAREN"


class Token:
    def __init__(self,type_,value=None):
        self.type = type_
        self.value = value


    def __repr__ (self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
   


#################################
# ------------------ Lexer
##################################
class Lexer:
    def __init__(self,fn,text):
            self.fn = fn
            self.text = text
            self.pos = Position(-1,0,-1,fn,text)
            self.current_char = None
            self.advance()


    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None


    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
               
            # Handle Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                # We don't find the charahcter we're looking for, return an error
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start,self.pos,"'"+char+"'")
        return tokens, None


    def make_number(self):
        num_str= ""
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()    
           
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


 #################################
# ------------------ Nodes
# tok: token
##################################
class NumberNode:
    def __init__(self,tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'
   
 # Binary Opperation Node  
# op_tok: Operation token


class BinOpNode:
    def __init__(self,left_node, op_tok,right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
   
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
   
#################################
# ------------------ PARSER
##################################    
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()


    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx  < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
########################################################
    def parse(self):
        res = self.expr()
        return res






    def factor(self):
        tok = self.current_tok
        if tok.type in (TT_INT,TT_FLOAT):
            self.advance()
        return NumberNode(tok)


    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))


    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))


    def bin_op(self,func,ops):
        left = func()
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left


#################################
# ------------------ RUN
##################################


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return  None, error
# Generate Abtract Syntax Tree
    parser = Parser(tokens)
    ast = parser.parse()


    return ast, error
