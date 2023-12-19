from elasticsearch import Elasticsearch

# Create an Elasticsearch instance
es = Elasticsearch('<elasticsearch_host>:<port>')

# Read service statuses from Bash script output
# Replace these with actual statuses obtained from the Bash script
httpd_status = "active"
rabbitmq_status = "inactive"
postgresql_status = "active"

# Determine "rbcapp1" status based on services' statuses
if httpd_status != "active" or rabbitmq_status != "active" or postgresql_status != "active":
    rbcapp1_status = "DOWN"
else:
    rbcapp1_status = "UP"

# Store "rbcapp1" status in Elasticsearch
doc = {
    "application": "rbcapp1",
    "status": rbcapp1_status
}

# Index the status document into Elasticsearch
es.index(index='application_status', doc_type='status', body=doc)
