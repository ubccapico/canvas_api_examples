Each Script will call the canvas api and print out a small report on all the courses the user has access to using the `/api/v1/courses` [endpoint](https://canvas.instructure.com/doc/api/courses.html#method.courses.index).

### Scripts Overview

The three scripts highlight some basic ways to use the Canvas API.

`simple_input.py` will request the Canvas access token as user input (as a password) along with sort order as an input.

`simple_env.py` will check environment variables for access token, sort order, per page, and the canvas base url. It will quit if not access token if provided or if sort order is not provided or valid (per page and base url will use default values if not found).

`robust.py` uses the [Click](https://github.com/pallets/click) library to check environment variables and take in user input. It also uses the [canvasapi](https://github.com/ucfopen/canvasapi) library to wrap around the Canvas api. This implementation is a bit more robust in that it uses the power of existing libraries to simplify the code.



### Running the Scripts

You must rather have [Python](https://www.python.org/downloads/) installed on your system or [Docker](https://www.docker.com/get-started).


You can use Docker to skip the python dependency. To setup an environment to run the example scripts, just run:
```
docker-compose run test bash
cd /code && pip install requirements.txt
```

if you aren't using docker, make sure to install the pip requirements with
```
pip install requirements.txt
```

From here both Python and Docker will run the scripts the same

#### simple_input.py

Run the script with
```
python simple_input.py
```

#### simple_env.py

Setup the environment variables with
```
export CANVAS_ACCESS_TOKEN=########
export CANVAS_SORT_BY=course_name
export CANVAS_URL=https://canvas.ubc.ca
export CANVAS_PER_PAGE=40
```

Run the script with
```
python simple_env.py
```

Remove the environment variables with
```
unset CANVAS_ACCESS_TOKEN
unset CANVAS_SORT_BY
unset CANVAS_URL
unset CANVAS_PER_PAGE
```



#### robust.py

Run the script with
```
python robust.py
```

You can also run with some environment variables:
```
export CANVAS_ACCESS_TOKEN=########
export CANVAS_SORT_BY=course_name
export CANVAS_URL=https://canvas.ubc.ca
export CANVAS_PER_PAGE=40

python robust.py

unset CANVAS_ACCESS_TOKEN
unset CANVAS_SORT_BY
unset CANVAS_URL
unset CANVAS_PER_PAGE
```

You can also pass variables from the command line
```
python robust.py --url=https://canvas.ubc.ca --per_page=40 --sort_by=course_name --token=########
```