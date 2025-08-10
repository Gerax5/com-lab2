from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
      raise TypeError(f"Unsupported operand types for {op}: {left_type} and {right_type}")
    
    if op == '%':
      if isinstance(left_type, IntType) and isinstance(right_type, IntType):
          if self._is_literal_zero(ctx.expr(1)):
              raise TypeError("Modulo by zero")
          return IntType()
      raise TypeError(f"Unsupported operand types for %: {left_type} and {right_type}")
    
    if op == '*':
      if self._is_number(left_type) and self._is_number(right_type):
          return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
      raise TypeError(f"Unsupported operand types for *: {left_type} and {right_type}")

    if op == '/':
      if self._is_number(left_type) and self._is_number(right_type):
          if self._is_literal_zero(ctx.expr(1)):
              raise TypeError("Division by zero")
          return FloatType()
      raise TypeError(f"Unsupported operand types for /: {left_type} and {right_type}")

  def visitPow(self, ctx: SimpleLangParser.PowContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError(f"Unsupported operand types for **: {left_type} and {right_type}")


  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for + or -: {} and {}".format(left_type, right_type))
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
