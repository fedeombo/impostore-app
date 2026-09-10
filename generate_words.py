# generate_words.py
import sqlite3

DB_NAME = "words.db"

# Coppie (Parola Civili, Indizio Impostore) - Entrambi singoli vocaboli
VOCABULARY = {
    "Cibo": [
        ("Pizza", "Forno"),
        ("Pasta", "Grano"),
        ("Gelato", "Freddo"),
        ("Pane", "Farina"),
        ("Mela", "Albero"),
        ("Formaggio", "Latte"),
        ("Cioccolato", "Cacao"),
        ("Biscotto", "Colazione"),
        ("Carne", "Griglia"),
        ("Pesce", "Mare"),
        ("Riso", "Chicco"),
        ("Patata", "Terra"),
        ("Pomodoro", "Rosso"),
        ("Caffè", "Tazzina"),
        ("Uovo", "Guscio"),
        ("Torta", "Candeline"),
        ("Fragola", "Rosso"),
        ("Limone", "Agro"),
        ("Miele", "Ape"),
        ("Olio", "Oliva"),
        ("Salame", "Fetta"),
        ("Prosciutto", "Stagionato"),
        ("Zucchero", "Dolce"),
        ("Sale", "Sapido"),
        ("Cipolla", "Lacrime"),
        ("Aglio", "Spicchio"),
        ("Funghi", "Bosco"),
        ("Vino", "Uva"),
        ("Birra", "Schiuma"),
        ("Banana", "Giallo")
    ],
    "Animali": [
        ("Cane", "Guinzaglio"),
        ("Gatto", "Fusa"),
        ("Leone", "Savana"),
        ("Tigre", "Strisce"),
        ("Elefante", "Proboscide"),
        ("Lupo", "Branco"),
        ("Orso", "Letargo"),
        ("Aquila", "Volo"),
        ("Squalo", "Pinna"),
        ("Delfino", "Salto"),
        ("Cavallo", "Sella"),
        ("Mucca", "Fattoria"),
        ("Pecora", "Lana"),
        ("Giraffa", "Collo"),
        ("Zebra", "Bianconero"),
        ("Serpente", "Veleno"),
        ("Coccodrillo", "Fiume"),
        ("Pinguino", "Ghiaccio"),
        ("Gufo", "Notte"),
        ("Farfalla", "Bruco"),
        ("Volpe", "Coda"),
        ("Scimmia", "Liana"),
        ("Rana", "Stagno"),
        ("Topo", "Formaggio"),
        ("Balena", "Oceano"),
        ("Pipistrello", "Grotta"),
        ("Formica", "Colonia"),
        ("Ape", "Puntura"),
        ("Zanzara", "Prurito"),
        ("Camaleonte", "Colore")
    ],
    "Oggetti": [
        ("Telefono", "Schermo"),
        ("Chiave", "Serratura"),
        ("Orologio", "Tempo"),
        ("Portafoglio", "Monete"),
        ("Zaino", "Spalle"),
        ("Ombrello", "Pioggia"),
        ("Bicchiere", "Vetro"),
        ("Piatto", "Tavola"),
        ("Forchetta", "Denti"),
        ("Coltello", "Lama"),
        ("Cucchiaio", "Zuppa"),
        ("Bottiglia", "Tappo"),
        ("Penna", "Inchiostro"),
        ("Matita", "Grafite"),
        ("Gomma", "Cancellare"),
        ("Quaderno", "Fogli"),
        ("Libro", "Capitolo"),
        ("Specchio", "Riflesso"),
        ("Pettine", "Capelli"),
        ("Cuscino", "Letto"),
        ("Coperta", "Caldo"),
        ("Sedia", "Schienale"),
        ("Tavolo", "Gambe"),
        ("Lampada", "Luce"),
        ("Quadro", "Cornice"),
        ("Scarpa", "Suola"),
        ("Calzino", "Piede"),
        ("Cintura", "Fibbia"),
        ("Occhiali", "Lenti"),
        ("Portachiavi", "Mazzo")
    ],
    "Cinema": [
        ("Attore", "Recitazione"),
        ("Regista", "Regia"),
        ("Copione", "Battuta"),
        ("Oscar", "Premio"),
        ("Popcorn", "Mais"),
        ("Cinema", "Sala"),
        ("Biglietto", "Ingresso"),
        ("Schermo", "Telo"),
        ("Proiettore", "Fascio"),
        ("Poltrona", "Fila"),
        ("Trailer", "Anteprima"),
        ("Locandina", "Manifesto"),
        ("Commedia", "Risate"),
        ("Dramma", "Lacrime"),
        ("Horror", "Paura"),
        ("Thriller", "Tensione"),
        ("Cartone", "Disegno"),
        ("Cameraman", "Cinepresa"),
        ("Costume", "Vestito"),
        ("Trucco", "Faccia")
    ],
    "Scienza": [
        ("Neurone", "Cervello"),
        ("Atomo", "Nucleo"),
        ("Molecola", "Legame"),
        ("Cellula", "Microscopio"),
        ("Batterio", "Infezione"),
        ("Pianeta", "Orbita"),
        ("Stella", "Luce"),
        ("Galassia", "Spazio"),
        ("Cometa", "Scia"),
        ("Gravità", "Caduta"),
        ("Energia", "Corrente"),
        ("Laboratorio", "Camice"),
        ("Telescopio", "Cielo"),
        ("Provetta", "Chimica"),
        ("DNA", "Genetica"),
        ("Vulcano", "Magma"),
        ("Terremoto", "Faglia"),
        ("Magnete", "Attrazione"),
        ("Robot", "Circuito"),
        ("Laser", "Raggio")
    ]
}

def populate_words():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS words")
    cursor.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            word TEXT NOT NULL UNIQUE,
            hint TEXT NOT NULL
        )
    """)

    words_batch = []
    seen = set()

    for category, items in VOCABULARY.items():
        for word, hint in items:
            clean_word = word.strip()
            clean_hint = hint.strip()
            if clean_word.lower() not in seen:
                seen.add(clean_word.lower())
                words_batch.append((category, clean_word, clean_hint))

    cursor.executemany("INSERT INTO words (category, word, hint) VALUES (?, ?, ?)", words_batch)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM words")
    total = cursor.fetchone()[0]
    print(f"Database aggiornato: {total} parole e indizi a singolo vocabolo.")
    conn.close()

if __name__ == "__main__":
    populate_words()