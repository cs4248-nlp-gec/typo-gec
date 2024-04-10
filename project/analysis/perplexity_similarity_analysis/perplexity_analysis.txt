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
    loss=model(tensor_input, labels=tensor_input)[0]
    return np.exp(loss.detach().numpy())

def total_score(model, tokenizer, filename):
    total_score = 0
    nan_count = 0
    total_lines = 0
    with open(filename, 'r', errors="ignore") as f:
        lines = f.readlines()
        total_lines += len(lines)
        for line in lines:
            sentence = line.strip()
            if sentence:
                to_add = score(model, tokenizer, sentence)
                if np.isnan(to_add):
                    nan_count += 1
                else:
                    total_score += to_add
    return total_score/(total_lines - nan_count), 100 * nan_count / (total_lines)

# add the files seperately
#f_long, f_short, f_light, f_medium, f_heavy = "long_typo.txt", "short_typo.txt", "light_typo.txt", "medium_typo.txt", "heavy_typo.txt"

long, long_nan = total_score(model, tokenizer, f_long)
short, short_nan = total_score(model, tokenizer, f_short)
light, light_nan = total_score(model, tokenizer, f_light)
medium, medium_nan = total_score(model, tokenizer, f_medium)
heavy, heavy_nan = total_score(model, tokenizer, f_heavy)

print("Score for long: ", long, long_nan)
print("Score for short: ", short, short_nan)
print("Score for light: ", light, light_nan)
print("Score for medium: ", medium, medium_nan)
print("Score for heavy: ", heavy, heavy_nan)



'''
perplexity score analysis

score format: average perplexity score, number of nan, number of lines, percentage of nan
Score for long:   461.787511013522,     0,      101,        0%
Score for short:  7736.254397026347,    7,      596,        1.17%
Score for light:  1930.290759843189,    5,      4384,       0.114%
Score for medium: 3419.8989599032425,   3,      4384,       0.0684%
Score for heavy:  2795.5261774032642,   2,      4384,       0.0456%


long sentences is corrected better than short sentences (probably because there is more words available to guess the correction.
Failure to correct in short sentence also affects how readble the sentence is much more than long sentence since there is lesser context)

Light PP score is better than medium and heavy PP score as expected.
But heavy PP score is somehow slightly better than medium. (Maybe is that the difference is about the same, equally 
bad since the difference is not as high between the long and short)
'''