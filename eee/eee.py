#!/bin/env python3

import sys
import re

LETTER = "e"


def parse(inputFileName: str) -> str:
    e_len = 1

    code: str = ""
    preprocessor_defines: dict = {}

    with open(inputFileName, "r") as inputFile:
        file = inputFile.read()
        file = re.sub(
            "\\/\\*[\\s\\S]*\\*\\/", "\n", file
        )  # replace multiline comments with a "\n"
        file = re.sub("\\/\\/.*", "\n", file)  # replace comments with a "\n"

        stringMatcher = re.compile('".*?"')

        lines = file.split("\n")

        word_dividers = (
            "(",
            ")",
            ",",
            "{",
            "}",
            "[",
            "]",
            ";",
            "*",
            "/",
            "+",
            "-",
            "<<",
            ">>",
            "<",
            ">",
            "==",
            "=",
            ">=",
            "<=",
        )
        wide_word_dividers = ("<<", ">>", "==", ">=", "<=")

        dividers = "([\\[\\]{}(),;*-+<>=]{1,2})"

        # single line comments and empty lines
        while len(lines) > 0:
            line = lines[0]

            if line.startswith("#"):
                code += line + "\n"
                del lines[0]
                continue

            # wider
            for orig, expanded in [
                (word_divider, f" {word_divider} ") for word_divider in word_dividers
            ]:
                if '"' not in line and "'" not in line:
                    divider_locations = re.search(dividers, line)
                    if divider_locations is not None:
                        line = line.replace(
                            divider_locations.group(0),
                            f" {divider_locations.group(0)} ",
                        )
                else:
                    while '"' in line:
                        strings = stringMatcher.findall(line)
                        for string in strings:
                            preprocessor_defines[string] = e_len * LETTER
                            line = line.replace(string, e_len * LETTER)
                            e_len += 1
                            line = line.replace(orig, expanded)

            for word in line.split(" "):
                if word != "":
                    if word in preprocessor_defines.keys():
                        line = line.replace(word, preprocessor_defines[word])
                    else:
                        line = line.replace(word, e_len * LETTER)
                        preprocessor_defines[word] = e_len * LETTER
                        e_len += 1
            if line == "\n":
                code += line

            line = re.sub("[ \t]{2,}", " ", line)
            code += line
            del lines[0]

    defines = "".join([f"#define {e} {word}\n" for word, e in preprocessor_defines.items()])
    code = code.split("\n")[0] + "\n" + defines + code.split("\n")[1]

    # print(str(preprocessor_defines))
    return code


if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if inputFileName == outputFileName:
        print("No overwriting")
        exit(1)

    with open(outputFileName, "w") as outputFile:
        outputFile.write(parse(inputFileName))
