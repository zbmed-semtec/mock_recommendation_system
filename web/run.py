import os
import json
import pandas as pd
import logging
import datetime
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Integer
from sqlalchemy.sql import func
from flask import render_template, request
from app.models import Recommendations, Publications
from app.config import app, db
from app.cli import cli
from uuid import uuid4
import requests

app.cli.add_command(cli)


STELLA_APP_API = 'http://stella-app:8000/stella/api/v1/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LOG_DIR = "./logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "system.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Logging Configuration
logging.basicConfig(filename=LOG_FILE_PATH,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

click_dict = {}  # Global variable to store click information for the session
session_start_date = None
session_end_date = None
rec_id = None  # Global variable for recommendation ID


def index_data(jl_path):
    corpus = {}
    with open(jl_path) as jl:
        for line in jl:
            j = json.loads(line)
            corpus[j["pmid"]] = json.loads(line)
    logging.info("Indexed %s documents from %s", len(corpus), jl_path)
    return corpus


def doc_list(id_list):
    logging.info(">>>>>>>>> LEN CORPUS %s", str(len(corpus)))
    logging.info(">>>>>>>>> ID LIST %s", str(id_list))
    return [corpus.get(id) for id in id_list]

@app.route('/')
def index():
    session_id = session.get('session_id') or str(uuid4())
    logger.info(f'{session_id} - Session started ')
    session['session_id'] = session_id

    return render_template('index.html', session_id=session_id)

@app.route('/query', methods=['GET'])
def search_query():
    global click_dict, session_start_date, session_end_date, rec_id
    query_id = request.args.get('query')
    session_id = session.get('session_id')
    session_data = {
        'session_id': session.get('session_id'),  
        'query': query_id
    }

    logger.info(f'{session_id} - Search initiated for query: {query_id}')

    req = requests.get(STELLA_APP_API + "recommendation/publications?itemid=" + query_id).json()
    logger.info(req)


    result_list = req.get("body").values()
    logger.info(">>>>>>>>> RESULT LIST %s", result_list)

    if len(result_list)==0:
        error_message = "No recommendations found for query: {}".format(query_id)
        return render_template('query.html', error_message=error_message)

    id_list = [doc["docid"] for doc in result_list]
    logger.info(">>>>>>>>> ID LIST %s", id_list)

    results = doc_list(id_list)
    logger.info(">>>>>>>>> Retrieved %s results for query: %s", len(results), query_id)
    
    session_start_date = datetime.datetime.now()
    session_end_date = session_start_date + datetime.timedelta(seconds=300)
    rec_id = req.get("header").get("rid")
    logger.info(f"first rec_id: {rec_id}")

    click_dict = req.get("body")
    click_dict = {
        key: {
            "docid": val.get("docid"),
            "system": val.get("type"),
            "clicked": False,
            "date": None,
        }
        for key, val in req.get("body", {}).items()
    }

    session_id = session.get('session_id')
    clicked_query = request.args.get('query')
    logger.info(f"Session ID: {session_id}, Clicked on article with PMID: {clicked_query}")
    for key, val in click_dict.items():
            if val.get("docid") == clicked_query:
                val["clicked"] = True  # Mark as clicked
                val["date"] = session_start_date.strftime("%Y-%m-%d %H:%M:%S")
    payload = {
            "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "interleave": True,
            "clicks": json.dumps(click_dict),

        }
    logger.info(f"Feedback payload: {payload}")

    req = requests.post(
            STELLA_APP_API + "recommendation/" + str(rec_id) + "/feedback", data=payload
        )
    logger.info(f"Response fo feedback API: {req}")
    page = request.args.get('page', 1, type=int)
    per_page = 10

    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(results))

    paginated_data = results[start_index:end_index]

    content = []
    for recom in paginated_data:
        pmid = recom['pmid']
        title, abstract = recom['title'], recom['abstract']
        content.append([pmid, title, abstract])
    logging.info(content)
    title, abstract = get_text(query_id)
    logging.info(title, abstract)
    total_pages = (len(results) + per_page - 1) // per_page
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return render_template('query.html', query=query_id, title=title, abstract=abstract, content=content, per_page=per_page, 
                            page=page, start_index=start_index, end_index=end_index, total_pages=total_pages, 
                            prev_page=prev_page, next_page=next_page)

def get_text(query_id):
    data = Publications.query.filter_by(PMID=query_id).first()
    title = data.title if data else None
    abstract = data.abstract if data else None
    return title, abstract

@app.route('/log', methods=['GET'])
def log_queries():
    global click_dict, session_start_date, session_end_date, rec_id
    session_id = session.get('session_id')
    clicked_query = request.args.get('query')
    logger.info(f"Session ID: {session_id}, Clicked on article with PMID: {clicked_query}")
    for key, val in click_dict.items():
        logger.info(val)
        if int(val["docid"]) == int(clicked_query):
            logger.info("clicked paper")
            val["clicked"] = True
            logger.info(val)
            val["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Updated click_dict for docid {clicked_query}: {val}")

    # Prepare and send feedback payload
    payload = {
        "start": session_start_date.strftime("%Y-%m-%d %H:%M:%S"),
        "end": session_end_date.strftime("%Y-%m-%d %H:%M:%S"),
        "interleave": True,
        "clicks": json.dumps(click_dict),
    }
    logger.info(f"Feedback payload: {payload}")

    feedback_url = f"{STELLA_APP_API}recommendation/{rec_id}/feedback"
    response = requests.post(feedback_url, data=payload)
    logger.info(f"Feedback sent to {feedback_url}, response: {response.status_code}")

    return '', 204

@app.route('/pmid-list')
def pmid_list():
    all_pmids = {recommendation.PMID for recommendation in Recommendations.query.all()}
    return render_template('pmid_list.html', pmids=list(all_pmids))


if __name__ == '__main__':
    file = "./data/relish_text.jsonl"
    logger.info(">>>>>>>>> FILE %s", file)
    corpus = index_data(file)
    app.run(debug=True, host='0.0.0.0', port=5000)


