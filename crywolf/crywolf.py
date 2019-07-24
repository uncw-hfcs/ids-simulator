import os
from flask import Flask, render_template, url_for
from flask_sqlalchemy import  SQLAlchemy
from events import EventsTable, EventItem

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join.(basedir, 'crywolf.db')
#db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', section = "Section title passed from View to Template",
                            text = "Text passed from View to Template")

@app.route('/prequestionnaire')
def prequestionnaire():
    return render_template('prequestionnaire.html')

@app.route('/experiment')
def experiment():
    items = []
    with open("test_content.txt", "r") as inFile:
        for line in inFile:
            line = line.rstrip()
            id,date,classification,s_ip,s_port,d_ip,d_port,description = line.split("\t")
            items.append((id,date,classification,s_ip,s_port,d_ip,d_port,description))#EventItem(id,date,classification,s_ip,s_port,d_ip,d_port,description))
    #eventsTable = EventsTable(items, classes = ['container'], border = True)
    return render_template('experiment.html', table = items)#eventsTable)

@app.route('/postsurvey') 
def postsurvey():
    return render_template('postsurvey.html')

@app.route('/events/<eventData>')
def events(eventData):    
    return render_template('events.html', test = eventData)

if __name__ == "__main__":
    app.run(debug=True)