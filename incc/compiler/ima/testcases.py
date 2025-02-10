# This file contains hashmaps of different tests

# A test case for some expression is a hashmap of form testcase: {"incc code", expected result}
# all test cases on one specific expression are grouped into an dict
# {"expr": Expressionclass, "testcases": [{"code": "incc code", "expected": expected result}, ...]}

from .expr import *

ima_test = """
	3+(4*5)
"""
binaryexpr_tests = {"expr": "BinaryOperatorExpression", "testcases": [
	{"code": """
		3+(4*5)
	""",
	"expected": 23}
	]}


sequence_tests = {"expr": "SequenceExpression", "testcases": [
	{"code": """
		{
			2+3; 6*3
		}
	""",
	"expected": 18},

	{"code": """
		{
			{ 7+4 };
			19
		}
	""",
	"expected": 19},

	{"code": """
		{
			{ 7+4 };
			{ 27 }
		}
	""",
	"expected": 27}
	]}

globalvar_tests = {"expr": "VariableExpression", "testcases": [
	{"code": """
		{
			x:=2; y:=3; z:=x*y
		}
	""",
	"expected": 6},

	{"code": """
		{
			x:=2; y := { 3 } + x
		}
	""",
	"expected": 5},
	]}


ite_tests = {"expr": "ITEExpression", "testcases": [
	{"code": """
		{
			x:=2;
			y:=0;
			if (x==0) then {
				3
			} else {
				7
			}
		}
	""",
	"expected": 7}
	]}


while_tests = {"expr": "WhileExpression", "testcases": [
	{"code": """
		{
			x:=2;
			y:=0;
			while (x>=0) do {
				x := x-1
			}
		}
	""",
	"expected": -1},

	{"code": """
		{
			x:=2;
			while (x>=0) do {
				y := 1;
				while (y>0) do {
					y := y-1
				};
				x := x-1;
				y
			}
		}
	""",
	"expected": 0}
	]}


loop_tests = {"expr": "LoopExpression", "testcases": [
	{"code": """
		{
			x:=34;
			loop x do {
				x:=x+1
			}
		}
	""",
	"expected": 68}
	]}


localvar_tests = {"expr": "LocalExpression", "testcases": [
	{"code": """
		{
			local x:=2 in x
		}
	""",
	"expected": 2},

	{"code": """
		{
			local x:=2 in local y:=4 in x;
			local x:=3 in x
		}
	""",
	"expected": 3},

	{"code": """
		{
			local x:=1
			in local y:=2 in x+y
		}
	""",
	"expected": 3},

	{"code": """
		{
			local x:=1
			in {
				x + local y:=2 in x+y
			}
		}
	""",
	"expected": 4},

	{"code": """
		{
			# global and local vars with same name
			x := 10;
			local x:=1 in x+2;
			x
		}
	""",
	"expected": 10},

	{"code": """
		{
			y:=1;
			local x:=2, y:=4 in x;
			x:=3
		}
	""",
	"expected": 3},

	{"code": """
		{
			x:=1;
			local y:=2 in
			local z:=3, y:=4 in y
		}
	""",
	"expected": 4},

	{"code": """
		{
			# Using Variable prior to definition is undefined behavior because it will be seen as global and thus appear in env from start of program
			x;
			local y:=2, x:=3 in x+y
		}
	""",
	"expected": 5},

	{"code": """
		{
			# Using Variable prior to definition is undefined behavior because it will be seen as global and thus appear in env from start of program
			local y:=2, x:=3 in x+y;
			x
		}
	""",
	"expected": Exception},

	{"code": """
		x
	""",
	"expected": Exception},

	{"code": """
		local m:=10 in {
			gl := 1;
			local b:=4, q:=8 in
				local za:=5 in {
					za+m + gl
				} + b
		} * local za:=2 in za
	""",
	"expected": 40},

	{"code": """
		{
			x:=1;
			x + local y:=2, x:=3, z:=4 in x+y
		}
	""",
	"expected": 6},

	{"code": """
		{
			a := 1;
			x := 2;
			z := local y:=3, x:=4 in x*y;
			x+z
		}
	""",
	"expected": 14},

	{"code": """
		{
			local x:=2 in {
				local x:=3 in x;
				x
			}
		}
	""",
	"expected": 2},

	# INTERESTING testcase
	# because inner local expression has body { x } + x
	# because + binds stronger than IN (precedence in parser)
	{"code": """
		{
			local x:=2 in {
				local x:=3 in {
					x
				} + x
			}
		}
	""",
	"expected": 6},
	# using brackets or tmp variable fixes the problem
	{"code": """
		{
			local x:=2 in {
				(local x:=3 in {
					x
				}) + x
			}
		}
	""",
	"expected": 5},
	{"code": """
		{
			local x:=2 in {
				z := local x:=3 in {
					x
				};
				z + x
			}
		}
	""",
	"expected": 5}

	]}


lambda_tests = {"expr": "LambdaExpression", "testcases": [
	{"code": """
		{
			f := \(x) -> x+11;
			f(2)
		}
	""",
	"expected": 13},

	{"code": """
		{
			f := \(x,y) -> x+y;
			f(2,3)
		}
	""",
	"expected": 5},

	{"code": """
		{
			# TODO: y in global vector for lambda
			local y:=1 in f := \(x) -> x+y;
			f(2)
		}
	""",
	"expected": 3},

	{"code": """
		{
			y:=2;
			f := \() -> {
				y:=y+1
			};
			f()
		}
	""",
	"expected": 3},

	{"code": """
		{
			x:=2;
			f := \() -> {
				x:=5
			};
			f();
			x
		}
	""",
	"expected": 5},

	{"code": """
		{
			x:=2;
			f := \() -> {
				x:=4
			};
			f()
		}
	""",
	"expected": 4},

	{"code": """
		{
			x:=1;
			f := \(y) -> {
				local x:=5 in x;
				x:=4
			};
			f(2)
		}
	""",
	"expected": 4},

	{"code": """
		{
			x:=5;
			f := \() -> x;
			f()
		}
	""",
	"expected": 5},

	{"code": """
		{
			local gauss:=\(x) -> {
				if (x<1) then 0 else x+gauss(x-1)
			} in
			gauss(2)
		}
	""",
	"expected": 3},

	{"code": """
		{
			gauss:=\(x) -> {
				if (x<1) then 0 else x+gauss(x-1)
			};
			gauss(2)
		}
	""",
	"expected": 3},

	{"code": """
		{
			local f:=\() -> f()
			in f()
		}
	""",
	"expected": Exception},

	{"code": """
		{
			local fac := \(n) -> {
				if (n <= 1) then 1
				else n*fac(n-1)
			} in
			fac(2)
		}
	""",
	"expected": 2},

	{"code": """
		{
			fac := \(n) -> {
				if (n <= 1) then 1
				else n*fac(n-1)
			};
			fac(3)
		}
	""",
	"expected": 6},

	{"code": """
		{
			x := 1;
			f := \(z) -> z:=4;
			f(2)
		}
	""",
	"expected": 4},

	{"code": """
		{
			x := 1;
			f := \(z) -> z:=4;
			f(x);
			x
		}
	""",
	"expected": 4},


	{"code": """
		{
			f := \() -> x:=5;
			f();
			x
		}
	""",
	"expected": 5},

	{"code": """
		{
			x := 1;
			local y:=2 in {
				f := \(z) -> {
					local g := \() -> z
					in g()
				};
				f(y)
			}
		}
	""",
	"expected": 2},

	{"code": """
		{
			local x:=1 in {
				(local x := \(y) -> if (y<1) then 0 else y+x(y-1)
				in x(2)) + x
			}
		}
	""",
	"expected": 4},

	{"code": """
		{
			f := \(x) -> {
				g := \(y) -> y;
				g(2) + x
			};
			f(1)
		}
	""",
	"expected": 3},

	{"code": """
		{
			f := \() -> {
				x
			};
			x := 4;
			f()
		}
	""",
	"expected": 4},

	{"code": """
		{
			f := \() -> {
				y
			};
			local y:=4 in f()
		}
	""",
	"expected": Exception},

	{"code": """
		{
			(\(x) -> {
				x
			})(1)
		}
	""",
	"expected": 1}

	]}



all_tests = [binaryexpr_tests,
	     sequence_tests,
	     globalvar_tests,
	     ite_tests,
	     while_tests,
	     loop_tests,
	     localvar_tests,
	     lambda_tests]

