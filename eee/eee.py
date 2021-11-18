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
            "\\/\\*[\\s\\S]*\\*\\/", " ", file
        )  # replace multiline comments wit ha " "
        file = re.sub("\\/\\/.+$", " ", file)  # replace comments wit ha " "

        lines = file.split("\n")

        multi_line_comment_in_progress = False
        word_dividers = ("(", ")", ",", "{", "}", "[", "]", ";", "*", "/", "+", "-")

        # single line comments and empty lines
        while len(lines) > 0:
            line = lines[0]
            print(line)

            # wider
            for orig, expanded in [
                (word_divider, f" {word_divider} ") for word_divider in word_dividers
            ]:
                if '"' not in line and "'" not in line:
                    line = line.replace(orig, expanded)
                else:
                    l_i_n_e = list(line)
                    line = ""
                    string = ""
                    in_str = False
                    for letter in l_i_n_e:
                        if letter == '"':
                            in_str = not in_str
                            if not in_str:
                                preprocessor_defines[e_len * LETTER] = f'{string}"'
                                line += f" {e_len * LETTER} "
                                e_len += 1
                                string = ""
                        if not in_str:
                            if letter in word_dividers:
                                line += f" {letter} "
                            else:
                                line += letter
                        else:
                            string += letter

            if line.startswith("#"):
                code += line
            if line == "\n":
                code += line

            del lines[0]

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
