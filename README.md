## Assignment

#  Assumption:

## "rbcapp1" is a critical application that needs to be monitored and its status should be 
## recorded into Elasticsearch. This Application depends on 3 services: httpd, rabbitMQ and
## postgreSQL .If any of these services are down, "rbcapp1" state will be considered "DOWN" otherwise it is "UP".
## Notes:
· Assume all these services runs under Linux machines

To monitor the status of the "rbcapp1" application and its dependent services (httpd, RabbitMQ, and PostgreSQL) on Linux 
machines and record their status into Elasticsearch, you can utilize various tools and techniques. One approach involves
using shell scripting and tools like systemctl to check service statuses and then sending the status information to 
Elasticsearch using a scripting language like Python.

Here's a conceptual outline of how you might achieve this:

1. Bash Script to Check Service Status:
Write a Bash script that uses systemctl commands to check the status of each service (httpd, rabbitMQ, postgreSQL) on the 
Linux machines where they are running. This script can perform checks periodically using a cron job or a monitoring tool.
eg: (check_services.sh):

2. Python Script to Send Status to Elasticsearch:
Write a Python script that reads the output/status from the Bash script and sends this information to Elasticsearch using 
the appropriate Elasticsearch client library (e.g., elasticsearch library for Python).

eg (send_to_elasticsearch.py using elasticsearch library):

Execution Flow:
Run the Bash script check_services.sh to obtain the status of the services.
Use a scheduling tool (like cron) to periodically execute the Python script send_to_elasticsearch.py that sends the 
obtained status to Elasticsearch.
Adjust the script logic and Elasticsearch configurations based on  specific environment and Elasticsearch setup to 
effectively monitor and record the status of the "rbcapp1" application and its dependent services.

## TEST1: Assume all services are running on the same server as Linux services.
## a) Write a Python script that monitors these services and creates a JSON object with
## application_name, application_status and host_name.
## Sample JSON Payload
{
 "service_name":"httpd",
 "service_status":"UP",
 "host_name":"host1"
}
## Write this JSON object to a file named {serviceName}-status-{@timestamp}.json

Python script monitor_service.py that monitors the services (httpd, rabbitMQ, postgreSQL) on the local machine, creates 
JSON objects for each service status, and writes these objects to separate JSON files named {serviceName}-status-{@timestamp}.json:

This script uses subprocess to call systemctl is-active <service_name> to retrieve the status of each service. It then creates 
JSON objects containing service name, status, and hostname, and writes them to separate JSON files with timestamped filenames as specified.
Execute this Python script on the Linux machine where these services are running to monitor their statuses and create the
corresponding JSON files. Adjust the services list according to the actual services you want to monitor.

## TEST1:b)
## Write a simple Python REST webservice that:                                                                                                                                               
## Accepts the above created JSON file and writes it to Elasticsearch 
## Provide a second endpoint where the data can be retrieved, i.e
## POST /add to Insert payload into Elasticsearch
## GET /healthcheck --> Return the all Application status (“UP” or “DOWN”)
## GET /healthcheck/{serviceName} --> Return the specific Application status (“UP” or “DOWN”)
Sample calls
https://myservice.example.com/add
https://myservice.example.com/healthcheck
https://myservice.example.com/healthcheck/httpd

To create a simple Python REST web service that accepts JSON files, writes them to Elasticsearch, and provides endpoints 
for retrieving application statuses, you can use Flask for creating the web service and the Elasticsearch client library to interact with Elasticsearch. Below is an example demonstrating this:

Firstly, ensure you have Flask and the Elasticsearch library installed. You can install them via pip:
pip install flask elasticsearch
Next, you can create a Flask application with the specified endpoints in monitor_service.py: 

This example creates a Flask web service with three endpoints:

POST /add: Accepts a JSON file upload and writes it to Elasticsearch.
GET /healthcheck: Retrieves statuses of all applications.
GET /healthcheck/{serviceName}: Retrieves the status of a specific application.
Make sure to replace <elasticsearch_host>:<port> with your Elasticsearch host and port.

For the file upload functionality, ensure that the UPLOAD_FOLDER directory exists and is writable by the application. 
Adjust the directory path to your desired location for storing uploaded files.

To test the endpoints, use tools like software like Postman, making POST requests to /add with the JSON file, and GET 
requests to /healthcheck and /healthcheck/{serviceName} to retrieve application statuses.

## TEST2:
## Assume the 3 services are running on different servers as RHEL services: httpd on host1, rabbitMQ on host2, postgreSQL on host3
## a) Create an Ansible inventory file for the above hosts that meets the monitoring needs explained above
## To create an Ansible inventory file for monitoring the three services (httpd, rabbitMQ, postgreSQL) running on different 
## hosts (host1, host2, host3), you can structure the Ansible inventory file as follows:

Create an inventory.ini file:

Explanation:

Each service is given its own group in the inventory file ([httpd], [rabbitMQ], [postgreSQL]).
Under each service group, specify the hostname(s) of the server(s) where that service is running. In this case, host1 for 
httpd, host2 for rabbitMQ, and host3 for postgreSQL.
This structure will allow you to organize hosts based on the services they are running. You can then create Ansible playbooks 
or roles to perform monitoring tasks or configurations specifically targeted at each service group or host.

This inventory file can be used as a basis for defining your Ansible playbook tasks for monitoring these services across 
multiple hosts. Adjust the playbook tasks as needed to monitor the services and perform checks across different servers 
based on their service roles.

## TEST2:
## b)Write an Ansible playbook that will action based on a provided variable named 
## "action":"action=verify_install": verifies the services are installed on their allocated hosts and if not,the playbook
## should install it. (for the install, please pick just one service to illustrate)  
## "action=check-disk" : with this action it should check the disk space on all servers and report any disk usage > 80%. 
## "action=check-status": with this action it should return the status of the application “rbcapp1” and a list of services 
## that are down. (you can use the REST endpoint created in TEST1.
## Below is a sample command to run the playbook
## ansible-playbook assignment.yml -i inventory -e action=verify_install ---- This is for verify
## install as an example    

Here is an example of an Ansible playbook (assignment.yml) that performs different actions based on the provided action 
variable: verify_install, check-disk, or check-status. For demonstration purposes, the playbook installs the httpd service 
on the host1 server when the action is set to verify_install.

Explanation:

The playbook consists of three main tasks sections corresponding to different actions based on the provided action variable.
For verify_install, it checks if httpd is installed on host1. If not, it installs the httpd package on host1.
For check-disk, it gathers disk facts using df -h command, checks if disk usage is over 80%, and triggers an alert if so (using the email_alert handler).
For check-status, it queries the rbcapp1 status and lists the services that are down using the REST endpoint created in TEST1.
The playbook includes a placeholder notify: email_alert for disk usage alerting. You need to define the email_alert handler 
in your playbook to send email alerts. Please configure the email functionality using Ansible's email-related modules or 
custom solutions based on your environment and requirements.

Run the playbook with different action variables using the command provided in your question:
bash:
ansible-playbook assignment.yml -i inventory -e action=verify_install

Replace action=verify_install with action=check-disk or action=check-status to perform different actions as per your requirement.
Adjust the playbook tasks and handlers as necessary for your environment and specific use case.


