import sys
import re
import random
import time

WORD_REGEX = "[A-Za-z]{1,}"


def scramble(word: str):
    matched_words = re.findall(WORD_REGEX, word)

    for matched_word in matched_words:
        shuffled_word = matched_word
        match len(matched_word):
            case 1:
                pass
            case 2 | 3:
                shuffled_word = "".join(
                    random.sample(list(shuffled_word), len(list(shuffled_word)))
                )
            case _:
                shuffled_word = (
                    shuffled_word[0]
                    + "".join(
                        random.sample(
                            list(shuffled_word[1:-1]), len(list(shuffled_word[1:-1]))
                        )
                    )
                    + shuffled_word[-1]
                )
        word = word.replace(matched_word, shuffled_word)
        # print(f"{matched_word=}\t{shuffled_word=}")
    return word


for line in sys.stdin:
    sys.stdout.write(" ".join([scramble(word) for word in line.split(" ")]))
