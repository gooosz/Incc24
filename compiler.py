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

# testcases
from tests import *

def main(args):
        env = {}
        lexer = lex()
        parser = yacc(start='program')

        with open(args.srcfile, 'r') as incc_file:
                incc_code = incc_file.read()
                ast = parser.parse(lexer=lexer, input=incc_code)

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


        # after constant folding + propagating it makes sense to do dead code elimination so unused variables will get deleted
        # so the program result can be calculated at compile time and contains nothing more
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

        if args.asm or args.obj or args.exe:
                # write asm code to file
                code_x86  = to_x86_64(code_ir, env)
                with open(f"./{file}.s","w") as program_code:
                        program_code.write(x86_program(code_x86, env))

        #if args.obj or args.exe:
        # generate object file
        os.system(f"nasm -f elf64 {file}.s -g -F dwarf")

        #if args.exe or all(arg is None for arg in vars(args).values()):
        # generate executable
        os.system(f"gcc -o {file} {file}.o -no-pie -ggdb -gdwarf")


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

        # decide between compiling a file or running testcases
        subparsers = argparser.add_subparsers(required=True, dest='action', help='Choose what to do')

        compile_args = subparsers.add_parser('c', help='Compile a file')
        compile_args.add_argument('--ir', type=str, choices=['cma', 'mama', 'ima'], default='ima', help='Set intermediate representation')

        compile_args.add_argument('--asm', action='store_true', help='Create assembly code')
        compile_args.add_argument('--obj', action='store_true', help='Create object file')
        compile_args.add_argument('--exe', action='store_true', help='Create executable')
        compile_args.add_argument('-o', type=str, dest='output', default="example1", help='Set ouput file')
        compile_args.add_argument('srcfile', type=str, help='The file to compile')
        addOptimizationFlags(compile_args)

        testcase_args = subparsers.add_parser('t', help='Run testcases')
        testcase_args.add_argument('--ir', type=str, choices=['cma', 'mama', 'ima'], default='ima', help='Set intermediate representation')
        testcase_args.add_argument('-o', type=str, dest='output', default="example2", help='Set ouput file')
        # for running only specific testcases
        testcase_args.add_argument('-e', nargs='+', help='Test only specific expression')
        testcase_args.add_argument('-t', nargs='+', help='Test only specific testcases no.')
        addOptimizationFlags(testcase_args)

        args = argparser.parse_args()
        print(f"args: {args}")

        match args.action:
                case 'c':
                        # Compile a file
                        main(args)
                case 't':
                        # Run testcases
                        runTests(args)
