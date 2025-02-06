from incc.language.lexer.proc_expr import *
from ply.lex import lex
from incc.language.parser.proc_expr import *
from ply.yacc import yacc
from incc.language.parser.program_expr import *
#from incc.language.parser.arith_expr import arith_expr_yacc
from incc.language.parser.code_generation import set_generator_module

### === CMA ===
#from incc.compiler.cma.x86_64 import to_x86_64, x86_program
#from incc.compiler.cma import arith_expr
#set_generator_module(arith_expr)        # where to find Expression classes
### === MaMA ===
#from incc.compiler.mama.x86_64 import to_x86_64, x86_program
#from incc.compiler.mama import arith_expr
#set_generator_module(arith_expr)        # where to find Expression classes
### === IMa ===
from incc.compiler.ima.x86_64 import to_x86_64, x86_program
from incc.compiler.ima import expr
from incc.compiler.ima import optimizations
set_generator_module(expr)        # where to find Expression classes

import argparse
import os
import copy

def main(args):
        rho = {}
        lexer = lex()
        parser = yacc(start='program')
        ima_test = """
                3+(4*5)
        """
        ima_seq = """
        {
                2+3; 6*3
        }
        """
        ima_globalvar = """
        {
                x:=2; y:=3; z:=x*y
        }
        """
        ima_constantfolding = """
        {
                x:=3*6; y:=2*x
        }
        """
        ima_constantpropagating = """
        {
                x:=3; y:=x*2; z:=y+x
        }
        """
        ima_deadcodeelimination = """
        {
                x:=2; y:=3+x; z:=y
        }

        """
        ima_deadcodeelimination2 = """
        {
                x:=2; y:=x*2; 7
        }

        """
        ima_ite = """
        {
                x:=2;
                y:=0;
                if (x==0) then {
                        3
                } else {
                        7
                }
        }

        """
        ima_while = """
        {
                x:=2;
                y:=0;
                while (x>=0) do {
                        x := x-1
                }
        }

        """
        ima_while2 = """
        {
                x:=2;
                while (x>=0) do {
                        y := 1;
                        while (y>=0) do {
                                y := y-1
                        };
                        x * 10
                }
        }

        """
        ima_loop = """
        {
                x:=34;
                loop x do {
                        x:=x+1
                }
        }

        """
        ima_local = """
        {
                local x:=2 in x
        }
        """
        bug_ima_local2 = """
        {
                local x:=1
                in local y:=2 in x+y
        }
        """
        bug_ima_local3 = """
        {
                local x:=1
                in {
                        x + local y:=2 in x+y
                }
        }
        """
        ima_lambda = """
        {
                # TODO: y in global vector for lambda
                local y:=1 in f := \(x) -> x+y;
                f(2)
        }
        """
        ima_lambda2 = """
        {
                y:=2;
                f := \() -> {
                        x:=y+1
                };
                f()
        }
        """
        ima_lambda3 = """
        {
                f := \(y) -> {
                        local x:=5 in x;
                        x:=4
                };
                f(2)
        }
        """
        ima_lambda4 = """
        {
                f := \() -> {
                        x:=4
                };
                f()
        }
        """
        ima_lambda5 = """
        {
                x:=5;
                f := \() -> x;
                f()
        }
        """
        ima_lambda6_fac = """
        {
                local fac := \(n) -> {
                        if (n <= 1) then 1
                        else n*fac(n-1)
                } in
                fac(2)
        }
        """
        ast = parser.parse(lexer=lexer, input=ima_lambda2)

        if args.O1 or args.constantfolding:
                # apply constant folding
                ast = optimizations.constantFolding(ast)
        if args.O1 or args.constantpropagation:
                ast = optimizations.constantPropagation(ast)

        if args.O1:
                # only if O1 is specified do folding + propagating in a loop
                old_ast = copy.deepcopy(ast)
                ast = optimizations.constantPropagation(ast)
                # run constant folding again because currently language only can do integer and variables
                # so by doing constant folding -> propagating -> folding
                # we achieve the result of the program at compile time
                ast = optimizations.constantFolding(ast)
                # apply constant propagation + fold until no changes happen
                # doesn't cause infinite loop because folding makes parse tree size smaller or equal
                #                                    propagating keeps parse tree size the same
                #                                    => converges to something, so no infinite loop
                while ast != old_ast:
                        old_ast = copy.deepcopy(ast)
                        ast = optimizations.constantPropagation(ast)
                        ast = optimizations.constantFolding(ast)

        # TODO: keine Prozeduren, Lambdas sind das einzige an Funktionen

        # quit/break for iterators
        # e.g.
        #       f() {
        #               break;
        #       }
        #       for i in ...:
        #               f()
        # call f in loop breaks the loops
        #


        # TODO: after constant folding + propagating it makes sense to do dead code elimination so unused variables will get deleted
        #       so the program result can be calculated at compile time and contains nothing more
        if args.O1 or args.deadcodeelimination:
                # TODO: doesn't eliminate all
                ast = optimizations.deadCodeElimination(ast)


        file = "example1"
        code_ir = ast.code_b(rho)  # always generate intermediate representation, but write only to file if specified by cma/mama flag
        print(f"env: {rho}")
        if args.cma:
                # write cma code to file
                with open(f"./{file}.cma","w") as cma_code:
                        cma_code.write(code_ir)
        if args.mama:
                # write mama code to file
                with open(f"./{file}.mama","w") as mama_code:
                        mama_code.write(code_ir)
        if args.ima:
                # write ima code to file
                with open(f"./{file}.ima","w") as ima_code:
                        ima_code.write(code_ir)

        # optimize on intermediate representation
        if args.optimizeir:
                pass
        
        if args.asm or args.obj or args.exe:
                # write asm code to file
                code_x86  = to_x86_64(code_ir, rho)
                with open(f"./{file}.s","w") as program_code:
                        program_code.write(x86_program(code_x86,rho))

        if args.obj or args.exe:
                # generate object file
                os.system(f"nasm -f elf64 {file}.s -g -F dwarf")

        if args.exe or all(arg is None for arg in vars(args).values()):
                # generate executable
                os.system(f"gcc -o {file} {file}.o -no-pie -ggdb -gdwarf")
        #print(f"env: {global_env(env)}")
        


"""
flags specify:
--cma: .incc24 -> .cma                  - writes cma code to file from incc24
--asm: .cma    -> .s                    - writes assembly code to file from cma
--obj: .s      -> .o                    - writes object file to file from assembly
--exe: .o      -> binary executable     - generates executable from object file
You can chain the different steps together like --cma --obj will generate all files from incc24 to object file
"""

def addOptimizationFlags(argparser):
        argparser.add_argument('-O1', action='store_true', help='local optimizations, such as constantfolding')
        argparser.add_argument('-O2', action='store_true', help='global optimizations')
        argparser.add_argument('--optimizeir', action='store_true', help='Optimize intermediate representation')

        argparser.add_argument('--constantfolding', action='store_true', help='Apply optimization constant folding')
        argparser.add_argument('--constantpropagation', action='store_true', help='Apply optimization constant propagation')
        argparser.add_argument('--deadcodeelimination', action='store_true', help='Apply optimization dead code elimination')



if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog='compiler', description='Run the compiler')
    # argparser.add_argument('file', type=str, nargs='?', help='The file to compile')
    argparser.add_argument('--cma', action='store_true', help='Create C-Machine code')
    argparser.add_argument('--mama', action='store_true', help='Create Maurer-Machine code')
    argparser.add_argument('--ima', action='store_true', help='Create IMa code')
    argparser.add_argument('--asm', action='store_true', help='Create assembly code')
    argparser.add_argument('--obj', action='store_true', help='Create object file')
    argparser.add_argument('--exe', action='store_true', help='Create executable')
    addOptimizationFlags(argparser)

    args = argparser.parse_args()
    main(args)
