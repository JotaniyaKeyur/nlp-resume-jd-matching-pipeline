import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def clean_text(self, text):
        """clean and normalize text"""
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        text = re.sub(r'[^\w\s\.\-\,\/\(\)]', '', text)

        return text

    def tokenize_sentences(self, text):
        """split text into sentences"""
        return sent_tokenize(text)

    def tokenize_words(self, text, remove_stopwords=True):
        """tokenize text into words with optional stop words removal"""
        words = word_tokenize(text.lower())
        if remove_stopwords:
            words = [w for w in words if w not in self.stop_words and w.isalnum()]
        return words

    def lemmatize_tokens(self, tokens):
        """Lemmatize list of tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def get_pos_tags(self, text):
        """parts-of-speech tags for text"""
        words = word_tokenize(text)
        return nltk.pos_tag(words)
