def visitDeclaration(self, ctx):
    var_name = ctx.ID().getText()
    type_name = ctx.type_().getText()
    if ctx.expr():
        expr_type = self.visit(ctx.expr())
        if expr_type != 'error_type' and expr_type is not None and type_name != expr_type:
            self.errors += 1
            print(f"Error Semántico: No se puede inicializar '{var_name}' de tipo '{type_name}' con valor de tipo '{expr_type}'.")
            return None
    inserted = self.table.insert(var_name, Symbol(var_name, type_name))
    if not inserted:
        self.errors += 1
    return None
