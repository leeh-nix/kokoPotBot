#!/bin/bash

# Remember to setup **.env** file before running this script

# Install the dependencies
pip install -r requirements.txt

# Run the project in an ec2 instance
pm2 start main.py --name "kokosbot" --interpreter python