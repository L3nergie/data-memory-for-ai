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
