import json
from utils.hash_generator import generate_hash
from utils.tokenizer import tokenize_phrase
from datetime import datetime

class DataHandler:
    def __init__(self, words_file: str, phrases_file: str, hash_list_file: str):
        self.words_file = words_file
        self.phrases_file = phrases_file
        self.hash_list_file = hash_list_file
        self.words_data = self._load_data(words_file)
        self.phrases_data = self._load_data(phrases_file)
        self.hash_list = self._load_data(hash_list_file)

    def _load_data(self, filename: str) -> Dict:
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"hashes": [], "last_verified": None}

    def add_word(self, word: str):
        word_hash = generate_hash(word)
        if word_hash not in self.words_data:
            # Ajouter le hash à la liste et lui attribuer un numéro unique
            hash_number = len(self.hash_list["hashes"])
            self.hash_list["hashes"].append(word_hash)
            self.words_data[word_hash] = {
                "word": word,
                "hash_number": hash_number,
                "relations": [],
                "relation_count": 0  # Initialiser le compteur de relations
            }
            self._save_data(self.words_file, self.words_data)
            self._save_data(self.hash_list_file, self.hash_list)

    def add_relation(self, word1: str, word2: str):
        hash1 = generate_hash(word1)
        hash2 = generate_hash(word2)
        if hash1 in self.words_data and hash2 in self.words_data:
            if word2 not in self.words_data[hash1]["relations"]:
                self.words_data[hash1]["relations"].append(word2)
                self.words_data[hash1]["relation_count"] += 1
            if word1 not in self.words_data[hash2]["relations"]:
                self.words_data[hash2]["relations"].append(word1)
                self.words_data[hash2]["relation_count"] += 1
            self._save_data(self.words_file, self.words_data)

    def add_phrase(self, phrase: str):
        tokens = tokenize_phrase(phrase)
        if phrase not in self.phrases_data:
            self.phrases_data[phrase] = {"tokens": tokens, "relations": []}
            self._save_data(self.phrases_file, self.phrases_data)

    def verify_data_integrity(self):
        # Vérifier que chaque hash dans words_data existe dans hash_list
        for word_hash, metadata in self.words_data.items():
            if word_hash not in self.hash_list["hashes"]:
                print(f"Erreur : Le hash {word_hash} n'existe pas dans la liste des hashs.")
                return False
        print("Vérification terminée : Aucune corruption détectée.")
        self.hash_list["last_verified"] = datetime.now().isoformat()
        self._save_data(self.hash_list_file, self.hash_list)
        return True

    def _save_data(self, filename: str, data: Dict):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
