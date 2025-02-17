from .expr import *

# Optimizations

"""
 Optimizations that take advantage of and change the Parse Tree
 such as Constant Folding
"""
def constantFolding(ast: CompiledExpression):
	# check parse tree recursively if constant foldable
	notAConstant = [VariableExpression] 	# list of all Expressions that are no constants, where no recusive call to fold should happen
	aConstant = [SelfEvaluatingExpression, int]
	# every Expression that is neither in notAConstant nor aConstant may be constant foldable
	match ast:
		case ProgramExpression(body):
			return constantFolding(body)
		case BinaryOperatorExpression(e1, op, e2):
			# replace expression by SelfEvaluatingExpression containing the calculated constant
			print(f"--folding {ast}")
			if type(e1) not in notAConstant and type(e2) not in notAConstant:
				e1 = constantFolding(e1)	# need to recursively fold the children
				e2 = constantFolding(e2)
				# can only calculate if e1 and e2 are now constants,
				# else it only folded the children of binary operator which is fine
				if type(e1) is SelfEvaluatingExpression and type(e2) is SelfEvaluatingExpression:
					foldedconstant = operators[op][1](e1.id, e2.id) # calculate the result of operand
					ast = SelfEvaluatingExpression(foldedconstant)
			return ast
		case SelfEvaluatingExpression(num):
			return ast # constant found, yippie
		case SequenceExpression(seq):
			# try to do constant folding on all elements of sequence
			#return SequenceExpression([constantFolding(expr) if type(expr) not in notAConstant else expr for expr in seq])
			folded_seq = []
			for i, expr in enumerate(seq):
				# expr itself must not be a constant, but only can be folded into one or else Expression object disappears
				if type(expr) not in notAConstant + aConstant:
					folded_seq.append(constantFolding(expr)) # update all entries to the folded expression
				else:
					folded_seq.append(expr)
			return SequenceExpression(folded_seq)
		case AssignmentExpression(var, val):
			if type(val) not in notAConstant + aConstant:
				ast = AssignmentExpression(var, constantFolding(val))
			return ast # try folding value of assignment
		case VariableExpression(name):
			# this shouldn't match because VariableExpression is in notAConstant list, so recursive call with this should not happen
			class VariableIsNotAConstant(Exception):
				pass
			raise VariableIsNotAConstant()
		case _:
			return ast # no constant, expression stays the same


# propagate constants
# check for constants in new field in env ['const': None] default or the value directly
def constantPropagation(ast: CompiledExpression):
	match ast:
		case ProgramExpression(body):
			return constantPropagation(body)
		case BinaryOperatorExpression(e1, op, e2):
			e1 = constantPropagation(e1)
			e2 = constantPropagation(e2)
			return BinaryOperatorExpression(e1, op, e2)
		case SelfEvaluatingExpression(num):
			return ast # constant found, yippie
		case SequenceExpression(seq):
			for i, expr in enumerate(seq):
				if type(expr) is AssignmentExpression and type(expr.value) is SelfEvaluatingExpression:
					# search next expression that has expr in it
					# and replace by SelfEvaluatingExpression value of variable
					for j in range(i+1, len(seq)):
						try:
							seq[j] = constPropReplaceIn(seq[j], expr)
						except VariableOverwritten:
							break	# variable got overwritten so stop propagating this variable
			return ast
		case AssignmentExpression(var, val):
			val = constantPropagation(val)
			return AssignmentExpression(var, val)
		case VariableExpression(name):
			# plain variable should only happen later in sequence (after some assignment), so case makes only sense in constPropReplaceIn
			raise ThisShouldNotHappen()
		case _:
			return ast # no constant, expression stays the same

# search next expression that has expr in it
# and replace by SelfEvaluatingExpression value of variable
# gets thrown by constPropReplaceIn in case the variable holding const got overwritten
class VariableOverwritten(Exception):
	pass

class ThisShouldNotHappen(Exception):
	pass

# this helper is called by constantPropagation and replaces each VariableExpression with same name as const name by the value
def constPropReplaceIn(ast: CompiledExpression, const: AssignmentExpression):
	match ast:
		case BinaryOperatorExpression(e1, op, e2):
			e1 = constPropReplaceIn(e1, const)
			e2 = constPropReplaceIn(e2, const)
			return BinaryOperatorExpression(e1, op, e2)
		case SelfEvaluatingExpression(num):
			return ast # stays the same
		case SequenceExpression(seq):
			propagated_seq = []
			for i, expr in enumerate(seq):
				try:
					propagated_seq.append(constPropReplaceIn(expr, const))
				except VariableOverwritten:
					break	# variable got overwritten so stop propagating this variable
			return SequenceExpression(propagated_seq)
		case AssignmentExpression(var, val):
			# check if const got overwritten
			if var.name == const.var.name:
				# stop propagating current const because got overwritten
				raise VariableOverwritten()
			else:
				val = constPropReplaceIn(val, const)
				return AssignmentExpression(var, val) # i dont understand python but returning ast doesnt update val, so must construct new object
		case VariableExpression(name):
			if name == const.var.name:
				print(f"--propagating {ast} by {const.value}")
				ast = const.value # replace single variable by constant
			return ast
		case _:
			print(f"no match for {ast}?")
			return ast # no constant, expression stays the same

"""
 Optimizations that optimize the intermediate representation
 such as Dead Code Elimination
"""
# TODO: chomsky nutzlose variables entfernen Algorithmus anschauen
def deadCodeElimination(ast: CompiledExpression):
	# TODO: globale Variables sind an keinen scope gebunden, können mitten im Baum vorkommen: {x:=4;5}+{x} ist valid weil x global
	match ast:
		case ProgramExpression(body):
			body = deadCodeElimination(body)
			return ProgramExpression(body)
		case BinaryOperatorExpression(e1, op, e2):
			e1 = deadCodeElimination(e1)
			e2 = deadCodeElimination(e2)
			return BinaryOperatorExpression(e1, op, e2)
		case SelfEvaluatingExpression(num):
			return ast # constant found, yippie
		case SequenceExpression(seq):
			# need to loop over a copy of seq or else removing element in loop causes weird side effects for iterators
			seqcopy = seq[:]
			# last expression is automatically alive because it's output of program
			# get all used expressions in last expression
			# if last expression in list is assignment, replace it by it's value because no expression comes after last one so variable unused except value as return of program
			if type(seq[-1]) is AssignmentExpression:
				print(f"--replacing unused {seq[-1].var} by it's value {seq[-1].value}")
				seq[-1] = seq[-1].value
			aliveExprs = gatherAlive(seq[-1])
			# gather recursively in last expression in sequence all used expressions
			# after that go through list backwards and delete everything unused/dead
			for i, expr in reversed(list(enumerate(seqcopy))):
				# only remove if not used and not last expression
				if i < len(seq)-1:
					match expr:
						case AssignmentExpression(var, val):
							# in every alive variable check the assigment of variable again if there are used/alive expressions
							if var in aliveExprs:
								aliveExprs += gatherAlive(val)
							if var not in aliveExprs and val not in aliveExprs:
								print(f"--eliminating dead {expr} at {i}")
								# because we traverse the list in reverse doing a pop in loop is okay
								# because the changed indices due to pop only affect indices after expr
								# but they were already looked at in previous iteration because reverse
								seq.pop(i)
						case _:
							# delete everything else
							print(f"--2 eliminating dead {expr}  at {i}")
							seq.pop(i)
			print(f"gatherAlive: {aliveExprs}")
			return SequenceExpression(seq)
		case AssignmentExpression(var, val):
			val = deadCodeElimination(val)
			return AssignmentExpression(var, val)
		case _:
			return ast # expression stays the same

# returns a list of all alive expressions recursively in ast
def gatherAlive(ast: CompiledExpression) -> list[CompiledExpression]:
	match ast:
		case BinaryOperatorExpression(e1, op, e2):
			return gatherAlive(e1) + gatherAlive(e2)
		case SelfEvaluatingExpression(num):
			return [] # constant is already in expression, so no previous expression that has to be kept alive is here
		case SequenceExpression(seq):
			# go through seq backwards and gather all in every element recursively
			#  TODO: this doesn't work currently for multiple reasons:
			#			- if last expression in loop is assignment, the assignment is replaced by value
			#			  which changes semantics in a decrementing loop
			#			- the last expression is always alive because it' the return value of the sequence in loop,
			#			  and it optimizes a loop only away if aliveExprs is empty, which thus is never the case
			if type(seq[-1]) is AssignmentExpression:
				# TODO: dont do this if last expression is while with variable assign else infinite loop => semantics changed
				print(f"--replacing unused {seq[-1].var} by it's value {seq[-1].value}")
				seq[-1] = seq[-1].value
			aliveExprs = gatherAlive(seq[-1])
			# skip last expression in loop because already gathered
			for expr in reversed(seq[:-1]):
				match expr:
					case AssignmentExpression(var, val):
						# in every alive variable check the assigment of variable again if there are used/alive expressions
						if var in aliveExprs:
							aliveExprs += gatherAlive(val)
			return aliveExprs
		case AssignmentExpression(var, val):
			return gatherAlive(val)
		case ITEExpression(cond, ifbody, elsebody):
			return gatherAlive(cond) + gatherAlive(ifbody) + gatherAlive(elsebody)
		case WhileExpression(cond, body):
			aliveExprs  = gatherAlive(cond)
			aliveExprs += gatherAlive(body)
			if aliveExprs:
				# list not empty => alive expressions in while, so keep while expression
				aliveExprs += [ast]
			return aliveExprs
		case LoopExpression(loopvar, body):
			raise NotImplementedError()
		case _:
			return [ast] # expression needs to be kept alive



# returns true if expr is not contained in ast
# expr only makes sense for variables right now
# everything else gets constant folded/propagated
def isDeadIn(ast: CompiledExpression, expr: VariableExpression):
	#print(f"expr {expr}")
	match ast:
		case BinaryOperatorExpression(e1, op, e2):
			print(f"isDeadIn(e1, expr) = {isDeadIn(e1, expr)}")
			print(f"isDeadIn(e2, expr) = {isDeadIn(e2, expr)}")
			return isDeadIn(e1, expr) and isDeadIn(e2, expr)
		case SelfEvaluatingExpression(num):
			return True
		case SequenceExpression(seq):
			is_expr_dead = True
			for i, nextexpr in enumerate(seq):
				# search if expr is somewhere in seq
				is_expr_dead = is_expr_dead and isDeadIn(nextexpr, expr)
			return is_expr_dead
		case AssignmentExpression(var, val):
			# left side of assignment doesn't matter because new value assigned
			print(f"val {val}")
			return isDeadIn(val, expr)
		case VariableExpression(name):
			print(f"ast {ast}, expr {expr}")
			if type(expr) is VariableExpression and name == expr.name:
				return False
			return True
		case _:
			return True # not found
