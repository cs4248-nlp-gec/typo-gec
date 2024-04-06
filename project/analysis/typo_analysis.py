import difflib
from pprint import pprint


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.readlines()


def compare_files(predicted_file_path,
                  original_file_path):  # original_file should have no typos.
    file1_lines = read_file(file1_path)
    file2_lines = read_file(file2_path)

    d = difflib.Differ()

    for line1, line2 in zip(file1_lines, file2_lines):
        words1 = line1.strip().split()
        words2 = line2.strip().split()
        diff = list(d.compare(words2, words1))
        pprint(diff)


# True positive = match the typo to the corrected properly
# True negative =
def get_score(line1, line2, typos, corrected):
    pass


# Example usage
file1_path = 'path/to/file1.txt'
file2_path = 'path/to/file2.txt'
compare_files(file1_path, file2_path)
