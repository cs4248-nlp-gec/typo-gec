import matplotlib.pyplot as plt
import re


def analyse_POS(filename):
    # Open the file and read its contents
    with open(filename, 'r') as file:
        data = file.read()

    # Define a regular expression pattern to match the words after ":"
    pattern = re.compile(r'(?<=\w:)(\w+)')

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, data)

    # Count the occurrences of each matched word
    word_counts = {}
    for match in matches:
        if match.isdigit():
            continue
        if match in word_counts:
            word_counts[match] += 1
        else:
            word_counts[match] = 1

    sorted_word_counts = sorted(word_counts.items(),
                                key=lambda item: item[1],
                                reverse=True)

    # Get the sorted word counts
    sorted_word_counts = sorted(word_counts.items(),
                                key=lambda item: item[1],
                                reverse=True)

    for word, count in sorted_word_counts:
        print(f"{word}: {count}")


if __name__ == "__main__":
    files = ['light', 'medium', "heavy"]
    for file in files:
        print(file)
        analyse_POS(f"{file}.txt")
        print()
