from forms import PrequestionnaireForm, SurveyForm, UserForm, eventDecisionForm
import os
import re
from bleach import clean
from flask import Flask, render_template, url_for, redirect, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import func, distinct
import datetime

eventnum_pattern = re.compile("^[0-9]{1,2}$")

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'crywolf.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

import models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route("/reference")
def reference():
    return render_template('reference.html')

# ---------------------------Index-------------------------------------
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('intro'))

    error = None
    form = UserForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('intro'))
        else:
            error = "Invalid username. Please try again."

    return render_template('index.html', form=form, error=error)
# ---------------------------------------------------------------------
# ---------------------------Landing Page------------------------------
@app.route("/intro", methods=["GET"])
@login_required
def intro():
    return render_template("intro.html")
# ---------------------------------------------------------------------
# ---------------------------Questionnaire-----------------------------
@app.route('/prequestionnaire', methods=["GET", "POST"])
@login_required
def prequestionnaire():
    form = PrequestionnaireForm()
    if form.validate_on_submit():
        answers = models.PrequestionnaireAnswers(
            timestamp=datetime.datetime.now(),
            user=current_user.username,
            role=form.role.data,
            exp_researcher=form.exp_researcher.data,
            exp_admin=form.exp_admin.data,
            exp_software=form.exp_software.data,
            exp_security=form.exp_security.data,
            familiarity_none=form.familiarity_none.data,
            familiarity_read=form.familiarity_read.data,
            familiarity_controlled=form.familiarity_controlled.data,
            familiarity_public=form.familiarity_public.data,
            familiarity_engineered=form.familiarity_engineered.data,
            subnet_mask=form.subnet_mask.data,
            network_address=form.network_address.data,
            tcp_faster=form.tcp_faster.data,
            http_port=form.http_port.data,
            firewall=form.security_device.data,
            socket=form.ip_port.data,
            which_model=form.which_model.data
        )
        user = models.User.query.filter_by(
            username=current_user.username).first()
        local_user = db.session.merge(user)
        local_user.questionnaire_complete = True
        db.session.add(answers, local_user)
        db.session.commit()
        flash("Questionnaire saved successfully!")
        return redirect(url_for('training'))
    return render_template('prequestionnaire.html', form=form)
# ---------------------------------------------------------------------
# ---------------------------Training Page-----------------------------
@app.route('/training', methods=["GET", "POST"])
@login_required
def training():
    ids = [1, 2, 3, 4, 5]
    eventsList = []  # This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((models.TrainingEvent.query.get(id),
                           models.TrainingEventDecision.query.filter_by(user=current_user.username, event_id=id).
                           order_by(models.TrainingEventDecision.time_event_decision.desc()).first())
                          )
    user = models.User.query.filter_by(username=current_user.username).first()
    if request.method == "POST":
        local_user = db.session.merge(user)
        local_user.training_complete = True
        db.session.add(local_user)
        db.session.commit()
        return redirect(url_for('experiment'))

    return render_template('training.html', eventsList=eventsList, num_unprocessed_alerts=(len(eventsList) - get_events_processed_for_user(current_user, training=True)))
# ---------------------------------------------------------------------
# ---------------------------Training Event Pages----------------------
@app.route('/trainingEventPage', methods=["GET", "POST"])
@login_required
def trainingEventPage():

    if not re.match(eventnum_pattern, request.args.get('eventId')) or not 0 < int(request.args.get('eventId')) <= 5:
        abort(404)


    event = models.TrainingEvent.query.get(request.args.get('eventId'))
    num_training_events = db.session.query(func.count(models.TrainingEvent.id)).scalar()
    form = eventDecisionForm()
    decision = models.TrainingEventDecision.query.filter_by(user=current_user.username, event_id=event.id).\
        order_by(models.TrainingEventDecision.time_event_decision.desc()).first()
    if request.method == 'GET' and decision is not None:
        form.escalate.data = decision.escalate
        form.confidence.data = decision.confidence

    if form.validate_on_submit():
        response = models.TrainingEventDecision(
            user=current_user.username,
            event_id=event.id,
            escalate=form.escalate.data,
            confidence=form.confidence.data,
            time_event_decision=datetime.datetime.now()
        )
        db.session.add(response)
        db.session.commit()
        flash(f"Successfully recorded decision for Training Event {event.id}!")
        if event.id == 5:
            flash(f"You recorded a decision for the last training event. Click on specific Events below to revisit them if you like.")
            return redirect(url_for("training"))
        else:
            return redirect(url_for('trainingEventPage', eventId=event.id + 1))

    
    if event.id == 1:
        page = 'MoscowEventPage.html'
    elif event.id == 2:
        page = 'BeijingEventPage.html'
    else:
        page = 'trainingEventPage.html'
    print(f"{type(event.id+1)}: {(event.id+1)}")
    return render_template(page, event=event, number=event.id + 1, num_unprocessed_alerts=num_training_events - get_events_processed_for_user(current_user, training=True), form=form)


def get_event_list_for_user(user):
    ids = [int(id) for id in user.events.split(",")]
    # This is the most obvious "Escalate" event. Everyone sees this.
    ids.insert(25, 73)
    ids.insert(6, 74)  # This is the "Please just select 'Escalate' event"
    # This is the "Please just select 'Don't escalate' event"
    ids.insert(43, 75)
    return ids


def get_events_processed_for_user(current_user, training=False):
    if training:
        return db.session.query(func.count(distinct(models.TrainingEventDecision.event_id))).filter(
            models.TrainingEventDecision.user == current_user.username).scalar()
    else:
        return db.session.query(func.count(distinct(models.EventDecision.event_id))).filter(
            models.EventDecision.user == current_user.username).scalar()
# ---------------------------------------------------------------------
# ---------------------------Experiment Page---------------------------
@app.route('/experiment', methods=["GET", "POST"])
@login_required
def experiment():
    user = models.User.query.filter_by(username=current_user.username).first()
    if request.method == "POST":
        local_user = db.session.merge(user)
        local_user.experiment_complete = True
        db.session.add(local_user)
        db.session.commit()
        return redirect(url_for('postsurvey'))

    if user.time_begin == None:
        local_user = db.session.merge(user)
        local_user.time_begin = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit()

    ids = get_event_list_for_user(current_user)
    eventsList = []  # This will store an eventID and eventDecision tuple
    for id in ids:
        eventsList.append((
            models.Event.query.get(id),
            models.EventDecision.query.filter_by(user=current_user.username, event_id=id).order_by(
                models.EventDecision.time_event_decision.desc()).first()
        )
        )
    return render_template('experiment.html', eventsList=eventsList, num_unprocessed_alerts=(len(eventsList) - get_events_processed_for_user(current_user)))
# ---------------------------------------------------------------------
# ---------------------------Experiment Event Page---------------------
@app.route('/eventPage', methods=["GET", "POST"])
@login_required
def eventPage():
    eventId = request.args.get('eventId')
    ids = get_event_list_for_user(current_user)
    if not re.match(eventnum_pattern, eventId) or int(eventId) not in ids:
        abort(404)
    
    event_index = ids.index(int(eventId))
    event = models.Event.query.get(eventId)
    form = eventDecisionForm()
    decision = models.EventDecision.query.filter_by(user=current_user.username, event_id=eventId).\
        order_by(models.EventDecision.time_event_decision.desc()).first()
    if request.method == 'GET' and decision is not None:
        form.escalate.data = decision.escalate
        form.confidence.data = decision.confidence
    if request.method == 'GET':
        newEvent = models.EventClicked(
            user=current_user.username,
            event_id=eventId,
            time_event_click=datetime.datetime.now()
        )
        db.session.add(newEvent)
        db.session.commit()

    if form.validate_on_submit():
        response = models.EventDecision(
            user=current_user.username,
            event_id=eventId,
            escalate=form.escalate.data,
            confidence=form.confidence.data,
            time_event_decision=datetime.datetime.now()
        )
        db.session.add(response)
        db.session.commit()
        flash(f"Successfully recorded decision for Event {event_index + 1}!")
        if event_index == len(ids) - 1:
            flash(f"You recorded a decision for the last event in the list. Click on specific Events below to revisit them if you like.")
            return redirect(url_for("experiment"))
        else:
            next_event = models.Event.query.get(ids[event_index + 1]).id
            return redirect(url_for('eventPage', eventId=next_event))

    return render_template('eventPage.html', event=event, number=event_index + 1, num_unprocessed_alerts=len(ids) - get_events_processed_for_user(current_user), form=form)
# ---------------------------------------------------------------------
# ---------------------------Survey Page-------------------------------
@app.route('/postsurvey', methods=["GET", "POST"])
@login_required
def postsurvey():

    user = models.User.query.filter_by(username=current_user.username).first()
    if request.method == "GET" and user.time_end == None:
        local_user = db.session.merge(user)
        local_user.time_end = datetime.datetime.now()
        db.session.add(local_user)
        db.session.commit()

    form = SurveyForm()
    if form.validate_on_submit():
        responses = models.SurveyAnswers(
            user=current_user.username,
            timestamp=datetime.datetime.now(),
            mental=form.mental.data,
            physical=form.physical.data,
            temporal=form.temporal.data,
            performance=form.performance.data,
            effort=form.effort.data,
            frustration=form.frustration.data,
            useful_info=clean(form.useful_info.data),
            feedback=clean(form.feedback.data)
        )
        local_user = db.session.merge(user)
        local_user.survey_complete = True
        db.session.add(responses, local_user)
        db.session.commit()
        return redirect(url_for('completion'))
    return render_template('postsurvey.html', form=form)
# ---------------------------------------------------------------------
# ---------------------------Completion Page---------------------------
@app.route("/completion")
def completion():
    code = current_user.completion_code
    # logout_user()
    return render_template('completion.html', code=code)
# ---------------------------------------------------------------------
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

