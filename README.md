## Pawfect Match ##

For best results with managing dependencies, running, and editing files:
* Install [Docker](https://docs.docker.com/install/overview/)
* In your command-line, run `docker build -t pawfect .`
* You may or may not need `sudo` for all docker commands
* Spin up a docker container with a bind mount to the `site` folder:
  * While **in the pawfect-match repo folder**: `docker run -d --name pawfect-site -v "$(pwd)"/site:/pawfect/site/ -p 5000:5000 pawfect`
  * Your container is now running in the background.
  * Inside the container, the flask app is being served to `localhost:5000` and that port is "linked" to your computer's port 5000.
  * There is a folder `/pawfect/site` inside the container that has everything that your current `/site folder` contains.
  * If you want to interact with the container, changed the `-d` (detached) to `-it` (interactive).
* You can now visit the site at `http://localhost:5000` and edit files in `pawfect-match/site` as normal.
