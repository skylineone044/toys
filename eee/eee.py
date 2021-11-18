#!/bin/env python3

import sys

LETTER = "e"


def parse(inputFileName: str) -> str:
    tokens = {}

    res: str = ""

    with open(inputFileName, "r") as inputFile:
        for line in inputFile.readlines():
            if line.strip().startswith("//"):
                res += line
            if line.startswith("#"):
                res += line
            if line == "\n":
                res += line

    return res


if __name__ == "__main__":
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if inputFileName == outputFileName:
        print("No overwriting")
        exit(1)

    with open(outputFileName, "w") as outputFile:
        outputFile.write(parse(inputFileName))
