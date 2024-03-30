# This script is for extracting out the sentences from the files in corrected_typo and original_typo that can be processed by Errant to produce m2 files.
import argparse


def extract_sentences(source_path: str, prefix: str, dest_path: str):
    prefix_length = len(prefix)
    with open(source_path, 'r') as source_file:
        with open(dest_path, 'w') as dest_file:
            for line in source_file:
                if line.startswith(prefix):
                    dest_file.write(line[prefix_length:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_path",
                        help="Path to source file",
                        required=True)
    parser.add_argument("--dest_path",
                        help="Path to destination file",
                        required=True)
    parser.add_argument("--prefix",
                        help="Prefix to identify sentences to extract",
                        required=True)
    args = parser.parse_args()
    extract_sentences(args.source_path, args.prefix, args.dest_path)
