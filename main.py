# main.py
import sqlite3
import random
import uuid
from typing import List, Dict, Set
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="L'Impostore")
DB_NAME = "words.db"

# Sessioni in-memory: session_id -> { "used_words": set(), "categories": list() }
sessions: Dict[str, Dict] = {}

class StartSessionRequest(BaseModel):
    categories: List[str]

class NextRoundRequest(BaseModel):
    session_id: str
    players: List[str]
    num_impostors: int = 1

def query_db(query: str, args=(), one=False):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/categories")
def get_categories():
    rows = query_db("SELECT DISTINCT category FROM words")
    return {"categories": [r[0] for r in rows]}

@app.post("/api/session/start")
def start_session(req: StartSessionRequest):
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        "categories": req.categories,
        "used_word_ids": set()
    }
    return {"session_id": session_id}

@app.post("/api/round/next")
def next_round(req: NextRoundRequest):
    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessione non trovata")
    
    if req.num_impostors >= len(req.players):
        raise HTTPException(status_code=400, detail="Troppi impostori per il numero di giocatori")

    categories = session["categories"]
    used_ids = list(session["used_word_ids"])
    
    # Costruiamo la query escludendo le parole già usate
    placeholders_cat = ",".join(["?"] * len(categories))
    query = f"SELECT id, category, word, hint FROM words WHERE category IN ({placeholders_cat})"
    params = list(categories)

    if used_ids:
        placeholders_used = ",".join(["?"] * len(used_ids))
        query += f" AND id NOT IN ({placeholders_used})"
        params.extend(used_ids)

    query += " ORDER BY RANDOM() LIMIT 1"
    row = query_db(query, tuple(params), one=True)

    # Se le parole sono finite per quelle categorie, resettiamo il pool della sessione
    if not row:
        session["used_word_ids"].clear()
        query_reset = f"SELECT id, category, word, hint FROM words WHERE category IN ({placeholders_cat}) ORDER BY RANDOM() LIMIT 1"
        row = query_db(query_reset, tuple(categories), one=True)
        if not row:
            raise HTTPException(status_code=400, detail="Nessuna parola trovata per le categorie selezionate")

    word_id, category, secret_word, hint = row
    session["used_word_ids"].add(word_id)

    # Assegnazione ruoli casuale
    players = list(req.players)
    random.shuffle(players)
    impostors = set(random.sample(players, req.num_impostors))

    # Creazione carte giocatore ordinate per l'ordine di passaggio telefono
# Creazione carte giocatore
    cards = []
    for player in req.players:
        is_imp = player in impostors
        cards.append({
            "player": player,
            "is_impostor": is_imp,
            "role": "Impostore" if is_imp else "Civile",
            "category": category,
            # Se è impostore non conosce la parola esatta, ma vede l'indizio a singola parola
            "word": "???" if is_imp else secret_word,
            "hint": hint if is_imp else ""
        })

    return {
        "category": category,
        "cards": cards,
        "impostors": list(impostors),
        "secret_word": secret_word,
        "hint": hint
    }

if __name__ == "__main__":
    import uvicorn
    # Ascolta su 0.0.0.0 per permettere la connessione da smartphone
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)