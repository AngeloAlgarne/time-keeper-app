# Time Tracker App

A simple time tracker app for projects using dockerized django-rest, reactjs, and postgresql. Note that production for this project has not been setup.

Users can create a new project, start the time tracker, and once it's completed, see the final stats of the project, such as the date of when it was created, completed, and the total elapsed hours of the project.

## Requirements

To run the dockerized application, you must first have docker installed. Visit the link https://docs.docker.com/engine/install/ to know more. You can also install Docker Desktop for easier use, which will install the Docker Engine as well.

## Installation

- Clone this repository in your local directory by running: `git clone https://github.com/AngeloAlgarne/time-tracker-app.git`. 
	- You can also fork this repo beforehand if you may.
- Open the root folder of the cloned repo in the terminal.
- In the terminal, run the command: `docker compose up` to run the app using docker.
	- Please note that the `reactjs` container will take the longest time to load. It will be a hot minute before it completely loads in.

## Development

To continue the development, you must first have `NodeJS`, `Python`, and `PostgreSQL` installed in your device. Development inside the docker containers are not doable for this project.

Note that you need to change the `HOST` inside `backend/backend/.env` to `localhost` in order to use your local postgres. Additionally, you need to setup the database `timetracker_db` in your local postgres first, before Django can  connect to it.