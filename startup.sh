python3 -m venv venv
pip install -r requirements.txt
sqlite3 data/boardgames.db < data/boardgames_dump.sql
sqlite3 data/boardgames.db "PRAGMA foreign_keys = ON;"
python3 generate_env.py
python3 -m app.main