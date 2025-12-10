from __future__ import annotations
import rascal_ast as ast
from rascal_ast import (Visitor, Label)

# Espaçamento MEPA para labels
TAB_MEPA = "     "

class Codegen(Visitor):
    
    MEPA_OP = {
        '+': 'SOMA', '-': 'SUBT', '*': 'MULT', 'div': 'DIVI',
        'and': 'CONJ', 'or': 'DISJ',
        '=': 'CMIG', '<>': 'CMDG', '<': 'CMME',
        '<=': 'CMEG', '>': 'CMMA', '>=': 'CMAG',
        'not': 'NEGA',
    }

    def __init__(self):
        self.code: list[str] | None = []
        self.has_error = False
        self.label_counter: int = -1
        self.procs = {} 
        self.current_level = 0

    def _error(self, msg: str):
        print(msg)
        self.has_error = True

    def _send(self, instr: str):
        self.code.append(TAB_MEPA + instr)

    def _send_label(self, label: str):
        self.code.append(f"{label}: NADA")

    def _new_label(self) -> str:
        self.label_counter += 1
        return f"R{self.label_counter:02d}"
    
    # Nós gerais

    def visit_Program(self, node: ast.Program):
        self._send("INPP")
        
        if node.total_vars > 0:
            self._send(f"AMEM {node.total_vars}")
        
        if node.block.methods:
            main_label = self._new_label()
            self._send(f"DSVS {main_label}")
            self.visit(node.block.methods)
            self._send_label(main_label)
        
        self.visit(node.block.cmd)
        
        if node.total_vars > 0:
            self._send(f"DMEM {node.total_vars}")
        self._send("PARA")
        self._send("FIM")

    # Nós de declaração

    def visit_DclrMethod(self, node: ast.DclrMethod):
        label = self._new_label()
        self.procs[node.symbol.name] = label
        self._send_label(label)
        last_level = self.current_level
        self.current_level = node.symbol.lex_level + 1
        self._send(f"ENPR {self.current_level}")
        
        total_vars = node.total_vars
        if total_vars > 0:
            self._send(f"AMEM {total_vars}")
            
        self.visit(node.block.cmd)
        
        if total_vars > 0:
            self._send(f"DMEM {total_vars}")
            
        total_params = 0
        if node.param:
            for par in node.param: 
                total_params += len(par.id_values)
            
        self._send(f"RTPR {total_params}")
        self.current_level = last_level

    def visit_DclrFunction(self, node: ast.DclrFunction):
        label = self._new_label()
        self.procs[node.symbol.name] = label
        self._send_label(label)
        last_level = self.current_level
        self.current_level = node.symbol.lex_level + 1
        self._send(f"ENPR {self.current_level}")
        
        total_vars = node.total_vars
        if total_vars > 0:
            self._send(f"AMEM {total_vars}")
            
        self.visit(node.block.cmd)
        if total_vars > 0:
            self._send(f"DMEM {total_vars}")
            
        total_params = 0
        if node.param:
            for par in node.param:
                total_params += len(par.id_values)
            
        self._send(f"RTPR {total_params}")
        self.current_level = last_level

    # Nós de expressões

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        self.visit(node.left)
        self.visit(node.right)
        op_mepa = self.MEPA_OP.get(node.op)
        if op_mepa: 
            self._send(op_mepa)
        else:
            self._error(f"Operador binário desconhecido {node.op}")

    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        self.visit(node.expr)
        if node.op == '-': 
            self._send("INVR")
        elif node.op == 'not': 
            self._send("NEGA")
        else: 
            self._error(f"Operador unário desconhecido {node.op}")

    def visit_NumberExpr(self, node: ast.NumberExpr):
        self._send(f"CRCT {node.value}")

    def visit_BooleanExpr(self, node: ast.BooleanExpr):
        val = 1 if node.value else 0
        self._send(f"CRCT {val}")

    def visit_VarExpr(self, node: ast.VarExpr):
        self._send(f"CRVL {node.symbol.lex_level},{node.symbol.shift}")

    def visit_FunctionExpr(self, node: ast.FunctionExpr):
        self._send("AMEM 1")
        for arg in reversed(node.args):
            self.visit(arg)
        label = self.procs.get(node.symbol.name)
        self._send(f"CHPR {label},{self.current_level}")

    # Nós de comandos

    def visit_CompoundCmd(self, node: ast.CompoundCmd):
        self.visit(node.cmds)

    def visit_CmdAttribution(self, node: ast.CmdAttribution):
        self.visit(node.expr)
        level = node.symbol.lex_level
        offset = node.symbol.shift
        if node.symbol.label == Label.FUNC:
             level = 1
        if node.symbol and offset is not None:
            self._send(f"ARMZ {level},{offset}")
        else:
            self._erro(f"Deslocamento da variável de atribuição não encontrado.")
        
    def visit_CmdIf(self, node: ast.CmdIf):
        if node.cmd_else:
            lab_end = self._new_label()
            lab_else = self._new_label()
            self.visit(node.cond)
            self._send(f"DSVF {lab_else}")
            self.visit(node.cmd_then)
            self._send(f"DSVS {lab_end}")
            self._send_label(lab_else)
            self.visit(node.cmd_else)
            self._send_label(lab_end)
        else:
            lab_out = self._new_label()
            self.visit(node.cond)
            self._send(f"DSVF {lab_out}")
            self.visit(node.cmd_then)
            self._send_label(lab_out)

    def visit_CmdWhile(self, node: ast.CmdWhile):
        lab_start = self._new_label()
        lab_end = self._new_label()
        self._send_label(lab_start)
        self.visit(node.cond)
        self._send(f"DSVF {lab_end}")
        self.visit(node.cmd_do)
        self._send(f"DSVS {lab_start}")
        self._send_label(lab_end)

    def visit_CmdRead(self, node: ast.CmdRead):
        for symbol in node.symbols:
            self._send("LEIT")
            self._send(f"ARMZ {symbol.lex_level},{symbol.shift}")

    def visit_CmdWrite(self, node: ast.CmdWrite):
        for expr in node.expr:
            self.visit(expr)
            self._send("IMPR")

    def visit_CmdProcedures(self, node: ast.CmdProcedures):
        for arg in reversed(node.args):
            self.visit(arg)
        
        name = node.symbol.name
        if name in self.procs:
            label = self.procs[name]
            self._send(f"CHPR {label},{self.current_level}")
        else:
            self._error(f"Label de '{name}' não encontrado.")