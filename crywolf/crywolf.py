import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import  SQLAlchemy
import webbrowser


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
        answers = models.PrequestionnaireAnswers(
            role = form.role.data,
            exp_researcher = form.exp_researcher.data,
            exp_admin = form.exp_admin.data,
            exp_software = form.exp_software.data,
            exp_security = form.exp_security.data,
            familiarity_none = form.familiarity_none.data,
            familiarity_read = form.familiarity_read.data,
            familiarity_controlled = form.familiarity_controlled.data,
            familiarity_public = form.familiarity_public.data,
            familiarity_engineered = form.familiarity_engineered.data,
            subnet_mask = form.subnet_mask.data,
            network_address = form.network_address.data,
            tcp_faster = form.tcp_faster.data,
            http_port = form.http_port.data,
            firewall = form.firewall.data,
            socket = form.socket.data,
            which_model = form.which_model.data)        
        db.session.add(answers)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('prequestionnaire.html', form=form)

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