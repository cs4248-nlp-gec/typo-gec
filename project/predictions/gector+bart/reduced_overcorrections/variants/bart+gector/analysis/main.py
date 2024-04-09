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

    sorted_word_counts = sorted(
        word_counts.items(), key=lambda item: item[1], reverse=True)

    # Get the sorted word counts
    sorted_word_counts = sorted(
        word_counts.items(), key=lambda item: item[1], reverse=True)

    for word, count in sorted_word_counts:
        print(f"{word}: {count}")

    # Extract the words and counts
    words, counts = zip(*sorted_word_counts)

    # Create the pie chart
    plt.pie(counts, labels=words, autopct="%1.1f%%")
    plt.title("Most Common Errors")
    plt.savefig(f"./{filename}_plotpie.png")


def analyse_POS_bar(filename):
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

    sorted_word_counts = sorted(
        word_counts.items(), key=lambda item: item[1], reverse=True)

    # Get the sorted word counts
    sorted_word_counts = sorted(
        word_counts.items(), key=lambda item: item[1], reverse=True)

    # Prepare data
    x_vals = [word for word, count in sorted_word_counts]
    y_vals = [count for word, count in sorted_word_counts]

    # Create a bar chart
    plt.bar(x_vals, y_vals)

    # Add labels and title
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Frequency Distribution of errors")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # save the plot
    plt.savefig(f"./{filename}_plotbar.png")


if __name__ == "__main__":
    # files = ["heavy.txt", 'light.txt', 'medium.txt']
    # for file in files:
    analyse_POS('heavy.txt')
    # analyse_POS_bar('heavy.txt')
