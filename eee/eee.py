#!/bin/env python3

import sys
import re


LETTER = "e"
PREPROCESSOR_DEFINES: dict = {}


def e_word(word: str) -> bool:
    return set(list(word)) == set(LETTER)


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
        "\\/\\*[\\s\\S]*?\\*\\/", "\n", input
    )  # replace multiline comments with a "\n"
    res: str = re.sub("\\/\\/.*", " ", res)  # replace comments with a " "
    return res


def convert(input: str, regex: str, padding: str = "") -> str:
    res: str = ""
    matcher = re.compile(regex)

    for i, line in enumerate(input.split("\n")):
        if not line.strip().startswith("#"):
            strings = re.findall(matcher, line)
            if len(strings) > 0:
                for string in strings:
                    line: str = line.replace(
                        string, f"{padding}{generate_e(string)}{padding}"
                    )
        res += line + "\n"
    return res


def parse(inputFileName: str) -> str:
    with open(inputFileName, "r") as inputFile:
        file = remove_comments(inputFile.read())
        file = convert(file, '(".*?")')  # replace strng literals
        file = convert(file, "[\\w\\d]+")  # replace words
        file = convert(
            file, "[^\\w^\\s]+", padding=" "
        )  # replace punctuation and other characters

    code: str = "".join(
        [
            f"#define {e_word} {original}\n"
            for original, e_word in PREPROCESSOR_DEFINES.items()
        ]
    )
    code += file
    return code


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments!", file=sys.stderr)
        exit(2)
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if inputFileName == outputFileName:
        print("No overwriting", file=sys.stderr)
        exit(1)

    with open(outputFileName, "w") as outputFile:
        outputFile.write(parse(inputFileName))
