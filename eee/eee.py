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
        [f"\\{letter}" if not letter.isalpha() and not letter.isnumeric() else letter for letter in list(token)]
    )


def convert(input: str, padding: str) -> str:
    tokens: list = list(PREPROCESSOR_DEFINES.keys())
    tokens.sort(reverse=True, key=len)

    # regex_tokenMatcher = "[^A-Za-z0-9]{1}token[^A-Za-z0-9]{1}"

    res: str = ""

    for line in input.split("\n"):
        if not line.strip().startswith("#"):
            for token in tokens:
            # regex = f"[^A-Za-z0-9]{escape(token)}[^A-Za-z0-9]"
                line = line.replace(token, f"{padding}{PREPROCESSOR_DEFINES[token]}{padding}")
                # line: str = re.sub(
                #     regex,
                #     f"{padding}{PREPROCESSOR_DEFINES[token]}{padding}",
                #     line,
                # )
        res += line + "\n"

    return res


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
