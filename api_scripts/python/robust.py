# -*- coding: utf-8 -*-
import json

import click # used for easily collecting user input more robustly
import requests
import canvasapi # used to easily call Canvas API endpoints
import pandas as pd

# Using a command line library like click allows for easily
# setting up the scripts settings with default values,
# ways to set values in the command line, and forcing
# certain inputs like access token to be provided securely
@click.command()

# token should be input like a password. Will check `CANVAS_ACCESS_TOKEN`
# environment variable for token. If not found, user can input in the command line
# via `--token=###` or they will be prompted after running the command
@click.option('--token', help='Canvas API token.', hide_input=True,
    prompt='Enter your access token',required=True, envvar='CANVAS_ACCESS_TOKEN')

# Will check `CANVAS_SORT_BY` environment variable for sort order first.
# If not found, user can input sort_by in the command line via `--sort_by=course_name`
# or they will prompted after running the command
# restricted to what values are allowed
@click.option('--sort_by', help='Course a sort order. [course_name, sis_course_id, teacher, account_name]',
    type=click.Choice(['course_name', 'sis_course_id', 'teacher', 'account_name']),
    prompt='Select a sort order [course_name, sis_course_id, teacher, account_name]',
    required=True, envvar='CANVAS_SORT_BY')

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
def view_course_report(url, token, sort_by, per_page):
    # create a canvas api handler for all requests
    # by using a Canvas API library, we no longer need to
    # worry about keeping track of the authorization header
    # or request urls in our code
    canvas_api = canvasapi.Canvas(url, token)

    click.echo("Finding courses...")
    click.echo("-----------------------------")

    paginated_courses = canvas_api.get_courses(
        per_page=per_page,
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