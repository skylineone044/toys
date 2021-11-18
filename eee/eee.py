#!/bin/env python3

import sys
import re

LETTER = "e"


def parse(inputFileName: str) -> str:
    tokens = {}
    e_len = 1

    code: str = ""
    preprocessor_defines: str = {}

    with open(inputFileName, "r") as inputFile:
        file = inputFile.read()
        file = re.sub(
            "\\/\\*[\\s\\S]*\\*\\/", "\n", file
        )  # replace multiline comments wit ha " "
        file = re.sub("\\/\\/.+$", "\n", file)  # replace comments wit ha " "

        stringMatcher = re.compile("\".*?\"")

        lines = file.split("\n")

        word_dividers = ("(", ")", ",", "{", "}", "[", "]", ";", "*", "/", "+", "-")

        # single line comments and empty lines
        while len(lines) > 0:
            line = lines[0]

            # wider
            for orig, expanded in [
                (word_divider, f" {word_divider} ") for word_divider in word_dividers
            ]:
                if '"' not in line and "'" not in line:
                    line = line.replace(orig, expanded)
                else:
                    while '"' in line:
                        strings = stringMatcher.findall(line)
                        for string in strings:
                            preprocessor_defines[e_len * LETTER] = string
                            line = line.replace(string, e_len * LETTER)
                            e_len += 1


            if line.startswith("#"):
                code += line
            if line == "\n":
                code += line

            del lines[0]
            print(line)

    print(str(preprocessor_defines))
    return code


if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if inputFileName == outputFileName:
        print("No overwriting")
        exit(1)

    with open(outputFileName, "w") as outputFile:
        outputFile.write(parse(inputFileName))
