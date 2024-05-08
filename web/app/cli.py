import json
from flask import Flask
from flask.cli import AppGroup
from app.config import app, db
from app.models import Publications, Recommendations

cli = AppGroup('populate', help="Commands for populating the database.")

@cli.command('all')
def populate_all():
    populate_articles()
    populate_recommendations()

def populate_articles():
    db.session.query(Publications).delete()
    db.session.commit()
    filename = 'data/relish_text.jsonl'
    with open(filename, 'r', newline='', encoding='utf-8') as jsonfile:
        for line in jsonfile:
            data = json.loads(line)
            data_entry = Publications(PMID=data['pmid'], title=data['title'], abstract=data['abstract'])
            db.session.add(data_entry)
    db.session.commit()
    print("Database populated with articles.")

def populate_recommendations():
    db.session.query(Recommendations).delete()
    db.session.commit()
    filename = 'data/relish_recoms.jsonl'
    with open(filename, 'r', newline='', encoding='utf-8') as jsonfile:
        for line in jsonfile:
            data = json.loads(line)
            data_entry = Recommendations(PMID=data['pmid'], recom_number=data['recom_number'], target_pmid=data['target_pmid'], relevance=data['relevance'])
            db.session.add(data_entry)
    db.session.commit()
    print("Database populated with recommendations.")

app.cli.add_command(cli)
