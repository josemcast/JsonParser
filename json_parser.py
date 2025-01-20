from Scanner import Scanner
from Parser import Parser
import sys
import pprint


def run(filename: str):

    if filename.lower().endswith(".json"):
        input = ""
        with open(filename, 'r') as file:
            input = "".join(file.readlines())

        scanner = Scanner(input)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        obj = parser.parser()

        pprint.pp(obj)

    else:
        print(filename)


def repl():

    if len(sys.argv) < 1:
        print("Usage: python3 parser_json file_name.json")
        sys.exit(1)

    run(sys.argv[1])


if __name__ == "__main__":
    repl()
