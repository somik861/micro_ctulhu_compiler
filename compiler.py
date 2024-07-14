from argparse import ArgumentParser
from pathlib import Path

import examples.example_ast as example_ast
from src.CommandFactory import CommandFactory
from src.Environment import Environment


def main() -> None:
    parser = ArgumentParser()
    # parser.add_argument('source_code', type=Path, help='Source code in yaml or json.')
    parser.add_argument('output_code', type=Path, help='Where to output ctulhu code.')
    
    args = parser.parse_args()
    
    ast = example_ast.get_add_ast()
    
    res = ast.compile(Environment(), CommandFactory())
    with open(args.output_code, 'w', encoding='utf-8') as f:
        for line in res.code:
            f.write(f'{line}\n')

    print(f'{len(res.code)} line written')

if __name__ == '__main__':
    main()