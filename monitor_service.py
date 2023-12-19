from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import json
import os
import datetime
import subprocess

app = Flask(__name__)
es = Elasticsearch('<elasticsearch_host>:<port>')  # Replace with your Elasticsearch host and port
def get_service_status(service_name):
    try:
        # Run systemctl status to get service status
        output = subprocess.check_output(["systemctl", "is-active", service_name])
        return output.decode().strip()  # Return the status (UP or DOWN)
    except subprocess.CalledProcessError as e:
        return "DOWN"  # If service check encounters an error, consider it DOWN


def create_json(service_name, service_status):
    # Create JSON object
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    json_data = {
        "service_name": service_name,
        "service_status": service_status,
        "host_name": os.uname().nodename
    }
    # Write JSON object to a file
    file_name = f"{service_name}-status-{timestamp}.json"
    with open(file_name, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print(f"Created {file_name} with status: {service_status}")


# Service names to monitor
services = ["httpd", "rabbitmq", "postgresql"]

# Monitor services and create JSON objects
for service in services:
    status = get_service_status(service)
    create_json(service, status)

@app.route('/add', methods=['POST'])
def add_to_elasticsearch():
    file = request.files['file']
    if file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        file_name = f"uploaded-file-{timestamp}.json"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            es.index(index='service_status', doc_type='status', body=data)
        return jsonify({'message': 'File uploaded successfully.'}), 200
    else:
        return jsonify({'error': 'File not found in the request.'}), 400


@app.route('/healthcheck', methods=['GET'])
def healthcheck_all():
    query = {"query": {"match_all": {}}}
    res = es.search(index='service_status', body=query)
    hits = res['hits']['hits']
    statuses = [hit['_source']['service_status'] for hit in hits]
    return jsonify({'status': statuses})


@app.route('/healthcheck/<service_name>', methods=['GET'])
def healthcheck(service_name):
    query = {"query": {"match": {"service_name": service_name}}}
    res = es.search(index='service_status', body=query)
    hits = res['hits']['hits']
    if hits:
        status = hits[0]['_source']['service_status']
        return jsonify({'service_name': service_name, 'status': status})
    else:
        return jsonify({'error': 'Service not found.'}), 404


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploaded_files'  # Specify the folder for uploaded files
    app.run(host='0.0.0.0', port=5000)  # Replace with your desired host and port
