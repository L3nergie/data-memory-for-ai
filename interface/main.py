from system.query_processor import QueryProcessor
from system.data_handler import DataHandler
from datetime import datetime

def main():
    query_processor = QueryProcessor("database/words.json", "database/phrases.json")
    data_handler = DataHandler("database/words.json", "database/phrases.json", "database/hash_list.json")

    # Vérification quotidienne des données
    last_verified = data_handler.hash_list.get("last_verified")
    if last_verified:
        last_verified_date = datetime.fromisoformat(last_verified)
        if (datetime.now() - last_verified_date).days >= 1:
            print("Vérification des données en cours...")
            data_handler.verify_data_integrity()

    while True:
        query = input("Entrez votre recherche : ")
        sort_alphabetical = input("Trier par ordre alphabétique ? (o/n) : ").lower() == "o"
        results = query_processor.search(query, sort_alphabetical=sort_alphabetical)
        for result, relevance in results:
            print(f"{result} (Pertinence : {relevance:.2f}%)")

if __name__ == "__main__":
    main()
