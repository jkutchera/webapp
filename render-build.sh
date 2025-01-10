#!/bin/bash
set -x

# Install prerequisites
apt-get update && apt-get install -y curl gnupg2

# Add Microsoft package signing key and repository
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install the ODBC driver
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
