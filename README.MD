# Board Game Recommendation Website

A Flask web app that recommends board games based on what games the user likes and dislikes.

## Some Technologies Used:
* Flask
* WTForms
* Flask SQLAlchemy
* Flask Migrate (Alembic)
* Requests with xml.etree
* Pandas
* Dotenv

## Installation and Setup Guide:
1. Clone the repository.

2. (Optional but recommended) Set up a virtual environment:
```bash
python3 -m venv venv
```
3. Install required dependencies (assuming you already have pip):
```bash
pip install -r requirements.txt
```
4. Convert the sql dump to a database:
```bash
sqlite3 data/boardgames.db < data/boardgames_dump.sql
```
5. Activate foreign keys for the database:
```bash
sqlite3 data/boardgames.db
PRAGMA foreign_keys = ON;
```
6. Generate an environment:
```bash
python3 generate_env.py
```
7. Run:
```bash
python3 -m app.main
```