# serve angular apps
for PRs and stuff

## installation
* use python v3.7+
* create venv : `python -m venv virtual`
* activate venv : `source venv/bin/activate`
* install packages : `pip install -r requirements.txt`

## usage
* run flask app with `python app.py`
* hit endpoint `http://localhost:8800/start` to start angular app,
it gives you the port number of where the app is running
* visit `http://localhost:1234` to view the angular app
* hti endpoint `http://localhost:8800/stop/1234` to stop angular app running on port `1234`