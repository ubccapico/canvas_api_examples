# -*- coding: utf-8 -*-
import dotenv
import json

# os is a simple way to access environment variables
import os

import requests
import pandas as pd

# load variables from .env file
dotenv.load_dotenv(dotenv.find_dotenv())

# Static settings
# Using a base urls is useful for switching between test and production environments easily
BASE_URL = os.environ.get('CANVAS_URL', 'https://canvas.ubc.ca')
PER_PAGE = int(os.environ.get('CANVAS_PER_PAGE', '100'))

# ensure access token is available
TOKEN = os.environ.get('CANVAS_ACCESS_TOKEN')
if TOKEN == None:
    print("No access token found. Please set `CANVAS_ACCESS_TOKEN`")
    exit()
auth_header = {'Authorization': 'Bearer ' + TOKEN} # setup the authorization header to be used later

# ensure that COURSE_STATE is valid
COURSE_STATE = os.environ.get('CANVAS_COURSE_STATE')
if not COURSE_STATE in ["unpublished", "available", "completed", "deleted"]:
    print("Invalid course state. Please set `CANVAS_COURSE_STATE` to one of [unpublished, available, completed, deleted]")
    exit()

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
        "state[]": [COURSE_STATE],
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