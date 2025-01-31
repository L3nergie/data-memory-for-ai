import json
from utils.hash_generator import generate_hash
from utils.tokenizer import tokenize_phrase

class DataHandler:
    def __init__(self, words_file: str, phrases_file: str):
        self.words_file = words_file
        self.phrases_file = phrases_file
        self.words_data = self._load_data(words_file)
        self.phrases_data = self._load_data(phrases_file)

    def _load_data(self, filename: str) -> Dict:
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def add_word(self, word: str):
        word_hash = generate_hash(word)
        if word_hash not in self.words_data:
            self.words_data[word_hash] = {"word": word, "relations": []}
            self._save_data(self.words_file, self.words_data)

    def add_phrase(self, phrase: str):
        tokens = tokenize_phrase(phrase)
        if phrase not in self.phrases_data:
            self.phrases_data[phrase] = {"tokens": tokens, "relations": []}
            self._save_data(self.phrases_file, self.phrases_data)

    def _save_data(self, filename: str, data: Dict):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
