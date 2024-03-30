from model import NorvigTypoModel
import re
import argparse


def predict(input_path, output_path, is_verbose=True):
    model = NorvigTypoModel("big.txt")
    with open(input_path, 'r') as input_file:
        with open(output_path, 'w') as output_file:
            inp_lines = input_file.readlines()
            lines_num = len(inp_lines)
            if is_verbose:
                print("Processing {} lines.".format(lines_num))
            for idx, line in enumerate(inp_lines):
                line_corrected = model.predict_sentence(line)
                output_file.write(line_corrected)
                if (idx + 1) % 100 == 0 and is_verbose:
                    print("Processed {} / {} lines.".format(idx + 1, lines_num))


# To test, try running the following command:
# python predict.py --input_path ../../project/sentences_only/test/ABCN.dev.gold.bea19_original_typo.txt --output_path out.txt
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_path", help="Path to input file", required=True)
    parser.add_argument(
        "--output_path", help="Path to output file", required=True)
    args = parser.parse_args()
    predict(args.input_path, args.output_path)
