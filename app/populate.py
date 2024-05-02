import json
from app.config import db
from app.models import Publications, Recommendations


# Function to populate the database with data from a local TSV file
def populate_database():
    db.session.query(Publications).delete()
    db.session.commit()
    filename = 'data/relish_text.jsonl'  # Path to JSON file
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
    filename = 'data/relish_recoms.jsonl'  # Path to JSON file
    with open(filename, 'r', newline='', encoding='utf-8') as jsonfile:
        for line in jsonfile:
            data = json.loads(line)
            data_entry = Recommendations(PMID=data['pmid'], recom_number=data['recom_number'], target_pmid=data['target_pmid'], relevance=data['relevance'])
            db.session.add(data_entry)
    db.session.commit()
    print("Database populated with recommendations.")