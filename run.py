import os
import json
import pandas as pd
import logging
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Integer
from sqlalchemy.sql import func
from flask import render_template, request
from app.models import Recommendations, Publications
from app.config import app, db
from uuid import uuid4

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Logging Configuration
LOG_FILE_PATH = "system_log.log"
logging.basicConfig(filename=LOG_FILE_PATH,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    session_id = session.get('session_id') or str(uuid4())
    logger.info(f'{session_id} - Session started ')
    session['session_id'] = session_id

    return render_template('index.html', session_id=session_id)

@app.route('/query', methods=['GET'])
def search_query():
    query_id = request.args.get('query')
    session_id = session.get('session_id')
    session_data = {
        'session_id': session.get('session_id'),  # Get the session ID
        'query': query_id  # Include the query in the session data
    }
    logger.info(f'{session_id} - Search initiated for query: {query_id}')
    # save_queries(session_data)

    data = Recommendations.query.filter_by(PMID=query_id).all()

    if len(data)==0:
        error_message = "No recommendations found for query: {}".format(query_id)
        return render_template('query.html', error_message=error_message)

     # Pagination settings
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Calculate the start and end indices for pagination
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(data))

    # Get the subset of recommendations for the current page
    paginated_data = data[start_index:end_index]

    content = []
    for recom in paginated_data:
        pmid = recom.target_pmid
        title, abstract = get_text(pmid)
        recom_number = recom.recom_number
        relevance = recom.relevance
        content.append([pmid, title, abstract, recom_number, relevance])

    title, abstract = get_text(query_id)

    # Calculate pagination information
    total_pages = (len(data) + per_page - 1) // per_page
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
    session_id = session.get('session_id')
    query = request.args.get('query')

    # For demonstration purposes, I'll just print the session ID and query
    logger.info(f"Session ID: {session_id}, Clicked on article with PMID: {query}")
    return '', 204


if __name__ == '__main__':
    if os.environ.get('FLASK_PORT'):
        app.run(debug=True, host='localhost', port=int(os.environ.get('FLASK_PORT')))
    else:
        app.run(debug=True, host='localhost', port=5001)


