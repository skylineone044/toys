#!/bin/env python3

import sys
import re


LETTER = "e"
PREPROCESSOR_DEFINES: dict = {}
PREPROCESSOR_BLACKLIST = ("assert")


def e_word(word: str) -> bool:
    return set(list(word)) == set(LETTER)


def generate_e(original: str) -> str:
    if not e_word(original) and original not in PREPROCESSOR_BLACKLIST:
        PREPROCESSOR_DEFINES[original] = (
            (len(PREPROCESSOR_DEFINES) + 1) * LETTER
            if original not in PREPROCESSOR_DEFINES.keys()
            else PREPROCESSOR_DEFINES[original]
        )
        # print(f"replacing: {original} -> {PREPROCESSOR_DEFINES[original]}")
        return PREPROCESSOR_DEFINES[original]
    else:
        return original


def remove_comments(input: str) -> str:
    res: str = re.sub(
        "\\/\\*[\\s\\S]*?\\*\\/", "\n", input
    )  # replace multiline comments with a "\n"
    res: str = re.sub("\\/\\/.*", " ", res)  # replace comments with a " "
    return res


def generate_tokens(input: str, regex: str) -> None:
    matcher = re.compile(regex)
    for line in input.split("\n"):
        if not line.strip().startswith("#"):
            matches = re.findall(matcher, line)
            for string in matches:
                generate_e(string)


def escape(token: str) -> str:
    return "".join(
        [
            f"\\{letter}" if not letter.isalpha() and not letter.isnumeric() else letter
            for letter in list(token)
        ]
    )


def convert(input: str, padding: str) -> str:
    tokens: list = list(PREPROCESSOR_DEFINES.keys())
    tokens.sort(reverse=True, key=len)

    res: str = ""

    for line in input.split("\n"):
        if not line.strip().startswith("#"):
            for token in tokens:
                line = line.replace(
                    token, f"{padding}{PREPROCESSOR_DEFINES[token]}{padding}"
                )
        res += line + "\n"

    return res


def assert_handler(input: str) -> str:
    for line in input.split("\n"):
        if line.strip().startswith("assert"):
            # line =
            # fix assert


def parse(inputFileName: str) -> str:
    with open(inputFileName, "r") as inputFile:
        file = remove_comments(inputFile.read())

        regex_string = '(".*?")'
        regex_words = "([\\w\\d]+)"
        regex_symbols = "([^\\w^\\s]+)"

        generate_tokens(file, regex_string)
        file = convert(file, padding=" ")
        generate_tokens(file, regex_words)
        file = convert(file, padding=" ")
        generate_tokens(file, regex_symbols)
        file = convert(file, padding=" ")

    code = "".join(
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
