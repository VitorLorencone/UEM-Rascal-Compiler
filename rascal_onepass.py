# ONE PASS RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from __future__ import annotations
import rascal_ast as ast
from rascal_codegen import Codegen
from rascal_semantic import Semantic

class Onepass(ast.Visitor):
    def __init__(self):
        self.semantic = Semantic()
        self.codegen = Codegen()
        self.has_error = False
        self.code: list[str] = []

    # Nós gerais

    def visit_Program(self, node: ast.Program):
        self.semantic.visit_Program(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_Program(node)
        self.code = self.codegen.code

    def visit_Block(self, node: ast.Block):
        self.semantic.visit_Block(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_Block(node)
        self.code = self.codegen.code

    # Nós declarações

    def visit_DclrVar(self, node: ast.DclrVar):
        self.semantic.visit_DclrVar(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

    def visit_DclrMethod(self, node: ast.DclrMethod):
        self.semantic.visit_DclrMethod(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_DclrMethod(node)
        self.code = self.codegen.code

    def visit_DclrFunction(self, node: ast.DclrFunction):
        self.semantic.visit_DclrFunction(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_DclrFunction(node)
        self.code = self.codegen.code

    def visit_MethodBlock(self, node: ast.MethodBlock):
        self.semantic.visit_MethodBlock(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_MethodBlock(node)
        self.code = self.codegen.code

    # Nós expressões

    def visit_VarExpr(self, node: ast.VarExpr):
        self.semantic.visit_VarExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_VarExpr(node)
        self.code = self.codegen.code

    def visit_FunctionExpr(self, node: ast.FunctionExpr):
        self.semantic.visit_FunctionExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_FunctionExpr(node)
        self.code = self.codegen.code

    def visit_BinaryExpr(self, node: ast.BinaryExpr):
        self.semantic.visit_BinaryExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_BinaryExpr(node)
        self.code = self.codegen.code

    def visit_UnaryExpr(self, node: ast.UnaryExpr):
        self.semantic.visit_UnaryExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_UnaryExpr(node)
        self.code = self.codegen.code

    def visit_NumberExpr(self, node: ast.NumberExpr):
        self.semantic.visit_NumberExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_NumberExpr(node)
        self.code = self.codegen.code

    def visit_BooleanExpr(self, node: ast.BooleanExpr):
        self.semantic.visit_BooleanExpr(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_BooleanExpr(node)
        self.code = self.codegen.code

    # Nós comandos

    def visit_CmdAttribution(self, node: ast.CmdAttribution):
        self.semantic.visit_CmdAttribution(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdAttribution(node)
        self.code = self.codegen.code

    def visit_CmdRead(self, node: ast.CmdRead):
        self.semantic.visit_CmdRead(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdRead(node)
        self.code = self.codegen.code

    def visit_CmdProcedures(self, node: ast.CmdProcedures):
        self.semantic.visit_CmdProcedures(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdProcedures(node)
        self.code = self.codegen.code

    def visit_CmdIf(self, node: ast.CmdIf):
        self.semantic.visit_CmdIf(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdIf(node)
        self.code = self.codegen.code

    def visit_CmdWhile(self, node: ast.CmdWhile):
        self.semantic.visit_CmdWhile(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdWhile(node)
        self.code = self.codegen.code

    def visit_CmdWrite(self, node: ast.CmdWrite):
        self.semantic.visit_CmdWrite(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CmdWrite(node)
        self.code = self.codegen.code

    def visit_CompoundCmd(self, node: ast.CompoundCmd):
        self.semantic.visit_CompoundCmd(node)
        self.has_error = self.semantic.has_error
        if self.has_error: return

        self.codegen.visit_CompoundCmd(node)
        self.code = self.codegen.code