# LEXER RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from ply.lex import LexToken
import ply.lex as lex

# Organização do Lexer

reserved = {
    'program' : 'PROGRAM',
    'procedure' : 'PROCEDURE',
    'function' : 'FUNCTION',
    'var' : 'VAR',
    'begin' : 'BEGIN',
    'end' : 'END',
    'integer' : 'INTEGER',
    'boolean' : 'BOOLEAN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'read' : 'READ',
    'write' : 'WRITE',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'div' : 'DIV'
}

# Listagem dos tokens
tokens = [
          'ID',
          'NUMBER',
          'NEQUAL',
          'GREATER_EQUAL',
          'LESSER_EQUAL',
          'ATTRIBUTION'
          ] + list(reserved.values())

# Literais só podem ter 1 caractere
literals = ['+', '-', '*', '=', 
            '>', '<', ':', '(', 
            ')', ',', ';','.']

# Construções para operadores
t_NEQUAL = r'<>'
t_GREATER_EQUAL = r'>='
t_LESSER_EQUAL = r'<='
t_ATTRIBUTION = r':='

# Construções para números e IDs

def t_NUMBER(t) -> LexToken:
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t) -> LexToken:
    r'[a-zA-Z]\w*'
    t.type = reserved.get(t.value, "ID")
    return t

# Regra para contabilizar as linhas
def t_newline(t) -> None:
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para ignorar espaços em branco
t_ignore = ' \t'

# Regra para erro léxico
def t_error(t) -> None:
    print(f'ERRO LÉXICO - símbolo ilegal: {t.value[0]} na linha {t.lexer.lineno}')
    t.lexer.has_error = True
    t.lexer.skip(1)

def Lexer():
    lexer = lex.lex()
    lexer.has_error = False
    return lexer

if __name__ == '__main__':
    pass