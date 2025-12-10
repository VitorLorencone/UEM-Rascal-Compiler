# AST RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from __future__ import annotations
from dataclasses import (dataclass, field)

# Criação de Tipos para AST e outros

class Node:...

class Type:...

@dataclass()
class IntegerType(Type):
    def __str__(self) -> str: return "integer"

@dataclass()
class BooleanType(Type):
    def __str__(self) -> str: return "boolean"

TYPE_INTEGER = IntegerType()
TYPE_BOOLEAN = BooleanType()

class Label:
    PROGRAM = 'program'
    FUNC = 'function'
    PROC = 'procedure'
    PARAM = 'param'
    VAR = 'var'

@dataclass
class Symbol:
    name: str
    label: str
    symbol_type: Type | None = None
    lex_level: int = 0
    shift: int = 0
    title: str = ""
    params: list[Type] = field(default_factory=list)

# Visitor Genérico para AST

class Visitor:
    def visit(self, node: Node):
        if node is None:
            return
        
        # Visita cada item de uma lista, poupa um for
        if isinstance(node, list):
            for item in node:
                self.visit(item)
            return

        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.default_visit)
        return visitor(node)

    def default_visit(self, node: Node):
        raise NotImplementedError(f"visit_{type(node).__name__} não implementado.")

# Definições de nós da AST

# Superclasses

class Expr(Node):
    expr_type: Type | None = None

class Cmd(Node):...

class Dclr(Node):...

# Classes de nós

# Gerais

@dataclass
class Program(Node):
    id_value: str
    block: Block
    total_vars: int = 0

@dataclass
class Block(Node):
    var: list[DclrVar]
    methods: list[DclrMethod]
    cmd: CompoundCmd

@dataclass
class MethodBlock(Node):
    var: list[DclrVar]
    cmd: CompoundCmd

# Declarações

@dataclass
class DclrVar(Dclr):
    id_values: list[str]
    var_type: str

@dataclass
class Params(Dclr):
    id_values: list[str]
    var_type: str

@dataclass
class DclrMethod(Dclr):
    id_value: str
    param: list[Params]
    block: MethodBlock
    total_vars: int = 0
    symbol: Symbol | None = None

@dataclass
class DclrFunction(Dclr):
    id_value: str
    param: list[Params]
    return_type: str
    block: MethodBlock
    total_vars: int = 0
    symbol: Symbol | None = None

# Expressões

@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class UnaryExpr(Expr):
    op: str
    expr: Expr

@dataclass
class VarExpr(Expr):
    id_value: str
    symbol: Symbol | None = None

@dataclass
class FunctionExpr(Expr):
    id_value: str
    args: list[Expr]
    symbol: Symbol | None = None

@dataclass
class NumberExpr(Expr):
    value: int

@dataclass
class BooleanExpr(Expr):
    value: bool

# Comandos

@dataclass
class CompoundCmd(Cmd):
    cmds: list[Cmd]

@dataclass
class CmdAttribution(Cmd):
    id_value: str
    expr: Expr
    symbol: Symbol | None = None

@dataclass
class CmdProcedures(Cmd):
    id_value: str
    args: list[Expr]
    symbol: Symbol | None = None

@dataclass
class CmdIf(Cmd):
    cond: Expr
    cmd_then: Cmd
    cmd_else: Cmd | None

@dataclass
class CmdWhile(Cmd):
    cond: Expr
    cmd_do: Cmd

@dataclass
class CmdRead(Cmd):
    id_values: list[str] 
    symbols: list[Symbol] = field(default_factory=list)

@dataclass
class CmdWrite(Cmd):
    expr: list[Expr]