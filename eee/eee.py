#!/bin/env python3

import sys
import re
import codecs


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
        # print(f"replacing {original} with {PREPROCESSOR_DEFINES[original]}")
        return PREPROCESSOR_DEFINES[original]
    else:
        return original


def remove_comments(input: str) -> str:
    res: str = re.sub(
        "\\/\\*[\\s\\S]*\\*\\/", "\n", input
    )  # replace multiline comments with a "\n"
    res: str = re.sub("\\/\\/.*", " ", res)  # replace comments with a " "
    return res


def convert_strings(input: str, string_regex: str, padding: str = "") -> str:
    res: str = ""
    # string_regex: str = '(".*?")'
    stringMatcher = re.compile(string_regex)

    for line in input.split("\n"):
        if line.startswith("#"):
            res += line + "\n"
        else:
            strings = re.findall(stringMatcher, line)
            if len(strings) > 0:
                for string in strings:
                    # string = codecs.decode(string, "unicode_escape")
                    line: str = line.replace(string, f"{padding}{generate_e(string)}{padding}")

            res += line + "\n"
    return res

def parse(inputFileName: str) -> str:

    code: str = ""

    with open(inputFileName, "r") as inputFile:
        file = remove_comments(inputFile.read())
        file = convert_strings(file, '(".*?")')   # replace strng literals
        file = convert_strings(file, "[\\w\\d]+")    # replace words
        # file = convert_strings(file, "[^\\w^\\s]+", padding=" ")    # replace punctuation and other characters

        print(file)
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
