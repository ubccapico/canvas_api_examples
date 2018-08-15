# -*- coding: utf-8 -*-
import json

# getpass and input are simple ways to get user input
import getpass

import requests
import pandas as pd
from builtins import input

# Static settings
# Using a base urls is useful for switching between test and production environments easily
BASE_URL = 'https://canvas.ubc.ca'
PER_PAGE = 100

# User input settings
# token should be treated as a password (not visible when typed)
token = None
while not token:
    token = getpass.getpass('Enter your access token:')
auth_header = {'Authorization': 'Bearer ' + token} # setup the authorization header to be used later

# require the course state to be provided
course_state = None
while not course_state in ['unpublished', 'available', 'completed', 'deleted']:
    course_state = input("Select a course state [unpublished, available, completed, deleted]:")


print("Finding courses...")
print("-----------------------------")
# continue to make requests until all data has been received
page = 1
courses = []
while True:
    # request urls should always be based of the base url so they do not
    # need to be changed when switching between test and production environments
    request_url = BASE_URL + '/api/v1/courses'
    params = {
        "per_page": str(PER_PAGE),
        "page": str(page),
        "state[]": [course_state],
        "include[]": ['total_students']
    }
    r = requests.get(request_url, headers=auth_header, params=params)

    # always take care to handle request errors
    r.raise_for_status() # raise error if 4xx or 5xx

    data = r.json()
    if len(data) == 0:
        break

    courses += data

    print("Finished processing page: "+str(page))
    page+=1

if len(courses) == 0:
    print("No courses found to report on.")
    exit()

# from here, a simple table is printed out
# using pandas for convenience
print("Report for "+str(len(courses)) + " courses.")
print("-----------------------------")

courses_df = pd.DataFrame(courses)
result = courses_df.to_string(
    columns=['id', 'name', 'course_code', 'workflow_state', 'start_at', 'end_at', 'total_students']
)
print(result)