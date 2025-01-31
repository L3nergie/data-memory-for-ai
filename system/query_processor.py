import json
from typing import List, Dict, Tuple
from utils.hash_generator import generate_hash
from utils.tokenizer import tokenize_phrase

class QueryProcessor:
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

    def search(self, query: str, relevance_threshold: int = 50, max_results: int = 10) -> List[Tuple[str, float]]:
        results = []
        query_words = query.split()
        for phrase, metadata in self.phrases_data.items():
            relevance = self._calculate_relevance(query_words, metadata["tokens"])
            if relevance >= relevance_threshold:
                results.append((phrase, relevance))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:max_results]

    def _calculate_relevance(self, query_words: List[str], phrase_tokens: List[str]) -> float:
        common_tokens = set(query_words).intersection(set(phrase_tokens))
        return (len(common_tokens) / len(query_words)) * 100
