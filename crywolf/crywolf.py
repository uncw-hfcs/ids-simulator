import os
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
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
        user = models.User.query.filter_by(username = form.username.data).first()
        if user is None:
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('prequestionnaire'))
    return render_template('index.html', form=form)

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
        # user = models.User.query.filter_by(username = current_user.username).first()
        # local_user = db.session.merge(user)
        # local_user.questionnaire_complete = True  
        db.session.add(answers)#, local_user)
        db.session.commit()
        return redirect(url_for('training'))
    return render_template('prequestionnaire.html', form=form)

@app.route('/training')
@login_required
def training():
    ids = [1,2,3,4,5]

    eventsList = []   #This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((models.TrainingEvent.query.get(id),
                          models.TrainingEventDecision.query.filter_by(user = current_user.username, event_id = id).
                            order_by(models.TrainingEventDecision.time_event_decision.desc()).first())
                         )
    return render_template('training.html', eventsList=eventsList)

@app.route('/experiment')
@login_required
def experiment():
    
    user = models.User.query.filter_by(username = current_user.username).first()
    # if request.method == "GET" and user.training_complete == False:
    #     local_user = db.session.merge(user)
    #     local_user.training_complete = True 
    #     db.session.add(local_user)
    #     db.session.commit()

    if request.method == "GET" and user.time_begin == None:
        local_user = db.session.merge(user)
        local_user.time_begin = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit()
    

    ids = [int(id) for id in current_user.events.split(",")]
    ids.insert(43,73)
    ids.insert(25, 72)

    eventsList = []   #This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((models.Event.query.get(id),
                          models.EventDecision.query.filter_by(user = current_user.username, event_id = id).
                            order_by(models.EventDecision.time_event_decision.desc()).first())
                         )
    return render_template('experiment.html', eventsList=eventsList) 

@app.route('/postsurvey', methods = ["GET", "POST"]) 
@login_required
def postsurvey():

    user = models.User.query.filter_by(username = current_user.username).first()
    # if request.method == "GET" and user.experiment_complete == False:
    #     local_user = db.session.merge(user)
    #     local_user.training_complete = True 
    #     db.session.add(local_user)
    #     db.session.commit()

    if request.method == "GET" and user.time_end == None:
        local_user = db.session.merge(user)
        local_user.time_end = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit()

    form = SurveyForm()
    if form.validate_on_submit():
        responses = models.SurveyAnswers(
            user = current_user.username,
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
        return redirect(url_for('logout')) 
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
            confidence = form.confidence.data,
            time_event_decision = datetime.datetime.now()
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
        newEvent = models.EventClicked(
            user = current_user.username,
            event_id = eventId,
            time_event_click = datetime.datetime.now()
        )   
        db.session.add(newEvent)
        db.session.commit()    
    else:
        if form.validate_on_submit():           
            response = models.EventDecision(
                user=current_user.username,
                event_id = eventId,
                escalate = form.escalate.data,
                confidence = form.confidence.data,
                time_event_decision = datetime.datetime.now()
            )            
            db.session.add(response)
            db.session.commit()
            return redirect(url_for("experiment"))
    return render_template('eventPage.html', event = event, form=form)

@app.route("/reference")
def reference():
    return render_template('reference.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

if __name__ == "__main__":
    app.run(debug=True)