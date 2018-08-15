# -*- coding: utf-8 -*-
import dotenv
import json

# os is a simple way to access environment variables
import os

import click # used for easily collecting user input more robustly
import requests
import canvasapi # used to easily call Canvas API endpoints
import pandas as pd

# load variables from .env file
dotenv.load_dotenv(dotenv.find_dotenv())
# Using a command line library like click allows for easily
# setting up the scripts settings with default values,
# ways to set values in the command line, and forcing
# certain inputs like access token to be provided securely
@click.command()

# Will check `CANVAS_COURSE_STATE` environment variable for course state first.
# If not found, user can input state in the command line via `--state=available`
# or they will prompted after running the command
# restricted to what values are allowed
@click.option('--state', help='Course state. [unpublished, available, completed, deleted]',
    type=click.Choice(['unpublished', 'available', 'completed', 'deleted']),
    prompt='Select a course state [unpublished, available, completed, deleted]',
    required=True, envvar='CANVAS_COURSE_STATE')

# Will check `CANVAS_URL` environment variable for Canvas base url first.
# If not found, user can input url in the command line via `--url=https://example.com`
# default values is `https://canvas.ubc.ca` production
@click.option('--url', help='Canvas Url. [default: https://canvas.ubc.ca]',
    default='https://canvas.ubc.ca', envvar='CANVAS_URL')

# Will check `CANVAS_PER_PAGE` environment variable for Canvas base url first.
# If not found, user  can input per_page in the command line via `--per_page=200`
# default values is `100`
@click.option('--per_page', help='How many courses to fetch per page. [default: 100]',
    default=100, type=int, envvar='CANVAS_PER_PAGE')
def view_course_report(url, state, per_page):

    # ensure access token is available
    TOKEN = os.environ.get('CANVAS_ACCESS_TOKEN')
    while not TOKEN:
        TOKEN = click.prompt("Enter your access token", hide_input=True)

    # create a canvas api handler for all requests
    # by using a Canvas API library, we no longer need to
    # worry about keeping track of the authorization header
    # or request urls in our code
    canvas_api = canvasapi.Canvas(url, TOKEN)

    click.echo("Finding courses...")
    click.echo("-----------------------------")

    paginated_courses = canvas_api.get_courses(
        per_page=per_page,
        state=[state],
        include=['total_students']
    )

    # fetch all courses (unwrap PaginatedList)
    # this is a particular quirk of the canvasapi library
    # it will only fetch pages are they are needed so
    # we need to loop though it all to fetch everything
    # before sending the data to Pandas
    courses = [course.attributes for course in paginated_courses]

    if len(courses) == 0:
        click.echo("No courses found to report on.")
        return

    # from here, a simple table is printed out
    # using pandas for convenience
    click.echo("Report for "+str(len(courses)) + " courses.")
    click.echo("-----------------------------")

    courses_df = pd.DataFrame(courses)
    result = courses_df.to_string(
        columns=['id', 'name', 'course_code', 'workflow_state', 'start_at', 'end_at', 'total_students']
    )
    click.echo(result)

if __name__ == '__main__':
    view_course_report()