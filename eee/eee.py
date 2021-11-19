#!/bin/env python3

import sys
import re


LETTER = "e"
PREPROCESSOR_DEFINES: dict = {}


def e_word(word: str) -> bool:
    return set(list(word)) == set(word[0])


def generate_e(original: str) -> str:
    if not e_word(original):
        PREPROCESSOR_DEFINES[original] = (
            (len(PREPROCESSOR_DEFINES) + 1) * LETTER
            if original not in PREPROCESSOR_DEFINES.keys()
            else PREPROCESSOR_DEFINES[original]
        )
        return PREPROCESSOR_DEFINES[original]
    else:
        return original


def remove_comments(input: str) -> str:
    res: str = re.sub(
        "\\/\\*[\\s\\S]*\\*\\/", "\n", input
    )  # replace multiline comments with a "\n"
    res: str = re.sub("\\/\\/.*", " ", res)  # replace comments with a " "
    return res


def convert_strings(input: str) -> str:
    res: str = ""
    stringMatcher = re.compile('(".*?")')

    for line in input.split("\n"):
        strings = re.findall(stringMatcher, line)
        if len(strings) > 0:
            for string in strings:
                line.replace(string, generate_e(string))

        res += line + "\n"
    return res


def parse(inputFileName: str) -> str:

    code: str = ""

    with open(inputFileName, "r") as inputFile:
        file = remove_comments(inputFile.read())
        file = convert_strings(file)
        print(file)

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

    print(str(PREPROCESSOR_DEFINES))
    return code


if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if inputFileName == outputFileName:
        print("No overwriting")
        exit(1)

    with open(outputFileName, "w") as outputFile:
        outputFile.write(parse(inputFileName))
