from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from sqlalchemy.sql import text
from sqlalchemy import and_, or_
import csv
import io
from flask import Response
from datetime import datetime
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DatabaseCredentials', 'username')
password = config.get('DatabaseCredentials', 'password')
host = config.get('DatabaseCredentials', 'host')
port = config.get('DatabaseCredentials', 'port')
database = config.get('DatabaseCredentials', 'database')

encoded_password = quote(password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{encoded_password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/") 
def index(): 
    return render_template('home.html')

@app.route('/view_execution_history', methods=['GET'])
def view_execution_history():
    search_process = request.args.get('search_process', default='', type=str)
    status_filter = request.args.get('status_filter', default='', type=str)
    date_start = request.args.get('date_start', default=None, type=str)
    date_end = request.args.get('date_end', default=None, type=str)
    page = request.args.get('page', default=1, type=int)

    items_per_page = 100

    # Building the SQL query with user filters
    query = 'SELECT * FROM "A2AMON"."A2A_EXECUTION_HISTORY" WHERE 1=1'

    if search_process:
        query += f" AND process_name LIKE '%%{search_process}%%'"

    if status_filter:
        query += f" AND execution_status = '{status_filter}'"

    if date_start:
        query += f" AND execution_start >= '{date_start}'"

    if date_end:
        query += f" AND execution_start <= '{date_end}'"

    # Add LIMIT and OFFSET for pagination
    query += f" ORDER BY execution_start DESC LIMIT {items_per_page} OFFSET {(page - 1) * items_per_page};"

    with db.engine.connect() as connection:
        result = connection.execute(text(query))
        all_execution_records = []

        for row in result:
            record = {
                'process_name': row[0],
                'execution_status': row[1],
                'execution_start': row[2],
                'execution_end': row[3],
                'execution_duration': row[4],
                'WHEN_INSERTED': row[5],
                'message_guid': row[6],
            }
            all_execution_records.append(record)

    # Get the total number of records for pagination
    count_query = 'SELECT COUNT(*) FROM "A2AMON"."A2A_EXECUTION_HISTORY" WHERE 1=1'

    if search_process:
        count_query += f" AND process_name LIKE '%%{search_process}%%'"

    if status_filter:
        count_query += f" AND execution_status = '{status_filter}'"

    if date_start:
        count_query += f" AND execution_start >= '{date_start}'"

    if date_end:
        count_query += f" AND execution_start <= '{date_end}'"
    count_query += ';'

    with db.engine.connect() as connection:
        total_records = connection.scalar(text(count_query))
        total_pages = (total_records // items_per_page) + int(bool(total_records % items_per_page))

    return render_template('execution_history.html', records=all_execution_records, page=page, total_pages=total_pages)


@app.route('/view_integration_content', methods=['GET'])
def view_integration_content():
    query = text('SELECT * FROM "A2AMON"."A2A_IFLOW_DATA";')
    with db.engine.connect() as connection:
        result = connection.execute(query)
        iflow_data = []

        for row in result:
            record = {
                'id': row[0],
                'version': row[1],
                'package_id': row[2],
                'name': row[3],
                'description': row[4],
                'created_by': row[5],
                'created_at': row[6],
                'modified_by': row[7],
                'modified_at': row[8]
            }
            iflow_data.append(record)

    return render_template('iflow_data.html', records=iflow_data)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    search_process = request.args.get('search_process', default='', type=str)
    status_filter = request.args.get('status_filter', default='', type=str)
    date_start = request.args.get('date_start', default=None, type=str)
    date_end = request.args.get('date_end', default=None, type=str)

    # Building the SQL query with user filters
    query = 'SELECT * FROM "A2AMON"."A2A_EXECUTION_HISTORY" WHERE 1=1'

    if search_process:
        query += f" AND process_name LIKE '%%{search_process}%%'"

    if status_filter:
        query += f" AND execution_status = '{status_filter}'"

    if date_start:
        query += f" AND execution_start >= '{date_start}'"

    if date_end:
        query += f" AND execution_start <= '{date_end}'"
    query += ';'

    output = io.StringIO()
    writer = csv.writer(output)

    with db.engine.connect() as connection:
        result = connection.execute(text(query))

        writer.writerow(['Process Name', 'Execution Status', 'Execution Start', 'Execution End',
                         'Execution Duration', 'WHEN_INSERTED', 'Message GUID'])

        for row in result:
            record = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
            writer.writerow(record)

    # Get current date as a string
    current_date = datetime.now().date().strftime("%Y-%m-%d")

    # Set filename with the current_date
    filename = f"execution_history_{current_date}.csv"

    output.seek(0)
    return Response(output, content_type='text/csv', headers={"Content-Disposition": f'attachment; filename={filename}'})

if __name__ == '__main__':
    app.run(debug=True)