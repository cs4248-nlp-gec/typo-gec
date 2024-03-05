import os

# This produces bad data as seen from the output.

def apply_annotations(m2_file):
    originals = []
    corrected_sentences = []
    corrections = []
    
    for line in m2_file.readlines():
        if line.startswith('S '):
            # Before starting on a new sentence, apply corrections to the current sentence if any
            if corrections:
                corrected_sentence = apply_corrections(current_sentence, corrections)
                corrected_sentences.append(corrected_sentence)
                corrections = []  # Reset corrections for the next sentence
            else:
                # If there are no corrections (first sentence or sentences without errors), add as is
                if originals:  # Avoid adding an empty string for the very first line
                    corrected_sentences.append(current_sentence)
            current_sentence = line[2:]
            originals.append(current_sentence)  # Keep track of original sentences
        elif line.startswith('A '):
            corrections.append(line)

    # Apply corrections to the last sentence
    if corrections:
        corrected_sentence = apply_corrections(current_sentence, corrections)
        corrected_sentences.append(corrected_sentence)
    else:
        # If no corrections for the last sentence, just add it as it was
        corrected_sentences.append(current_sentence)

    return originals, corrected_sentences

def apply_corrections(sentence, correction_lines):
    corrections = []
    for line in correction_lines:
        parts = line.split('|||')
        start_idx, end_idx = map(int, parts[0].split()[1:3])
        correction = parts[2] if len(parts) > 2 else ""
        corrections.append((start_idx, end_idx, correction))

    corrections.sort(reverse=True)
    for start_idx, end_idx, correction in corrections:
        words = sentence.split()
        # Remove incorrect words and insert correction if there is one
        if start_idx != -1:  # Ignore noop
            del words[start_idx:end_idx+1]
            if correction:
                words.insert(start_idx, correction)
        sentence = ' '.join(words)

    return sentence


for filename in os.listdir("./data"):
    if filename.endswith(".m2"):
        file_path = os.path.join("./data", filename)
        output_file_path = os.path.join("./out", filename.replace(".m2", "_corrected.txt"))

        with open(file_path, "r") as file:
            with open(output_file_path, "w") as out:
                for og, ne in zip(*apply_annotations(file)):
                    out.write(f"S {og}\nC {ne}\n\n")