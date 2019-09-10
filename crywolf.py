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

login_manager.login_view = "unauthorized"

@app.route('/unauthorized')
def unauthorized():
    return render_template('401.html')

@app.route("/reference")
def reference():
    return render_template('reference.html')

#---------------------------Index-------------------------------------
@app.route('/index',methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('intro'))
        
    error = None
    form = UserForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username = form.username.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('intro'))
        else:
            error = "Invalid username. Please try again."
        
    return render_template('index.html', form=form, error = error)
#---------------------------------------------------------------------
#---------------------------Landing Page------------------------------
@app.route("/intro", methods=["GET"])
@login_required
def intro():
    return render_template("intro.html")
#---------------------------------------------------------------------
#---------------------------Questionnaire-----------------------------
@app.route('/prequestionnaire', methods = ["GET", "POST"])
@login_required
def prequestionnaire(): 
    form = PrequestionnaireForm()
    if form.validate_on_submit():
        answers = models.PrequestionnaireAnswers(
            timestamp = datetime.datetime.now(),
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
            firewall = form.security_device.data,
            socket = form.ip_port.data,
            which_model = form.which_model.data
            )    
        user = models.User.query.filter_by(username = current_user.username).first()
        local_user = db.session.merge(user)
        local_user.questionnaire_complete = True  
        db.session.add(answers, local_user)
        db.session.commit()
        flash("Questionnaire saved successfully!")
        return redirect(url_for('training'))
    return render_template('prequestionnaire.html', form=form)
#---------------------------------------------------------------------
#---------------------------Training Page-----------------------------
@app.route('/training', methods = ["GET", "POST"])
@login_required
def training():
    # ids = [1,2,3,4,5]
    ids = [1, 2]
    if request.method == "GET":
        num_processed_alerts = 0
        for id in ids:
            if models.TrainingEventDecision.query.filter_by(user = current_user.username, event_id = id).\
                            order_by(models.TrainingEventDecision.time_event_decision.desc()).first() != None:
                num_processed_alerts += 1
    eventsList = []   #This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((models.TrainingEvent.query.get(id),
                          models.TrainingEventDecision.query.filter_by(user = current_user.username, event_id = id).
                            order_by(models.TrainingEventDecision.time_event_decision.desc()).first())
                         )
    user = models.User.query.filter_by(username = current_user.username).first()
    if request.method == "POST":
        local_user = db.session.merge(user)
        local_user.training_complete = True 
        db.session.add(local_user)
        db.session.commit()
        return redirect(url_for('experiment'))

    return render_template('training.html', eventsList=eventsList, num_unprocessed_alerts = (len(eventsList) - num_processed_alerts))
#---------------------------------------------------------------------
#---------------------------Training Event Pages----------------------
@app.route('/trainingEventPage', methods = ["GET", "POST"])
@login_required
def trainingEventPage():
    eventId = request.args.get('eventId')
    event = models.TrainingEvent.query.get(eventId)    
    number = request.args.get('index')
    form = eventDecisionForm()
    decision = models.TrainingEventDecision.query.filter_by(user = current_user.username, event_id = eventId).\
        order_by(models.TrainingEventDecision.time_event_decision.desc()).first()
    if request.method == 'GET' and decision is not None:
        form.escalate.data = decision.escalate
        form.confidence.data = decision.confidence
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
        flash(f"Successfully recorded event decision!")
        return redirect(url_for("training"))

    if event.id == 1:
        return render_template('MoscowEventPage.html', event = event, number = number, form=form)
    elif event.id == 2:
        return render_template('BeijingEventPage.html', event = event, number = number, form=form)
    else:
        return render_template('trainingEventPage.html', event = event, number = number, form=form)


#---------------------------------------------------------------------
#---------------------------Experiment Page---------------------------
@app.route('/experiment', methods = ["GET", "POST"])
@login_required
def experiment():    
    user = models.User.query.filter_by(username = current_user.username).first()
    if request.method == "GET" and user.time_begin == None:
        local_user = db.session.merge(user)
        local_user.time_begin = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit() 

    if request.method == "POST":
        local_user = db.session.merge(user)
        local_user.experiment_complete = True 
        db.session.add(local_user)
        db.session.commit()
        return redirect(url_for('postsurvey')) 

    ids = [int(id) for id in current_user.events.split(",")]
    ids.insert(25, 73) #This is the most obvious "Escalate" event. Everyone sees this.
    ids.insert(6,74) #This is the "Please just select 'Escalate' event"
    ids.insert(43,75) #This is the "Please just select 'Don't escalate' event"
    if request.method == "GET":
        num_processed_alerts = 0
        for id in ids:
            if models.EventDecision.query.filter_by(user = current_user.username, event_id = id).\
                            order_by(models.EventDecision.time_event_decision.desc()).first() != None:
                num_processed_alerts += 1

    eventsList = []   #This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((models.Event.query.get(id),
                          models.EventDecision.query.filter_by(user = current_user.username, event_id = id).
                            order_by(models.EventDecision.time_event_decision.desc()).first())
                         )    
    return render_template('experiment.html', eventsList=eventsList, num_unprocessed_alerts = (len(eventsList) - num_processed_alerts) )
#---------------------------------------------------------------------
#---------------------------Experiment Event Page---------------------
@app.route('/eventPage/<eventId>', methods = ["GET", "POST"])
@login_required
def eventPage(eventId):    
    event = models.Event.query.get(eventId)
    form = eventDecisionForm()
    decision = models.EventDecision.query.filter_by(user = current_user.username, event_id = eventId).\
        order_by(models.EventDecision.time_event_decision.desc()).first()
    if request.method == 'GET' and decision is not None:
        form.escalate.data = decision.escalate
        form.confidence.data = decision.confidence
    if request.method == 'GET':
        newEvent = models.EventClicked(
            user = current_user.username,
            event_id = eventId,
            time_event_click = datetime.datetime.now()
        )   
        db.session.add(newEvent)
        db.session.commit()    

    print(form.errors)
    
    if form.validate_on_submit():  
        print("Form valid!")         
        response = models.EventDecision(
            user=current_user.username,
            event_id = eventId,
            escalate = form.escalate.data,
            confidence = form.confidence.data,
            time_event_decision = datetime.datetime.now()
        )            
        db.session.add(response)
        db.session.commit()
        flash("Successfully recorded event decision!")
        return redirect(url_for("experiment"))
    return render_template('eventPage.html', event = event, form=form)
#---------------------------------------------------------------------
#---------------------------Survey Page-------------------------------
@app.route('/postsurvey', methods = ["GET", "POST"]) 
@login_required
def postsurvey():

    user = models.User.query.filter_by(username = current_user.username).first()
    if request.method == "GET" and user.time_end == None:
        local_user = db.session.merge(user)
        local_user.time_end = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit()

    form = SurveyForm()
    if form.validate_on_submit():
        responses = models.SurveyAnswers(
            user = current_user.username,
            timestamp = datetime.datetime.now(),
            mental = form.mental.data,
            physical = form.physical.data,
            temporal = form.temporal.data,
            performance = form.performance.data,
            effort = form.effort.data,
            frustration = form.frustration.data,
            useful_info = form.useful_info.data,
            feedback = form.feedback.data
        )
        local_user = db.session.merge(user)
        local_user.survey_complete = True 
        db.session.add(responses, local_user)
        db.session.commit()
        return redirect(url_for('completion'))
    return render_template('postsurvey.html', form=form)
#---------------------------------------------------------------------
#---------------------------Completion Page---------------------------
@app.route("/completion")
def completion():    
    code = current_user.completion_code
    # logout_user()
    return render_template('completion.html', code=code)
#---------------------------------------------------------------------
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)