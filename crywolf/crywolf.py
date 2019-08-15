import os
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import  SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '+xjtZo+YaAWKhCSky9nLCubHvPCjhRRxN45niWNVaN4='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crywolf.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from forms import PrequestionnaireForm, SurveyForm, UserForm, eventDecisionForm
import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

@app.route('/index',methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():

        login_user(models.User.query.filter_by(username = form.username.data).first(), remember=True)       
        return redirect(url_for('prequestionnaire'))
    return render_template('index.html', form=form, section = "Section title passed from View to Template",
                            text = "Text passed from View to Template")

@app.route('/prequestionnaire', methods = ["GET", "POST"])
@login_required
def prequestionnaire():    
    form = PrequestionnaireForm()
    if form.validate_on_submit():
        answers = models.PrequestionnaireAnswers(
            user = current_user.username,
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
        return redirect(url_for('training'))
    return render_template('prequestionnaire.html', form=form)

@app.route('/training')
@login_required
def training():
    ids = [1,2,3,4,5]

    eventsList = []
    for id in ids:
        eventsList.append(models.TrainingEvent.query.get(id))
    return render_template('training.html', eventsList=eventsList)

@app.route('/experiment')
@login_required
def experiment():
    ids = [x for x in range(1,91)]

    eventsList = []
    for id in ids:
        eventsList.append(models.Event.query.get(id))
    return render_template('test.html', eventsList=eventsList) #CHANGE BACK TO experiment.html!!!!

@app.route('/postsurvey', methods = ["GET", "POST"]) 
@login_required
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


@app.route('/trainingEventPage/<eventId>', methods = ["GET", "POST"])
@login_required
def trainingEventPage(eventId):
    event = models.TrainingEvent.query.get(eventId)    
    form = eventDecisionForm()
    if form.validate_on_submit():
        response = models.TrainingEventDecision(
            user=current_user.username,
            event_id = eventId,
            escalate = form.escalate.data,
            confidence = form.confidence.data
        )
        db.session.add(response)
        db.session.commit()
        return redirect(url_for("training"))
    return render_template('trainingEventPage.html', event = event, form=form)


@app.route('/eventPage/<eventId>', methods = ["GET", "POST"])
@login_required
def eventPage(eventId):
    event = models.Event.query.get(eventId)
    form = eventDecisionForm()

    if request.method == 'GET':
        print("GET")
        # TODO: Log a database entry that an event was clicked on       
    else:
        print("POST")
        if form.validate_on_submit():           
            response = models.EventDecision(
                user=current_user.username,
                event_id = eventId,
                escalate = form.escalate.data,
                confidence = form.confidence.data,
                time_event_click = time_event_click,
                time_event_decision = datetime.datetime.now()
            )
            
            db.session.add(response)
            db.session.commit()
            return redirect(url_for("experiment"))
    return render_template('eventPage.html', event = event, form=form)


@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

if __name__ == "__main__":
    app.run(debug=True)