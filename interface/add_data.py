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
