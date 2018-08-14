from flask import Flask, render_template, request, url_for, redirect
from json import loads, dumps
import apiUtil

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', client_form=False, data_form=False, info=None)

@app.route('/search/', methods=["GET", "POST"])
def search():
	result = request.form
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
	print result["name"]
	print ""
	data = apiUtil.findClient(result["name"])
	print data
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"
	return render_template('index.html', client_form=True, data_form=False, info=data)
	
	'''if (d["type"] == "clientForm"):
		answer = apiUtil.findClient(form["name"])
		return render_template
	'''
            

if __name__ == '__main__':
    app.debug = True
    app.run()
