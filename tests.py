from incc.language.lexer.proc_expr import *
from ply.lex import lex
from incc.language.parser.proc_expr import *
from ply.yacc import yacc
from incc.language.parser.program_expr import *
from incc.language.parser.code_generation import set_generator_module


from incc.compiler.ima.x86_64 import to_x86_64, x86_program
from incc.compiler.ima import expr
from incc.compiler.ima import optimizations
set_generator_module(expr)        # where to find Expression classes

import argparse
import os
import copy
import subprocess

# testcases
from incc.compiler.ima.testcases import *

def compileCode(code, args):
        env = {}
        lexer = lex()
        parser = yacc(start='program')

        ast = parser.parse(lexer=lexer, input=code)

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


        # TODO: after constant folding + propagating it makes sense to do dead code elimination so unused variables will get deleted
        #       so the program result can be calculated at compile time and contains nothing more
        if args.O1 or args.deadcodeelimination:
                # TODO: doesn't eliminate all
                ast = optimizations.deadCodeElimination(ast)


        file = args.output
        code_ir = ast.code_b(env, 0)  # always generate intermediate representation, but write only to file if specified by cma/mama flag
        print(f"main env: {env}")
        match args.ir:
                case 'cma':
                        # write cma code to file
                        with open(f"./{file}.cma","w") as cma_code:
                                cma_code.write(code_ir)
                case 'mama':
                        # write mama code to file
                        with open(f"./{file}.mama","w") as mama_code:
                                mama_code.write(code_ir)
                case 'ima':
                        # write ima code to file
                        with open(f"./{file}.ima","w") as ima_code:
                                ima_code.write(code_ir)
        # because we are running testcases: always create asm + exe files
        code_x86  = to_x86_64(code_ir, env)
        with open(f"./{file}.s","w") as program_code:
                program_code.write(x86_program(code_x86, env))

        # generate object file
        os.system(f"nasm -f elf64 {file}.s -g -F dwarf")

        # generate executable
        os.system(f"gcc -o {file} {file}.o -no-pie -ggdb -gdwarf")


def runExecutable(executable):
        # run the executable and return the output
        return int(subprocess.check_output(f"./{executable}", stderr=subprocess.STDOUT, shell=True))

def runTests(args):
        for exprtests in all_tests:
                # exprtests is a dict {"expr": Expressionclass, "testcases": [{"code": "incc code", "expected": expected result}, ...]}
                # run each testcase and compare with expected result
                # if not the same => stop and show detailed output
                # if list of expressions to test is specified/not empty => only tests those
                if not args.e or str(exprtests['expr']) in args.e:
                        print(f"=== Testing {exprtests['expr']} ===")
                        for i, testcase in enumerate(exprtests['testcases']):
                                # -e Expression -t 1 only runs testcase nr.1 of testcases of Expression
                                if args.t and str(i) not in args.t:
                                        continue;
                                code = testcase['code']
                                expected = testcase['expected'] # can be result of code or thrown exception

                                if expected is Exception:
                                        # test if an Exception (for now any Exception) is thrown
                                        try:
                                                compileCode(code, args)
                                                output = runExecutable(args.output)
                                                if type(output) is not type(expected):
                                                        print(f"Error at index {i} in {exprtests['expr']}: {code} has output {output}, but should be {expected}")
                                                        return
                                        except:
                                                # correct result, exception got thrown
                                                print(f"Testcase {i} passed✅")
                                else:
                                        # test normal result value
                                        compileCode(code, args)

                                        try:
                                                output = runExecutable(args.output)
                                        except subprocess.CalledProcessError as e:
                                                # error when running executable, mostly segfault
                                                print(f"{exprtests['expr']} {i}: {code}")
                                                raise e

                                        if output != expected:
                                                print(f"Error at index {i} in {exprtests['expr']}: {code} has output {output}, but should be {expected}")
                                                return
                                        else:
                                                # correct result
                                                print(f"Testcase {i} passed✅")


"""
flags specify:
--cma: .incc24 -> .cma                  - writes cma code to file from incc24
--asm: .cma    -> .s                    - writes assembly code to file from cma
--obj: .s      -> .o                    - writes object file to file from assembly
--exe: .o      -> binary executable     - generates executable from object file
You can chain the different steps together like --cma --obj will generate all files from incc24 to object file
"""

"""def addOptimizationFlags(argparser):
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

    # for running only specific testcases
    argparser.add_argument('-e', nargs='+', help='Test only specific expression')
    argparser.add_argument('-t', nargs='+', help='Test only specific testcases no.')


    args = argparser.parse_args()
    print(f"-- {args.e}")
    #main(args)
    runTests(args)"""

