# Language_Identifier
Determines the language of a given text file
# Run the file
The file can be ran in terminal using
- $ python language_detector.py data/train/en/all_en.txt data/train/es/all_es.txt data/test/
# Model
This program is able to take in training text files so the model can calculate the probabilities of characters being together. The text within the file is broken down to unigrams and bigrams.
- Unigrams keep count of each individual character.
- Bigrams keep count of a character given the character before it.

After those two n-grams are calculated, we smooth using add one-smoothing technique in order to add up all the probabilities. The model is then saved in English and Spanish.
# Prediciting 
The test files are given into the predict function and preprocessed to be tokenized. The tokens and the models (both the English and Spanish models) are used to calculate the probabilities. The model that creates the highest probability with the given text is the language.
- For example, if the English model has a higher probability than the Spanish model then the text must be English and will return English.
