#!/bin/bash

# Check httpd status
httpd_status=$(systemctl is-active httpd)
echo "httpd status: $httpd_status"

# Check RabbitMQ status
rabbitmq_status=$(systemctl is-active rabbitmq)
echo "RabbitMQ status: $rabbitmq_status"

# Check PostgresSQL status
postgresql_status=$(systemctl is-active postgresql)
echo "PostgresSQL status: $postgresql_status"
