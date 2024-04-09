import torch
import numpy as np

from transformers import GPT2Tokenizer, GPT2LMHeadModel
# Load pre-trained model (weights)
with torch.no_grad():
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    model.eval()
# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


def score(model, tokenizer, sentence):
    tokenize_input = tokenizer.encode(sentence)
    tensor_input = torch.tensor([tokenize_input])
    loss = model(tensor_input, labels=tensor_input)[0]
    return np.exp(loss.detach().numpy())


def total_score(model, tokenizer, filename):
    total_socre = 0
    total_lines = 0
    with open(filename, 'r', errors="ignore") as f:
        lines = f.readlines()
        total_lines += len(lines)
        for line in lines:
            sentence = line.strip()
            if sentence:
                total_socre += score(model, tokenizer, sentence)
    return total_socre / total_lines


long, short, light, medium, heavy = 0, 0, 0, 0, 0
f_long, f_short, f_light, f_medium, f_heavy = "long_typo.txt", "short_typo.txt", "light_typo.txt", "medium_typo.txt", "heavy_typo.txt"
long += total_score(model, tokenizer, f_long)
short += total_score(model, tokenizer, f_short)
light += total_score(model, tokenizer, f_light)
medium += total_score(model, tokenizer, f_medium)
heavy += total_score(model, tokenizer, f_heavy)

print("Score for long: ", long)
print("Score for short: ", short)
print("Score for light: ", light)
print("Score for medium: ", medium)
print("Score for heavy: ", heavy)

#ran this to get pp score.
# pp score for long is about 400, rest is nan (too large). Am still trying to work it out
