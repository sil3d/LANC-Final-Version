import nltk
import numpy as np
import unidecode
from spellchecker import SpellChecker

nltk.download('punkt')

# Initialize stemmers and spell checkers
stemmer_fr = nltk.stem.SnowballStemmer('french')
stemmer_en = nltk.stem.SnowballStemmer('english')
spell_fr = SpellChecker(language='fr')
spell_en = SpellChecker(language='en')
ignore_words = ['?', '.', '!', '<', '>', ',', '-', '_', ':', ';', '(', ')', '[', ']', 'é', 'ë', 'è', 'ê', 'à', 'â', 'ô', 'î', 'ù', 'û', 'ç', '£', '$', '€', '¥', '§', '%', '*', '&', '@', '#']

def tokenize(sentence, language='fr'):
    # Correct spelling errors and split the sentence into words
    corrected = correct_spelling(sentence, language)
    return nltk.word_tokenize(corrected)

def stem(word, language='fr'):
    # Remove accents and return lowercase
    if language == 'fr':
        return unidecode.unidecode(stemmer_fr.stem(word)).lower()
    elif language == 'en':
        return stemmer_en.stem(word).lower()
    else:
        raise ValueError(f'Unsupported language: {language}')

def bag_of_words(tokenized_sentence, all_words):
    # Stem each word in the tokenized sentence
    sentence_words = [stem(word) for word in tokenized_sentence]
    # Initialize bag with 0 for each word
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in sentence_words:
            bag[idx] = 1
    return bag

def correct_spelling(sentence, language='fr'):
    if language == 'fr':
        spell = spell_fr
    elif language == 'en':
        spell = spell_en
    else:
        raise ValueError(f'Unsupported language: {language}')
    
    # Correct spelling for each word in the sentence
    words = sentence.split()
    corrected = []
    for word in words:
        # Only correct spelling for words not in the ignore list and not starting with "http"
        if word not in ignore_words and not word.startswith("http"):
            corrected_word = spell.correction(word)
            corrected.append(corrected_word)
        else:
            corrected.append(word)
    # Remove non-string items from the list
    corrected = [word for word in corrected if isinstance(word, str)]
    return " ".join(corrected)
