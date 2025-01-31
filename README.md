# Projet de Recherche Sémantique en Temps Réel

Ce projet est une application Python qui permet d'effectuer des recherches sémantiques en temps réel. Il offre une interface interactive pour ajouter des mots ou des phrases à une base de données, effectuer des requêtes dynamiques, et ajuster les résultats en fonction de la pertinence et de la longueur des phrases.

---

## Structure du Projet

```
projet/
│
├── database/
│   ├── words.json          # Table des mots avec leurs hashs et relations
│   ├── phrases.json        # Table des phrases avec leurs tokens et relations
│
├── system/
│   ├── query_processor.py  # Système de traitement des requêtes
│   ├── data_handler.py     # Gestion des mots et phrases (ajout, vérification, hash)
│
├── interface/
│   ├── main.py             # Interface principale pour les requêtes en temps réel
│   ├── add_data.py         # Widget pour ajouter des mots ou des phrases
│
├── utils/
│   ├── hash_generator.py   # Génération de hashs pour les mots
│   ├── tokenizer.py        # Tokenisation des phrases et vérification des limites
│
├── README.md               # Documentation du projet
├── requirements.txt        # Dépendances du projet
```

---

## Fonctionnalités

1. **Recherche en Temps Réel** :
   - Affichage des résultats dès qu'un mot est entré.
   - Ajustement dynamique des résultats en fonction des mots supplémentaires.
   - Barre d'ajustement pour modifier le nombre de résultats et la pertinence.

2. **Gestion des Mots et Phrases** :
   - Vérification de l'existence des mots dans la base de données.
   - Génération de hashs pour sécuriser les mots.
   - Ajout de relations entre les mots et les phrases.
   - Découpage des phrases en tokens (entre 75 et 125 tokens) en respectant les points de fin de phrase.

3. **Interface Utilisateur** :
   - Champ de recherche interactif pour les requêtes.
   - Widget pour ajouter des mots ou des phrases à la base de données.

4. **Sécurité** :
   - Les mots sont stockés sous forme de hashs, avec une clé de cryptage basée sur le nombre de lettres.
   - Impossible d'avoir des doublons dans la table des mots.

---

## Utilisation

### Prérequis

- Python 3.x
- Bibliothèques : `json`, `hashlib`, `re`

### Installation

1. Clonez le dépôt du projet :

   ```bash
   git clone https://github.com/votre-utilisateur/votre-projet.git
   cd votre-projet
   ```

2. Installez les dépendances (si nécessaire) :

   ```bash
   pip install -r requirements.txt
   ```

---

## Fichiers et Fonctionnalités Détails

### 1. `system/query_processor.py`

Ce fichier contient la logique de traitement des requêtes. Il gère la recherche en temps réel et l'ajustement des résultats.

```python
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
```

---

### 2. `system/data_handler.py`

Ce fichier gère l'ajout de mots et de phrases à la base de données, ainsi que la vérification des doublons.

```python
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
```

---

### 3. `utils/hash_generator.py`

Ce fichier génère des hashs pour les mots en utilisant le nombre de lettres comme clé de cryptage.

```python
import hashlib

def generate_hash(word: str) -> str:
    key = str(len(word))
    return hashlib.sha256((word + key).encode()).hexdigest()
```

---

### 4. `utils/tokenizer.py`

Ce fichier tokenise les phrases et vérifie les limites de tokens (entre 75 et 125).

```python
import re

def tokenize_phrase(phrase: str) -> List[str]:
    # Découpage en tokens en respectant les points de fin de phrase
    tokens = re.split(r'[ !?.;"\']+', phrase)
    tokens = [token for token in tokens if token]
    return tokens
```

---

### 5. `interface/main.py`

Ce fichier contient l'interface principale pour les requêtes en temps réel.

```python
from system.query_processor import QueryProcessor

def main():
    query_processor = QueryProcessor("database/words.json", "database/phrases.json")
    while True:
        query = input("Entrez votre recherche : ")
        results = query_processor.search(query)
        for result, relevance in results:
            print(f"{result} (Pertinence : {relevance:.2f}%)")

if __name__ == "__main__":
    main()
```

---

### 6. `interface/add_data.py`

Ce fichier contient le widget pour ajouter des mots ou des phrases.

```python
from system.data_handler import DataHandler

def add_data():
    data_handler = DataHandler("database/words.json", "database/phrases.json")
    while True:
        data = input("Entrez un mot ou une phrase : ")
        if " " in data:
            data_handler.add_phrase(data)
        else:
            data_handler.add_word(data)
        print("Donnée ajoutée avec succès !")

if __name__ == "__main__":
    add_data()
```

---

## Conclusion

Ce projet est conçu pour être modulaire et extensible. Vous pouvez facilement ajouter de nouvelles fonctionnalités ou améliorer les existantes. N'hésitez pas à adapter le code à vos besoins spécifiques !

---

N'hésitez pas à me demander si vous avez besoin d'autres ajustements ou explications ! 😊
