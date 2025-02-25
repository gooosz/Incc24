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

	{"code": """
		{
			{3;4;x} := 5;
			x
		}
	""",
	"expected": 5},

	{"code": """
		{
			{x; 4} := 5;
			x
		}
	""",
	"expected": Exception}
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
	"expected": 5},

	{"code": """
		{
			x := 1;
			local x:=2 in x:=4
		}
	""",
	"expected": 4},

	{"code": """
		{
			x := 1;
			local x:=2 in {
				x := 5;
				x
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
	"expected": 1},

	{"code": """
		{
			f := \(x, y, z) -> {
				if (x==1) then y+z
				else x+y
			};
			f(1,2,3) + f(0,7,4)
		}
	""",
	"expected": 12},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;

			# sum = sum + (0+1) = 1
			# sum = sum + (1+2) = 4
			# sum = sum + (2+3) = 9

			i:=0;
				sum := 0;
				while (i < 3) do {
					sum := sum + if (i==0) then plus_eins(0)
						     else if (i==1) then plus_zwei(1)
						     else plus_drei(2);
					i := i+1
				};
				sum
		}
	""",
	"expected": 9},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;

			# sum = sum + (0+1) = 1
			# sum = sum + (1+2) = 4
			# sum = sum + (2+3) = 9

			local i:=0 in {
				sum := 0;
				while (i < 3) do {
					sum := sum + if (i==0) then 1
						     else if (i==1) then 3
						     else 5;
					i := i+1
				};
				sum
			}
		}
	""",
	"expected": 9},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;

			# sum = sum + (0+1) = 1
			# sum = sum + (1+2) = 4
			# sum = sum + (2+3) = 9

			local i:=0 in {
				sum := 0;
				while (i < 3) do {
					sum := sum + if (i==0) then plus_eins(i)
						     else if (i==1) then plus_zwei(i)
						     else plus_drei(i);
					i := i+1
				};
				sum
			}
		}
	""",
	"expected": 9}

	]}

array_tests = {"expr": "ArrayExpression", "testcases": [
	{"code": """
		{
			x:=[1,4]
		}
	""",
	"expected": 2},

	{"code": """
		{
			x:=array()
		}
	""",
	"expected": 0},

	{"code": """
		{
			x:=[1];
			x[0]
		}
	""",
	"expected": 1},

	{"code": """
		{
			first_element := \(arr) -> {
				# check if arr empty
				if (arr == 0) then -1
				else arr[0]
			};
			x := [11,22,33,44,55,66,77,88,99];
			first_element(x)
		}
	""",
	"expected": 11},

	{"code": """
		{
			first_element := \(arr) -> {
				# check if arr empty
				if (arr == 0) then -1
				else arr[0]
			};
			x := [11,22,33,44,55,66,77,88,99];
			first_element(x) * first_element(y:=[])
		}
	""",
	"expected": -11},

	{"code": """
		{
			row_sum := \(arr) -> {
				sum := 0;
				i := 0;
				while (i < arr) do {
					sum := sum + arr[i];
					i := i+1
				};
				sum
			};
			x := [11, 99];
			row_sum(x)
		}
	""",
	"expected": 110},

	{"code": """
		{
			# returns sum of row in matrix
			row_sum := \(matrix, row) -> {
				row := matrix[row];
				sum := 0;
				i := 0;
				while (i < row) do {
					sum := sum + row[i];
					i := i+1
				};
				sum
			};
			x := [[1,2], [4,5]];
			row_sum(x, 0)
		}
	""",
	"expected": 3},

	{"code": """
		{
			x := 1;
			arr := [x];
			y := arr[0];
			y := 2;
			arr[0]
		}
	""",
	"expected": 1},

	{"code": """
		{
			x := 1;
			y := x;
			arr := [y];
			arr[0] := 2;
			x + y
		}
	""",
	"expected": 2},

	{"code": """
		{
			x := 1;
			arr := [x];
			x := 2;
			arr[0]
		}
	""",
	"expected": 1},

	{"code": """
		{
			x := 1;
			arr := [x];
			arr[0] := 2;
			x
		}
	""",
	"expected": 1},

	{"code": """
		{
			local arr := [2] in arr[0]
		}
	""",
	"expected": 2},

	{"code": """
		{
			arr := [1,2,3];
			size(arr)
		}
	""",
	"expected": 3},

	{"code": """
		{
			x := 1;
			local arr:=[x] in arr[0]:=2;
			x
		}
	""",
	"expected": 1},

	# Basic values are passed by copy to array
	# everything else is passed as reference

	{"code": """
		{
			arr := [1,2,3];
			brr := arr;
			brr[1] := 4;
			arr[1]
		}
	""",
	"expected": 4},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;
			arr := [plus_eins, plus_zwei, plus_drei];
			arr[0](1)
		}
	""",
	"expected": 2},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;
			arr := [plus_eins, plus_zwei, plus_drei];

			# sum = sum + (0+1) = 1
			# sum = sum + (1+2) = 4
			# sum = sum + (2+3) = 9

			i:=0;
			sum := 0;
			while (i < arr) do {
				sum := sum + arr[i](i);
				i := i+1
			};
			sum
		}
	""",
	"expected": 9},

	{"code": """
		{
			plus_eins := \(x) -> x+1;
			plus_zwei := \(y) -> y+2;
			plus_drei := \(z) -> z+3;
			arr := [plus_eins, plus_zwei, plus_drei];

			# sum = sum + (0+1) = 1
			# sum = sum + (1+2) = 4
			# sum = sum + (2+3) = 9

			local i:=0 in {
				sum := 0;
				while (i < arr) do {
					sum := sum + arr[i](i);
					i := i+1
				};
				sum
			}
		}
	""",
	"expected": 9}

	]}

# get_basic of string is pointer to C-string, so checking return value here doesn't really make sense
string_tests = {"expr": "StringExpression", "testcases": [
	{"code": """
		x := "HelloWorld!"
	""",
	"expected": "HelloWorld!"},

	{"code": """
		{
			x := "Hello World!"
		}
	""",
	"expected": "Hello World!"},

	{"code": """
		{
			x := "Hello World!";
			x
		}
	""",
	"expected": "Hello World!"},

	{"code": """
		{
			x := "Hello %s!";
			x
		}
	""",
	"expected": "Hello %s!"},

	{"code": """
		{
			f := \(x) -> x := "New string";
			x := "Hello!";
			f(x);
			x
		}
	""",
	"expected": "New string"},

	# escaping doesn't work yet
	{"code": """
		{
			x := "Multi\\nLine\\nString!";
			x
		}
	""",
	"expected": Exception}
	]}

# TODO: escaping is weird because printf somehow sees it as 2 characters instead of 1
# printf returns number of written characters (excluding \0)
printf_tests = {"expr": "printf", "testcases": [
	{"code": """
		printf("Test")
	""",
	"expected": 4},

	{"code": r"""
		printf("Test\n")
	""",
	"expected": 5},

	{"code": """
		{
			x := "World!";
			printf("Hello %s", x)
		}
	""",
	"expected": 12},

	{"code": """
		{
			x := "InCC";
			printf("%s%d course", x, 24)
		}
	""",
	"expected": 13},

	{"code": """
		{
			printf("%d %d %d %d %d", 1, 2, 3, 4, 5)
		}
	""",
	"expected": 9},

	{"code": """
		{
			printf("%d %d %d %d %d %d", 1, 2, 3, 4, 5, 6)
		}
	""",
	"expected": 9},

	{"code": """
		{
			printf("%d %d %d %d %d %d %d %d", 1, 2, 3, 4, 5, 6, 7, 8)
		}
	""",
	"expected": 15}

	]}


all_tests = [binaryexpr_tests,
	     sequence_tests,
	     globalvar_tests,
	     ite_tests,
	     while_tests,
	     loop_tests,
	     localvar_tests,
	     lambda_tests,
	     array_tests,
	     string_tests,
	     printf_tests]

