# PRINTER RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from __future__ import annotations
import sys
import rascal_ast as ast
from rascal_ast import Visitor

# Tamanho da tabulação do Printer, para customizar
TAB = "   "

# Estrutura do printer

class Printer(Visitor):
    def __init__(self, out = sys.stdout):
        self.out = out

    def print(self, txt: str):
        self.out.write(txt)

    # Print dos nós gerais

    def visit_Program(self, node: ast.Program):
        self.print("\n(Program ")
        self.print(node.id_value)
        self.print(f"\n{TAB}")
        self.visit(node.block)
        self.print(")\n\n")
    
    def visit_Block(self, node: ast.Block):
        self.print("(Block")
        if node.var:
            self.print(f"\n{TAB * 2}(Variables")
            for v in node.var:
                self.print(" ")
                self.visit(v)
            self.print(")")
        if node.methods:
            self.print(f"\n{TAB * 2}(Methods")
            for method in node.methods:
                self.print(f"\n{TAB * 3}")
                self.visit(method)
            self.print(")")
        self.print(f"\n{TAB * 2}")
        self.visit(node.cmd)
        self.print(")")
    
    def visit_MethodBlock(self, node: ast.MethodBlock):
        self.print("(Body")
        if node.var:
            self.print(" (Variables")
            for v in node.var:
                self.print(" ")
                self.visit(v)
            self.print(")")
        self.print(" ")
        self.visit(node.cmd)
        self.print(")")

    # Print Declarações

    def visit_DclrVar(self, node: ast.DclrVar):
        self.print(f"{{{", ".join(node.id_values)} : {node.var_type}}}")

    def visit_DclrMethod(self, node: ast.DclrMethod):
        self.print(f"(Procedure {node.id_value} parameters:{{")
        if node.param:
            self.visit(node.param)
        self.print("} ")
        self.visit(node.block)
        self.print(")")

    def visit_DclrFunction(self, node: ast.DclrFunction):
        self.print(f"(Function {node.id_value} :{node.return_type} parameters:{{")
        if node.param:
            self.visit(node.param)
        self.print("} ")
        self.visit(node.block)
        self.print(")")

    def visit_Params(self, node: ast.Params):
        self.print(f" {{{", ".join(node.id_values)}:{node.var_type}}} ")

    # Print expressões

    def visit_VarExpr(self, node: ast.VarExpr):
        self.print(f"(Variable {node.id_value})")

    def visit_NumberExpr(self, node: ast.NumberExpr):
        self.print(str(node.value))

    def visit_BooleanExpr(self, node: ast.BooleanExpr):
        self.print(str(node.value).lower())

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        self.print(f"({node.op} ")
        self.visit(node.left)
        self.print(" ")
        self.visit(node.right)
        self.print(")")

    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        self.print(f"({node.op} ")
        self.visit(node.expr)
        self.print(")")

    def visit_FunctionExpr(self, node: ast.FunctionExpr):
        self.print(f"(FuncCall {node.id_value}")
        if node.args:
            for arg in node.args:
                self.print(" ")
                self.visit(arg)
        self.print(")")

    def visit_IdExpr(self, node: ast.IdExpr):
        self.print(f"(ID {node.name})")

    # Print comandos

    def visit_CompoundCmd(self, node: ast.CompoundCmd):
        self.print("(Begin")
        for cmd in node.cmds:
            self.print(f"\n{TAB * 3}")
            self.visit(cmd)
        self.print(")")

    def visit_CmdIf(self, node: ast.CmdIf):
        self.print("(if ")
        self.visit(node.cond)
        self.print(f"\n{TAB * 4}then ")
        self.visit(node.cmd_then)
        if node.cmd_else:
            self.print(f"\n{TAB * 4}Else ")
            self.visit(node.cmd_else)
        self.print(")")
    
    def visit_CmdWhile(self, node: ast.CmdWhile):
        self.print("(while ")
        self.visit(node.cond)
        self.print(f"\n{TAB * 4}Do ")
        self.visit(node.cmd_do)
        self.print(")")

    def visit_CmdAttribution(self, node: ast.CmdAttribution):
        self.print(f"(Attribution {node.id_value} ")
        self.visit(node.expr)
        self.print(")")

    def visit_CmdRead(self, node: ast.CmdRead):
        self.print(f"(Read {", ".join(node.id_values)})")

    def visit_CmdWrite(self, node: ast.CmdWrite):
        self.print("(Write")
        for expr in node.expr:
            self.print(" ")
            self.visit(expr)
        self.print(")")

    def visit_CmdProcedures(self, node: ast.CmdProcedures):
        self.print(f"(ProcCall {node.id_value}")
        if node.args:
            for arg in node.args:
                self.print(" ")
                self.visit(arg)
        self.print(")")