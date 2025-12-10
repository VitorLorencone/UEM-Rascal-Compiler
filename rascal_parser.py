# PARSER RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

import sys
import ply.yacc as yacc
import rascal_ast as ast
from rascal_lexer  import tokens, Lexer, reserved

parser = None

precedence = (
    ('nonassoc', '<', 'LESSER_EQUAL', '>', 'GREATER_EQUAL', '=', 'NEQUAL', 'ATTRIBUTION'),
    ('left', 'OR', '-', '+'),
    ('left', 'AND', 'DIV', '*'),
    ('right', 'NOT', 'MINUS'),
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
)

# Regras gerais

#<programa>
def p_programa(p):
    '''programa : PROGRAM ID ';' bloco '.' '''
    id = p[2]
    block = p[4]
    p[0] = ast.Program(id, block)

#<bloco>
def p_bloco(p):
    '''bloco : secao_declaracao_variaveis secao_declaracao_subrotinas comando_composto
             | secao_declaracao_subrotinas comando_composto
             | secao_declaracao_variaveis comando_composto
             | comando_composto'''
    var = None
    methods = None
    cmds = None

    if len(p) == 4:
        var, methods, cmds = p[1], p[2], p[3]
    elif len(p) == 3:
        if 'secao_declaracao_variaveis' in str(p.slice[1].type):
            var, cmds = p[1], p[2]
        else:
            methods, cmds = p[1], p[2]
    elif len(p) == 2:
        cmds = p[1]

    p[0] = ast.Block(var, methods, cmds)

#<secao_declaracao_variaveis>
def p_secao_declaracao_variaveis(p):
    '''secao_declaracao_variaveis : secao_declaracao_variaveis declaracao_variaveis ';'
                                  | VAR declaracao_variaveis ';' '''
    if p.slice[1].type == 'secao_declaracao_variaveis':
        p[0] = p[1] + [p[2]]
    else:
        # produção base: VAR declaracao_variaveis ';'
        p[0] = [p[2]]  # cria lista com uma declaração

#<declaracao_variaveis>
def p_declaracao_variaveis(p):
    '''declaracao_variaveis : lista_identificadores ':' tipo'''
    id_values = p[1]
    var_type = p[3]
    p[0] = ast.DclrVar(id_values, var_type)

#<lista_identificadores>
def p_lista_identificadores(p):
    '''lista_identificadores : lista_identificadores ',' ID
                               | ID'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

#<tipo>
def p_tipo(p):
    '''tipo : BOOLEAN 
              | INTEGER'''
    p[0] = p[1]

#<secao_declaracao_subrotinas>
def p_declaracao_subrotina(p):
    '''secao_declaracao_subrotinas : secao_declaracao_subrotinas declaracao_procedimento ';'
                                   | secao_declaracao_subrotinas declaracao_funcao ';'
                                   | declaracao_procedimento ';'
                                   | declaracao_funcao ';' '''
    if len(p) == 4:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

#<declaracao_procedimento>
def p_declaracao_procedimento(p):
    '''declaracao_procedimento : PROCEDURE ID parametros_formais ';' bloco_subrot
                               | PROCEDURE ID ';' bloco_subrot'''
    id_value = p[2]

    if p.slice[3].type == 'parametros_formais':
        param = p[3]
        block = p[5]
    else:
        param = []
        block = p[4]
    
    p[0] = ast.DclrMethod(id_value, param, block)

#<declaracao_funcao>
def p_declaracao_funcao(p):
    '''declaracao_funcao : FUNCTION ID parametros_formais ':' tipo ';' bloco_subrot
                          | FUNCTION ID ':' tipo ';' bloco_subrot'''
    id_value = p[2]

    if p.slice[3].type == 'parametros_formais':
        param = p[3]
        return_type = p[5]
        block = p[7]
    else:
        param = []  # sem parâmetros
        return_type = p[4]
        block = p[6]

    p[0] = ast.DclrFunction(id_value, param, return_type, block)

#<bloco_subrot>
def p_bloco_subrot(p):
    '''bloco_subrot : secao_declaracao_variaveis comando_composto
                     | comando_composto'''
    if len(p) == 3:
        var = p[1]
        cmd = p[2]
    else:
        var = None
        cmd = p[1]

    p[0] = ast.MethodBlock(var, cmd)


#<parametros_formais>
def p_parametros_formais(p):
    '''parametros_formais : '(' param_form ')' '''
    p[0] = p[2]

#<param_form>
def p_param_form(p):
    '''param_form : param_form ';' declaracao_parametros
                    | declaracao_parametros'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

#<declaracao_parametros>
def p_declaracao_parametros(p):
    '''declaracao_parametros : lista_identificadores ':' tipo'''
    id_values = p[1]
    var_type = p[3]
    p[0] = ast.Params(id_values, var_type)

# Regras de expressões

#<lista_expressões>
def p_lista_expressoes(p):
    '''lista_expressoes : lista_expressoes ',' expressao
                          | expressao'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

#<expressao_bin>
def p_expressao_bin(p):
    '''expressao : expressao '+' expressao
              | expressao '-' expressao
              | expressao '*' expressao
              | expressao '<' expressao
              | expressao '>' expressao
              | expressao '=' expressao
              | expressao DIV expressao
              | expressao NEQUAL expressao
              | expressao AND expressao
              | expressao OR expressao
              | expressao LESSER_EQUAL expressao
              | expressao GREATER_EQUAL expressao'''
    left = p[1]
    op = p[2]
    right = p[3]
    p[0] = ast.BinaryExpr(left, op, right)

#<expressao_un>
def p_expressao_un(p):
    '''expressao : NOT expressao
              | '-' expressao %prec MINUS'''
    op = p[1]
    expr = p[2]
    p[0] = ast.UnaryExpr(op, expr)

#<expressao_par>
def p_expressao_par(p):
    '''expressao : '(' expressao ')' '''
    p[0] = p[2]

#<expressao_lit>
def p_expressao_lit(p):
    '''expressao : NUMBER
              | FALSE
              | TRUE
              | ID
              | chama_func '''
    
    value = p[1]
    if isinstance(value, int):
        p[0] = ast.NumberExpr(value)
    elif value == 'false':
        p[0] = ast.BooleanExpr(False)
    elif value == 'true':
        p[0] = ast.BooleanExpr(True)
    elif isinstance(value, ast.FunctionExpr):
        p[0] = value
    else:
        p[0] = ast.VarExpr(value)

#<chama_func>
def p_chama_func(p):
    '''chama_func : ID '(' lista_expressoes ')'
                       | ID '(' empty ')' '''
    id_value = p[1]
    args = p[3] if p[3] is not None else []
    p[0] = ast.FunctionExpr(id_value, args)

# Regras de Comandos

#<comando_composto>
def p_comando_composto(p):
    '''comando_composto : BEGIN cmd_comp END'''
    cmds = p[2]
    p[0] = ast.CompoundCmd(cmds)

#<cmd_comp>
def p_cmd_comp(p):
    '''cmd_comp : cmd_comp ';' comando
                  | comando'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

#<comando>
def p_comando(p):
    '''comando : atribuicao
                 | chamada_procedimento
                 | condicional
                 | repeticao
                 | leitura
                 | escrita
                 | comando_composto'''
    p[0] = p[1]

#<atribuicao>
def p_atribuicao(p):
    '''atribuicao : ID ATTRIBUTION expressao'''
    id_value = p[1]
    expr = p[3]
    p[0] = ast.CmdAttribution(id_value, expr)

#<chamada_procedimento>
def p_chamada_procedimento(p):
    '''chamada_procedimento : ID '(' lista_expressoes ')'
                             | ID '(' empty ')' '''
    
    id_value = p[1]
    args = p[3] if p[3] is not None else []
    p[0] = ast.CmdProcedures(id_value, args)

#<condicional>
def p_condicional(p):
    '''condicional : IF expressao THEN comando ELSE comando
                     | IF expressao THEN comando'''
    cond = p[2]
    cmd_then = p[4]
    if len(p) == 5:
        p[0] = ast.CmdIf(cond, cmd_then, None)
    else:
        cmd_else = p[6]
        p[0] = ast.CmdIf(cond, cmd_then, cmd_else)

#<repetição>
def p_repeticao(p):
    '''repeticao : WHILE expressao DO comando'''
    cond = p[2]
    cmd_do = p[4]
    p[0] = ast.CmdWhile(cond, cmd_do)

#<leitura>
def p_leitura(p):
    '''leitura : READ '(' lista_identificadores ')' '''
    id_values = p[3]
    p[0] = ast.CmdRead(id_values)

#<escrita>
def p_escrita(p):
    '''escrita : WRITE '(' lista_expressoes ')' '''
    expr = p[3]
    p[0] = ast.CmdWrite(expr)

# Regras de Erro -> Apenas uma por problemas de implementação

#<condicional_error_then>
def p_condicional_error_then(p):
    '''condicional : IF expressao error comando'''
    print(f"|--- ERRO: 'IF' sem 'THEN' na linha {p.lineno(1)}", file=sys.stderr)
    p[0] = ast.CmdIf(p[2], None, None)

# REGRAS AUXILIARES

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    global parser
    if not p:
        print("ERRO SINTÁTICO - Fim de arquivo inesperado (EOF).", file=sys.stderr)
        parser.has_error = True
        return

    print(f"ERRO SINTÁTICO - Token inesperado: {p.type} ('{p.value}') na linha {p.lineno}", file=sys.stderr)
    parser.has_error = True

    # Recuperação token de sincronia
    while True:
        tok = parser.token()
        if not tok or tok.type in (list(reserved.values()) + [';', '.']):
            break

def Parser():
    global parser
    parser = yacc.yacc(debug=True)
    parser.has_error = False
    return parser