from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text

    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
      self.errors.append(f"Unsupported operand types for {op}: {left_type} and {right_type}")
      return
    
    if op == '%':
        if isinstance(left_type, IntType) and isinstance(right_type, IntType):
            if self._is_literal_zero(ctx.expr(1)):
                self.errors.append("Modulo by zero")
            self.types[ctx] = IntType()
        else:
            self.errors.append(f"Unsupported operand types for %: {left_type} and {right_type}")
        return
    

    if op == '*':
        if self._is_number(left_type) and self._is_number(right_type):
            self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
        else:
            self.errors.append(f"Unsupported operand types for *: {left_type} and {right_type}")
        return

    if op == '/':
        if self._is_number(left_type) and self._is_number(right_type):
            if self._is_literal_zero(ctx.expr(1)):
                self.errors.append("Division by zero")
            self.types[ctx] = FloatType()
        else:
            self.errors.append(f"Unsupported operand types for /: {left_type} and {right_type}")
        return

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    op = ctx.op.text

    if op == '+' and isinstance(left_type, StringType) and isinstance(right_type, StringType):
        self.types[ctx] = StringType()
        return
    
    if isinstance(left_type, BoolType) or isinstance(right_type, BoolType):
        self.errors.append(f"Unsupported operand types for {op}: {left_type} and {right_type}")
        return
    

    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def exitPow(self, ctx: SimpleLangParser.PowContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
        self.errors.append(f"Unsupported operand types for **: {left_type} and {right_type}")
        return

    if isinstance(left_type, IntType) and isinstance(right_type, IntType):
        if isinstance(ctx.expr(1), SimpleLangParser.IntContext):
            self.types[ctx] = IntType()
            return
    self.types[ctx] = FloatType()
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def _is_number(self, t):
    return isinstance(t, (IntType, FloatType))
  
  def _is_literal_zero(self, expr_ctx):
    from SimpleLangParser import SimpleLangParser
    if isinstance(expr_ctx, SimpleLangParser.IntContext):
        return expr_ctx.getText() == '0'
    if isinstance(expr_ctx, SimpleLangParser.FloatContext):
        try:
            return float(expr_ctx.getText()) == 0.0
        except:
            return False
    return False

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
