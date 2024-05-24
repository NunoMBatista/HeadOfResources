import flask
import logging
import psycopg2
import time
import jwt
from psycopg2.extras import RealDictCursor

from global_functions import db_connection, logger, StatusCodes

def daily_summary(date_str):
    # Write to debug log
    logger.debug(f'GET /daily_summary/{date_str}')
    
    # Connect to the database
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        with open('queries/daily_summary.sql', 'r') as f:
            query = f.read()
            cur.execute(query, (date_str, date_str, date_str))
        
        summary = cur.fetchall()
        
        response = {
            'status': StatusCodes['success'],
            'errors': None,
            'response': summary
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'GET /daily_summary/{date_str} - {error}')
        response = {
            'status': StatusCodes['internal_error'],
            'errors': str(error)
        }
        return flask.jsonify(response)
    
    finally:
        if conn is not None:
            conn.close()
            cur.close()
            
        return flask.jsonify(response)