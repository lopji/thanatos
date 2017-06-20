from flask import request,Flask,render_template,session,g,Response
import glob
import MySQLdb
import urllib
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def show(data):
	return json.dumps(data)
	
@app.route('/', methods=['POST'])
def default():
	data = {'status' : 200, 'y' : [0,1]}
	print request.form['tweet']
	return show(data)
	
app.config['DEBUG'] = True
app.run()
