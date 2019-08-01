import os
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager, login_user
import webbrowser


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '+xjtZo+YaAWKhCSky9nLCubHvPCjhRRxN45niWNVaN4='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crywolf.db')
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from forms import PrequestionnaireForm, SurveyForm, LoginForm

import models


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = models.User(userName = form.username.data)

        login_user(user, remember=True)

        flash('Logged in successfully.')

        return redirect(url_for('index'))
    return render_template('login.html', form=form)


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
    id = 1
    with open("testEvents.txt", "r") as inFile:
        for line in inFile:
            line = line.rstrip()
            line = line.split("\t")
            line.insert(0, str(id))    
            items.append(line)
            id += 1
    return render_template('experiment.html', table = items)

@app.route('/postsurvey', methods = ["GET", "POST"]) 
def postsurvey():
    form = SurveyForm()
    if form.validate_on_submit():
        responses = models.SurveyAnswers(
            mental = form.mental.data,
            physical = form.physical.data,
            temporal = form.temporal.data,
            performance = form.performance.data,
            effort = form.effort.data,
            frustration = form.frustration.data,
            useful_info = form.useful_info.data,
            feedback = form.feedback.data)
        db.session.add(responses)
        db.session.commit()
        return redirect(url_for('index')) 
    return render_template('postsurvey.html', form=form)

@app.route('/events/<eventData>')
def events(eventData):    
    return render_template('events.html', test = eventData)

if __name__ == "__main__":
    app.run(debug=True)