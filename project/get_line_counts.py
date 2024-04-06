import os
import json
from pprint import pprint

def count_lines_in_file(file_path):
    """Counts the number of lines in a given file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def find_txt_files_and_count_lines(start_dir):
    """Finds all .txt files from start_dir, counts lines in them, and stores the counts in a dictionary."""
    line_counts = {}
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                line_counts[full_path] = count_lines_in_file(full_path)
    return line_counts

def save_counts_to_file(line_counts, output_file):
    """Saves the line counts dictionary to a JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(line_counts, f, indent=4)
        print(f"Line counts successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to file {output_file}: {e}")

# Example usage
line_counts = find_txt_files_and_count_lines('.')
save_counts_to_file(line_counts, 'line_counts.json')
