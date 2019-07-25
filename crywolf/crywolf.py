import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import  SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '+xjtZo+YaAWKhCSky9nLCubHvPCjhRRxN45niWNVaN4='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crywolf.db')
db = SQLAlchemy(app)

from forms import PrequestionnaireForm
import models

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', section = "Section title passed from View to Template",
                            text = "Text passed from View to Template")

@app.route('/prequestionnaire', methods = ["GET", "POST"])
def prequestionnaire():
    form = PrequestionnaireForm()
    if form.validate_on_submit():
        one = form.one.data
        twoA = form.twoA.data
        twoB = form.twoB.data
        twoC = form.twoC.data
        twoD = form.twoD.data
        threeA = form.threeA.data
        threeB = form.threeB.data
        threeC = form.threeC.data
        threeD = form.threeD.data
        threeE = form.threeE.data
        four = form.four.data
        five = form.five.data
        six = form.six.data
        seven = form.seven.data
        eight = form.eight.data
        nine = form.nine.data
        ten = form.ten.data
        answers = models.PrequestionnaireAnswers(
            one = one,
            twoA = twoA,
            twoB = twoB,
            twoC = twoC,
            twoD = twoD,
            threeA = threeA,
            threeB = threeB,
            threeC = threeC,
            threeD = threeD,
            threeE = threeE,
            four = four,
            five = five,
            six = six,
            seven = seven,
            eight = eight,
            nine = nine,
            ten = ten)
        db.session.add(answers)
        db.session.commit()
        return redirect(url_for('index'))
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