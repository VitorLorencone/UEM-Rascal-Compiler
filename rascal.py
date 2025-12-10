# COMPILADOR RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

import sys
from rascal_lexer import Lexer
from rascal_parser import Parser
from rascal_printer import Printer
from rascal_semantic import Semantic
from rascal_codegen import Codegen
from rascal_onepass import Onepass

# Executa flag -l
def main_lex(input):
    lexer = Lexer()
    data = input.read()
    lexer.input(data)
    while True:
        token = lexer.token()
        if not token:
            break
        print(f'Token: {token.type} | Valor: {token.value}')

    if lexer.has_error:
        print('[Programa com erro léxico]')
        sys.exit(2)

# Executa flag -p
def main_parser(input):
    lexer = Lexer()
    parser = Parser()
    data = input.read()
    parser.parse(data, lexer)

    if lexer.has_error or parser.has_error:
        if lexer.has_error:
            print('[Programa com erro léxico]')
        if parser.has_error:
            print('[Programa com erro sintático]')
        sys.exit(2)

# Executa flag -a
def main_ast(input):
    lexer = Lexer()
    parser = Parser()
    data = input.read()
    ast_root = parser.parse(data, lexer)

    if lexer.has_error or parser.has_error:
        if lexer.has_error:
            print('[Programa com erro léxico]')
        if parser.has_error:
            print('[Programa com erro sintático]')
        sys.exit(2)

    printer = Printer()
    printer.visit(ast_root)

# Executa flag -s
def main_semantic(input):
    lexer = Lexer()
    parser = Parser()
    data = input.read()
    ast_root = parser.parse(data, lexer)

    if lexer.has_error or parser.has_error:
        if lexer.has_error:
            print('[Programa com erro léxico]')
        if parser.has_error:
            print('[Programa com erro sintático]')
        sys.exit(2)

    semantic = Semantic()
    semantic.visit(ast_root)

    if semantic.has_error:
        print('[Programa com erro semântico]')
        sys.exit(2)

# Executa a flag -o
def main_codegen(input, output):
    lexer = Lexer()
    parser = Parser()
    data = input.read()
    ast_root = parser.parse(data, lexer)

    if lexer.has_error or parser.has_error:
        if lexer.has_error:
            print('[Programa com erro léxico]')
        if parser.has_error:
            print('[Programa com erro sintático]')
        sys.exit(2)

    semantic = Semantic()
    semantic.visit(ast_root)

    if semantic.has_error:
        print('[Programa com erro semântico]')
        sys.exit(2)

    codegen = Codegen()
    codegen.visit(ast_root)

    if codegen.has_error:
        print('[Programa com erro de geração de código]')
        sys.exit(2)

    with open(output, 'w') as out:
        for i in codegen.code:
            out.write(i + "\n")

# Executa a flag -op
def main_onepass(input, output):
    lexer = Lexer()
    parser = Parser()
    data = input.read()
    ast_root = parser.parse(data, lexer)

    if lexer.has_error or parser.has_error:
        if lexer.has_error:
            print('[Programa com erro léxico]')
        if parser.has_error:
            print('[Programa com erro sintático]')
        sys.exit(2)

    onepass = Onepass()
    onepass.visit(ast_root)

    if onepass.has_error:
        print('[Programa com erro semântico]')
        sys.exit(2)

    with open(output, 'w') as out:
        for i in onepass.code:
            out.write(i + "\n")

# Função Principal
def main():

    if (len(sys.argv) < 3) or (len(sys.argv) > 4):
        print("Use: python rascal.py <flag> <file.ras> [out]")
        print("Para flags:")
        print("-l : Executa o lexer apenas")
        print("-p : Executa o lexer e parser apenas")
        print("-a : Executa o lexer, parser e imprime AST")
        print("-s : Executa o lexer, parser e semantico")
        print("-o : Executa tudo e gera o arquivo [out].mep")
        print("-op : Executa tudo e gera o arquivo [out].mep em uma travessia pela AST\n")
        sys.exit(1)

    flag: str = sys.argv[1]
    path: str = sys.argv[2]

    with open(path, 'r') as input:

        match flag:
            case '-l':
                main_lex(input)

            case '-p':
                main_parser(input)

            case '-a':
                main_ast(input)

            case '-s':
                main_semantic(input)

            case '-o':
                if len(sys.argv) == 3:
                    print("Uso incorreto da flag '-o', por favor, execute 'python rascal.py' para ajuda")
                    sys.exit(1)
                output = sys.argv[3] + '.mep'
                main_codegen(input, output)
        
            case '-op':
                if len(sys.argv) == 3:
                    print("Uso incorreto da flag '-op', por favor, execute 'python rascal.py' para ajuda")
                    sys.exit(1)
                output = sys.argv[3] + '.mep'
                main_onepass(input, output)

            case _:
                print(f"Flag '{flag}' não conhecida, por favor, execute 'python rascal.py' para ajuda")
                sys.exit(1)

if __name__ == "__main__":
    main()