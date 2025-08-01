# COLX 523 - Project - ARCOT
## The Abstraction and Reasoning Corpus - using Chain of Thoughts
---
## Milestone 1
The `Milestone1` directory contains the following files:
1. `Project Proposal.pdf`: The project proposal document.
2. `Teamwork Contract.pdf`: The teamwork contract document.

## Milestone 2
The `Milestone2` directory contains the following files:
1. `milestone2.md`: Explanation of the updates due for milestone 2 as described in the instruction repo. It contains descriptions of the corpus, its sources, its format, etc.

## Milestone 3
The `Milestone3` directory contains the following files:
1. `milestone3.md`: Explanation of the updates due for milestone 3 as described in the instruction repo. It contains descriptions of the annotations and the inter annotator agreement.

## Data
The `data` directory contains the following subdirectories:
1. `references`: Partial dataset comprising of gpt4 and human annotations that is used as a basis to form the corpus.
2. `original`: Original Kaggle dataset comprising of images in the form of .json files, that we use to form our main corpus containing images and the annotations.
3. `images`: Images regenerated from the .json files in the `original` folder, that we use for writing the human annotations.
4. `annotations`: Annotations for the images in the form of .tsv files.

## Source
The `src` directory contains the following files:
1. `utils.py`: Python script that converts .json files of images into .png files for visual aid while writing the human annotations.
