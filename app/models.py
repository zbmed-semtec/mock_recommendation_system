from app.config import db
from sqlalchemy import Integer

class Publications(db.Model):
    PMID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    abstract = db.Column(db.String(255))

class Recommendations(db.Model):
    PMID = db.Column(db.Integer, db.ForeignKey('publications.PMID'), primary_key=True)
    recom_number = db.Column(db.Integer, primary_key=True)
    target_pmid = db.Column(db.String(255))
    relevance = db.Column(db.Integer)
