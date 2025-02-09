# Compiler for InCC24

## Language specifics

Here are some features of the InCC24 programming language:

- multiparadigm: imperative, functional
- currently: only supports printing out integer result of program (no prior printing, string, data structures, etc.)

BNF of InCC24: <br/>
A program consists of \< ProgramExpression \> <br/>
where

- ProgramExpression ::= \< Expression \>
- SelfEvaluatingExpression ::= \< CONSTANT \>
- BinaryOperatorExpression ::= \< Expression \> \< OPERATOR \> \< Expression \>
- SequenceExpression ::= { \< ExpressionList \> }
- VariableExpression ::= \< STRING \>
- AssignmentExpression ::= \< VariableExpression \> := \< Expression \>
- ITEExpression ::= if (\< Expression \>) then \< Expression \> \[ else \< Expression \> \]
- WhileExpression ::= while (\< Expression \>) do \< Expression \>
- LoopExpression ::= loop \< Expression \> do \< Expression \>
- LocalExpression ::= local \< AssignmentList \> in \< Expression \>
- CallExpression ::= \< Expression \>( \< ParameterList \> )
- LambdaExpression ::= \\ ( \< VariableList \> ) -> \< Expression \>
		| \\ \< VariableList \> -> \< Expression \>
- Expression ::= \< SelfEvaluatingExpression \>
	       | \< BinaryOperatorExpression \>
	       | \< SequenceExpression \>
	       | \< VariableExpression \>
	       | \< AssignmentExpression \>
	       | \< ITEExpression \>
	       | \< WhileExpression \>
	       | \< LoopExpression \>
	       | \< LocalExpression \>
	       | \< CallExpression \>
	       | \< LambdaExpression \>

	       
- CONSTANT ::= 0 | ... | 9 | 0\< CONSTANT \> | ... | 9\< CONSTANT \>
- OPERATOR ::= + | - | * | / | \< | \> | <= | >= | == | !=
- ExpressionList ::= \< Expression \> | \< Expression \> ; \< ExpressionList \>
- STRING ::= 
- AssignmentList ::= \< STRING \> := \< Expression \> | \< STRING \> := \< Expression \> , \< AssignmentList \>
- ParameterList ::= \< Expression \> | \< Expression \> , \< ParameterList \>
- VariableList ::= \< STRING \> | \< STRING \> , \< VariableList \>

