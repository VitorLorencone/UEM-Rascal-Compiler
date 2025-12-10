# Compilador Rascal

Implementação de um compilador para a linguagem Rascal (Reduced Pascal) capaz de gerar código de máquina para MEPA, além de realizar análise léxica, sintática, semântica e impressão da AST, feito em python com ajuda da biblioteca PLY.

Desenvolvido como trabalho da disciplina de Compiladores pelos alunos Vitor Madeira Lorençone e Enzo Vignotti Sabino.

## Uso

```bash
python rascal.py <flag> <file.ras> [out]
```

Para as flags:
- `-l` : Executa o lexer apenas
- `-p` : Executa o lexer e parser apenas
- `-a` : Executa o lexer, parser e imprime AST
- `-s` : Executa o lexer, parser e semantico
- `-o` : Executa tudo e gera o arquivo [out].mep
- `-op` : Executa tudo e gera o arquivo [out].mep em uma travessia pela AST

### Exemplos
```bash
# Análise léxica
python rascal.py -l program.ras

# Análise sintática
python rascal.py -p program.ras

# Impressão da AST
python rascal.py -a program.ras

# Análise semântica
python rascal.py -s program.ras

# Gerar código MEPA
python rascal.py -o program.ras output

# Gerar código MEPA pt2
python rascal.py -op program.ras output
```

Por fim, executa-se o arquivo `output.mep` gerado com a implementação da máquina MEPA

```bash
python ./mepa/mepa_pt.py --progfile output.mep
```