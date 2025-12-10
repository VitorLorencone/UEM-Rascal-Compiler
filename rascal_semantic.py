# SEMANTIC RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from __future__ import annotations
import rascal_ast as ast
from rascal_ast import (Visitor, Symbol, Label, TYPE_INTEGER, TYPE_BOOLEAN)
from rascal_symbol_table import SymbolTable

MEPA_OFFSET = -5

class Semantic(Visitor):
    def __init__(self) -> None:
        self.ts = SymbolTable()
        self.has_error: bool = False
        self.found_return: bool = False
        self.current_func: Symbol | None = None

    def _error(self, msg: str):
        print(msg)
        self.has_error = True

    # Nós gerais

    def visit_Program(self, node: ast.Program):
        prog = Symbol(node.id_value, Label.PROGRAM)
        self.ts.install(prog)
        self.visit(node.block)
        node.total_vars = self.ts.total_vars_scope

    def visit_Block(self, node: ast.Block):
        self.visit(node.var)
        self.visit(node.methods)
        self.visit(node.cmd)

    # Nós declarações

    def visit_DclrVar(self, node: ast.DclrVar):
        if node.var_type == "integer":
            type_var = TYPE_INTEGER
        elif node.var_type == "boolean":
            type_var = TYPE_BOOLEAN
        else:
            self._error(f"ERRO SEMANTICO - Tipo desconhecido '{node.var_type}' na declaração de '{node.id_values}'")

        for ids in node.id_values:
            symbol = Symbol(ids, Label.VAR, type_var)
            error = self.ts.install(symbol)
            if error: 
                self._error(error)

    def visit_DclrMethod(self, node: ast.DclrMethod):
        symbol_method = Symbol(node.id_value, Label.PROC)
        
        if node.param:
            for param in node.param:
                if param.var_type == "integer":
                    type_method = TYPE_INTEGER
                elif param.var_type == "boolean":
                    type_method = TYPE_BOOLEAN
                else:
                    self._error(f"ERRO SEMANTICO - Tipo desconhecido '{param.var_type}' na declaração de '{param.id_values}'")

                for _ in param.id_values:
                    symbol_method.params.append(type_method)
        
        if error := self.ts.install(symbol_method): self._error(error)

        self.ts.opens_scope()
        if node.param:
            current_offset = MEPA_OFFSET
            
            for param in node.param:
                if param.var_type == "integer":
                    types = TYPE_INTEGER
                elif param.var_type == "boolean":
                    types = TYPE_BOOLEAN
                else:
                    self._error(f"ERRO SEMANTICO - Tipo desconhecido '{param.var_type}' na declaração de '{param.id_values}'")

                for ids in param.id_values:
                    symbol_param = Symbol(ids, Label.PARAM, types)
                    symbol_param.lex_level = self.ts.lex_level
                    symbol_param.shift = current_offset
                    if ids in self.ts.scopes[-1]:
                         self._error(f"ERRO SEMANTICO - Parâmetro '{ids}' com identificador repetido.")
                    else:
                         self.ts.scopes[-1][ids] = symbol_param
                    current_offset -= 1 

        self.visit(node.block)
        node.total_vars = self.ts.total_vars_scope
        node.symbol = symbol_method 
        self.ts.closes_scope()

    def visit_DclrFunction(self, node: ast.DclrFunction):
        if node.return_type == "integer":
            return_type = TYPE_INTEGER
        elif node.return_type == "boolean":
            return_type = TYPE_BOOLEAN
        else:
            self._error(f"ERRO SEMANTICO - Tipo desconhecido de retorno '{node.return_type}' na declaração de '{node.id_value}'")
        
        symbol_func = Symbol(node.id_value, Label.FUNC, return_type)
        if node.param:
            for param in node.param:
                if param.var_type == "integer":
                    types = TYPE_INTEGER
                elif param.var_type == "boolean":
                    types = TYPE_BOOLEAN
                else:
                    self._error(f"ERRO SEMANTICO - Tipo desconhecido '{param.var_type}' na declaração de '{param.id_values}'")

                for _ in param.id_values:
                    symbol_func.params.append(types)
        
        if error := self.ts.install(symbol_func): self._error(error)
        self.ts.opens_scope()
        last_func = self.current_func
        self.current_func = symbol_func
        total_params = 0
        if node.param:
            total_params = sum(len(p.id_values) for p in node.param)
        symbol_func.shift = MEPA_OFFSET - total_params
        if node.param:
            current_offset = MEPA_OFFSET
            for param in node.param:
                if param.var_type == "integer":
                    types = TYPE_INTEGER
                elif param.var_type == "boolean":
                    types = TYPE_BOOLEAN
                else:
                    self._error(f"ERRO SEMANTICO - Tipo desconhecido '{param.var_type}' na declaração de '{param.id_values}'")

                for ids in param.id_values:
                    symbol_param = Symbol(ids, Label.PARAM, types)
                    symbol_param.lex_level = self.ts.lex_level
                    symbol_param.shift = current_offset
                    if ids in self.ts.scopes[-1]:
                         self._error(f"ERRO SEMANTICO - Parâmetro '{ids}' com identificador repetido.")
                    else:
                         self.ts.scopes[-1][ids] = symbol_param
                    current_offset -= 1

        last_return = self.found_return
        self.found_return = False
        self.visit(node.block)

        # Sem retorno
        if not self.found_return:
            self._error(f"ERRO SEMANTICO - Função '{node.id_value}' sem retorno.")

        node.total_vars = self.ts.total_vars_scope
        node.symbol = symbol_func
        self.found_return = last_return
        self.current_func = last_func
        self.ts.closes_scope()

    def visit_MethodBlock(self, node: ast.MethodBlock):
        self.visit(node.var)
        self.visit(node.cmd)

    # Nós expressões

    def visit_VarExpr(self, node: ast.VarExpr):
        symbol = self.ts.search(node.id_value)
        if symbol:
            node.expr_type = symbol.symbol_type
            node.symbol = symbol 
        else:
            self._error(f"ERRO SEMANTICO - Variável '{node.id_value}' não declarada.")

    def visit_FunctionExpr(self, node: ast.FunctionExpr):
        symbol = self.ts.search(node.id_value)
        if symbol and symbol.label == Label.FUNC:
            node.expr_type = symbol.symbol_type
            node.symbol = symbol
            args = node.args
            expected = len(symbol.params)
            given = len(args) if args else 0
            
            if expected != given:
                self._error(f"ERRO SEMANTICO - Número incorreto de argumentos em '{symbol.name}' : espera {expected}, recebeu {given}")
            if args:
                for i, arg in enumerate(args):
                    self.visit(arg)
                    received_type = arg.expr_type
                    expected_type = symbol.params[i]
                    if received_type and received_type != expected_type:
                        self._error(f"ERRO SEMANTICO - Tipo incorreto em argumento de posição {i+1} em '{symbol.name}': esperado {expected_type}, recebido {received_type}")
        else:
            self._error(f"ERRO SEMANTICO - Função '{node.id_value}' inválida.")

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        self.visit(node.left)
        self.visit(node.right)
        if node.op in ('and', 'or', '>', '<', '>=', '<=', '=', '<>'):
            node.expr_type = TYPE_BOOLEAN
        else:
            node.expr_type = TYPE_INTEGER

    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        self.visit(node.expr)
        types = node.expr.expr_type
        if types is None:
            node.expr_type = None
            return

        if node.op == '-':
            if types != TYPE_INTEGER:
                self._error(f"ERRO SEMANTICO - Operador unário '-' requer inteiro")
            node.expr_type = TYPE_INTEGER
        elif node.op == 'not':
            if types != TYPE_BOOLEAN:
                self._error(f"ERRO SEMANTICO - Operador unário 'not' requer boolean")
            node.expr_type = TYPE_BOOLEAN

    def visit_NumberExpr(self, node: ast.NumberExpr): node.expr_type = TYPE_INTEGER

    def visit_BooleanExpr(self, node: ast.BooleanExpr): node.expr_type = TYPE_BOOLEAN

    # Nós Comandos

    def visit_CmdAttribution(self, node: ast.CmdAttribution):
        self.visit(node.expr)
        symbol = None

        # Retorno no nome da função
        if self.current_func and node.id_value == self.current_func.name:
            symbol = self.current_func
            self.found_return = True
            expected_type = symbol.symbol_type
        else:
            symbol = self.ts.search(node.id_value)
            if symbol is None:
                self._error(f"ERRO SEMANTICO - Identificador '{node.id_value}' não foi declarado")
                return
            expected_type = symbol.symbol_type
        node.symbol = symbol
        
        if symbol.label not in (Label.VAR, Label.PARAM, Label.FUNC):
            self._error(f"ERRO SEMANTICO - Atribuição não permitida em '{node.id_value}' ({symbol.label})")
            return
            
        if node.expr.expr_type and expected_type != node.expr.expr_type:
            self._error(f"ERRO SEMANTICO - Tipo incorreto em '{node.id_value}': recebeu {node.expr.expr_type}, esperado {expected_type}")

    def visit_CmdRead(self, node: ast.CmdRead):
        node.symbols = [] 
        for var_id in node.id_values:
            symbol = self.ts.search(var_id)
            if symbol:
                node.symbols.append(symbol)
                if symbol.label not in (Label.VAR, Label.PARAM):
                    self._error(f"ERRO SEMANTICO - Identificador '{var_id}' não é parâmetro ou variável")
            else:
                self._error(f"ERRO SEMANTICO - Variável '{var_id}' não declarada.")

    def visit_CmdProcedures(self, node: ast.CmdProcedures):
        symbol = self.ts.search(node.id_value)
        if symbol and symbol.label == Label.PROC:
            node.symbol = symbol
            args = node.args
            expected = len(symbol.params)
            given = len(args) if args else 0
            if expected != given:
                self._error(f"ERRO SEMANTICO - Número incorreto de argumentos em '{symbol.name}' : espera {expected}, recebeu {given}")
            if args:
                for i, arg in enumerate(args):
                    self.visit(arg)
                    received_type = arg.expr_type
                    expected_type = symbol.params[i]
                    if received_type and received_type != expected_type:
                        self._error(f"ERRO SEMANTICO - Tipo incorreto em argumento de posição {i+1} em '{symbol.name}': esperado {expected_type}, recebido {received_type}")
        else:
            self._error(f"ERRO SEMANTICO - Procedimento '{node.id_value}' inválido")
    
    def visit_CmdIf(self, node: ast.CmdIf):
        self.visit(node.cond)
        if node.cond.expr_type != TYPE_BOOLEAN:
            self._error(f"ERRO SEMANTICO - Tipo incorreto em condição do 'if' : esperado 'boolean'.")
        self.visit(node.cmd_then)
        if node.cmd_else: self.visit(node.cmd_else)

    def visit_CmdWhile(self, node: ast.CmdWhile):
        self.visit(node.cond)
        if node.cond.expr_type != TYPE_BOOLEAN:
            self._error(f"ERRO SEMANTICO - Tipo incorreto em condição do 'while' : esperado 'boolean'.")
        self.visit(node.cmd_do)

    def visit_CmdWrite(self, node: ast.CmdWrite):
        self.visit(node.expr)
    
    def visit_CompoundCmd(self, node: ast.CompoundCmd):
        self.visit(node.cmds)