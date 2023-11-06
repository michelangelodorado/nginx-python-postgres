import json
import psycopg2
import tailer

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='template1',
    user='postgres',
    password='default',
    host='localhost'
)
cursor = conn.cursor()

# Define the table schema for storing Nginx logs (if it doesn't exist)
create_table_query = '''
CREATE TABLE IF NOT EXISTS nginx_logs (
    id SERIAL PRIMARY KEY,
    time_local TIMESTAMP,
    remote_addr TEXT,
    remote_user TEXT,
    request TEXT,
    status INT,
    body_bytes_sent TEXT,
    http_referer TEXT,
    http_user_agent TEXT,
    http_apikey TEXT,
    api_client_name TEXT
);
'''
cursor.execute(create_table_query)

# Set the path to the Nginx access log file
log_file_path = '/var/log/nginx/access-2.log'

print("Monitoring Nginx access log...")

for line in tailer.follow(open(log_file_path)):
    # Parse the log data as JSON
    try:
        log_data = json.loads(line)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        continue  # Skip this log entry

    # Insert log data into the database
    cursor.execute(
        'INSERT INTO nginx_logs (time_local, remote_addr, remote_user, request, status, body_bytes_sent, http_referer, http_user_agent, http_apikey, api_client_name) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
        (log_data['time_local'], log_data['remote_addr'], log_data['remote_user'], log_data['request'], log_data['status'], log_data['body_bytes_sent'], log_data['http_referer'], log_data['http_user_agent'], log_data['http_apikey'], log_data['api_client_name'])
    )
    conn.commit()  # Commit changes to the database

# This part of the code will never be reached unless the script is explicitly stopped
cursor.close()
conn.close()
