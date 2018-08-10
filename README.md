The goal of this repository is to provide small examples of Canvas API usage along with pointing out some security best practices.

## API Scripts

API Scripts should primarily be used for automating regular tasks, running occasional one offs, or possibly collecting data for research purposes. The bottom line is that they should generally not require to much user input/action. If your task does require a large amount of user input/action, consider building a web application instead.

#### API Script Security Guidelines

The two most import security considerations are to ensure that Canvas access tokens are **secure** and that any data collected by the script is **secure**.

Scripts **MUST** follow these guidelines:
- Access tokens **MUST** never be stored in the scripts or repositories.
- Access tokens **MUST** never be stored, distributed, or displayed in any way by a script.
- Access tokens **MUST** be treated as a password when being entered via user input.
- Access tokens **SHOULD** not be stored in plain text in the file system (it is preferred to use secure secret storage system and/or environment variables)
- Data collected **MUST** follow UBC's data security guidelines (TODO: add link)


#### API Example Scripts

[Python Example Scripts](api_scripts/python)

JavaScript Example Scripts - TODO

