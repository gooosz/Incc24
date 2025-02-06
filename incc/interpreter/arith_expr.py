import operator

bin_operators = {'+': operator.add,
                 '-': operator.sub,
                 '*': operator.mul,
                 '/': operator.floordiv,
                 }
unary_operators = {'-': operator.neg,
                   }


class InterpretedExpression:
    def eval(self, env):
        raise Exception('eval unimplemented')

class SelfEvaluatingExpression(InterpretedExpression):
    def __init__(self, e1):
        self.e1 = e1

    def eval(self, env):
        return (self.e1, env)

class ProgramExpression(InterpretedExpression):
    def __init__(self, e):
        self.e = e
    def eval(self, env):
        return self.e.eval(env)

class BinaryOperatorExpression(InterpretedExpression):
    def __init__(self, e1, op, e2):
        self.e1 = e1
        self.op = op
        self.e2 = e2
    def eval(self, env):
        x, env1 = self.e1.eval(env)
        y, env2 = self.e2.eval(env1)
        return (bin_operators[self.op](x,y), env2)

class UnaryOperatorExpression(InterpretedExpression):
    def __init__(self, op, e1):
        self.e1 = e1
        self.op = op
    def eval(self, env):
        x , env1 = self.e1.eval(env)
        return (unary_operators[self.op](x), env1)

