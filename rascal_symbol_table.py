# SYMBOL TABLE RASCAL - UEM
# Vitor Madeira Lorençone - 132788
# Enzo Vignotti Sabino - 133791

from __future__ import annotations
from rascal_ast import (Symbol, Label)

# Classe de tabela de símbolos
# Rascal só tem escopo 0 ou 1

class SymbolTable:
    def __init__(self) -> None:
        self.scopes = [dict()]
        self.lex_level = 0
        self.shifts = [0] 

    def opens_scope(self):
        self.scopes.append({})
        self.lex_level = 1
        self.shifts.append(0)

    def closes_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.lex_level = 0
            self.shifts.pop()

    # Adiciona identificador na tabela de símbolos
    def install(self, s: Symbol) -> str | None:
        current = self.scopes[-1]
        if s.name in current:
            return f"ERRO SEMANTICO - Identificador '{s.name}' já declarado neste escopo."
        s.lex_level = self.lex_level
        if s.label in (Label.VAR, Label.PARAM):
            s.shift = self.shifts[-1]
            self.shifts[-1] += 1
        current[s.name] = s
        return None

    # Busca identificador na tabela
    def search(self, name: str) -> Symbol | None:
        for table in reversed(self.scopes):
            if name in table:
                return table[name]
        return None
    
    @property
    def total_vars_scope(self) -> int:
        return self.shifts[-1]