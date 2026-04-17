import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from generated.WhileLangVisitor import WhileLangVisitor
from generated.WhileLangParser import WhileLangParser
from .SymbolTable import SymbolTable, Symbol

class SemanticVisitor(WhileLangVisitor):
    def __init__(self):
        self.table = SymbolTable()

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitDeclaration(self, ctx):
        var_name = ctx.ID().getText()
        type_name = ctx.type_().getText()
        if ctx.expr():
            expr_type = self.visit(ctx.expr())
            if expr_type != 'error_type' and expr_type is not None and type_name != expr_type:
                print(f"Error Semántico: No se puede inicializar '{var_name}' de tipo '{type_name}' con valor de tipo '{expr_type}'.")
                return None
        self.table.insert(var_name, Symbol(var_name, type_name))
        return None

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()
        symbol = self.table.lookup(var_name)
        if symbol is None:
            print(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
            return None
        expr_type = self.visit(ctx.expr())
        if expr_type != 'error_type' and expr_type is not None and symbol.type != expr_type:
            print(f"Error Semántico: No se puede asignar tipo '{expr_type}' a variable '{var_name}' de tipo '{symbol.type}'.")
        return None

    def visitIfStatement(self, ctx):
        cond_type = self.visit(ctx.condition())
        if cond_type == 'string':
            print(f"Error Semántico: La condición del 'if' no puede ser de tipo 'string'.")
        statements = ctx.statement()
        if ctx.ELSE():
            mid = len(statements) // 2
            then_stmts, else_stmts = statements[:mid], statements[mid:]
        else:
            then_stmts, else_stmts = statements, []
        self.table.enter_scope()
        for s in then_stmts: self.visit(s)
        self.table.exit_scope()
        if ctx.ELSE():
            self.table.enter_scope()
            for s in else_stmts: self.visit(s)
            self.table.exit_scope()
        return None

    def visitWhileStatement(self, ctx):
        cond_type = self.visit(ctx.condition())
        if cond_type == 'string':
            print(f"Error Semántico: La condición del 'while' no puede ser de tipo 'string'.")
        self.table.enter_scope()
        for s in ctx.statement(): self.visit(s)
        self.table.exit_scope()
        return None

    def visitCondition(self, ctx):
        return self.visit(ctx.expr())

    def visitBreakStatement(self, ctx): return None
    def visitContinueStatement(self, ctx): return None

    def visitIdExpr(self, ctx):
        var_name = ctx.ID().getText()
        symbol = self.table.lookup(var_name)
        if symbol is None:
            print(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
            return 'error_type'
        return symbol.type

    def visitNumberExpr(self, ctx): return 'int'
    def visitStringExpr(self, ctx): return 'string'
    def visitParenExpr(self, ctx): return self.visit(ctx.expr())

    def visitComparisonExpr(self, ctx):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        if left_type == 'error_type' or right_type == 'error_type': return 'error_type'
        if left_type != right_type:
            print(f"Error Semántico: Comparación entre tipos incompatibles ({left_type} vs {right_type}).")
            return 'error_type'
        if left_type != 'int':
            print(f"Error Semántico: Comparaciones solo permitidas entre enteros, no entre {left_type}.")
            return 'error_type'
        return 'int'

    def visitArithmeticExpr(self, ctx):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        if left_type == 'error_type' or right_type == 'error_type': return 'error_type'
        op = ctx.getChild(1).getText()
        if left_type == 'string' and right_type == 'string':
            if op == '+': return 'string'
            print(f"Error Semántico: Operación '{op}' no permitida entre cadenas.")
            return 'error_type'
        if left_type != 'int' or right_type != 'int':
            print(f"Error Semántico: Operación aritmética solo permitida con enteros, no con {left_type} y {right_type}.")
            return 'error_type'
        return 'int'