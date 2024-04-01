# typo-gec [![telegram](https://github.com/cs4248-nlp-gec/typo-gec/actions/workflows/telegram.yml/badge.svg)](https://github.com/cs4248-nlp-gec/typo-gec/actions/workflows/telegram.yml) [![python](https://github.com/cs4248-nlp-gec/typo-gec/actions/workflows/format.yml/badge.svg)](https://github.com/cs4248-nlp-gec/typo-gec/actions/workflows/format.yml)

This repository contains the code for CS4248 Project.

## Setup guide

Please install gector from the offical repository. The model has been tested on python3.7.

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7

git clone https://github.com/grammarly/gector
cd gector

# create a virtual venv
python3 -m venv venv
source venv/bin/activate # on linux machine

# install the requirements
python -m pip install -r requirements.txt
```

If you experienced any errors during the installation process, feel free to reach out.

## Running ERRANT

ERRANT generates the M2 annotations for the given original and corrected sentences.

```bash
errant_parallel -orig <orig_file> -cor <cor_file1> [<cor_file2> ...] -out project/m2_annotations/<filename.m2>
```

## Running M2Scorer

**Note:** The m2scorer included in this repository is compatible with python3.7.

You can generate the annotations from ERRANT and then run the m2scorer to get the F0.5 score.

```bash
Usage: m2scorer [OPTIONS] PREDICTIONS ANNOTATIONS
where
 SYSTEM          -   system output, one sentence per line
 SOURCE_GOLD     -   source sentences with gold token edits

OPTIONS
-v --verbose - print verbose output
--very_verbose - print lots of verbose output
--max_unchanged_words N - Maximum unchanged words when extracting edits. Default = 2.
--ignore_whitespace_casing - Ignore edits that only affect whitespace and casing. Default no.
--beta - Set the ratio of recall importance against precision. Default = 0.5.
--timeout - Max number of seconds per sample
```
