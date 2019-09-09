from crywolf import db
from flask_login.mixins import UserMixin

class EventClicked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    event_id = db.Column(db.Integer)
    time_event_click = db.Column(db.DateTime)

class EventDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    event_id = db.Column(db.Integer)
    escalate = db.Column(db.String(15))
    confidence = db.Column(db.String(1))
    time_event_decision = db.Column(db.DateTime)

    def __repr__(self):
        return self.escalate

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    should_escalate = db.Column(db.String(25))
    country_of_authentication1 = db.Column(db.String(25))
    number_successful_logins1 = db.Column(db.String(25))
    number_failed_logins1 = db.Column(db.String(25))
    source_provider1 = db.Column(db.String(50))
    country_of_authentication2 = db.Column(db.String(25))
    number_successful_logins2 = db.Column(db.String(25))
    number_failed_logins2 = db.Column(db.String(25))
    source_provider2 = db.Column(db.String(50))
    time_between_authentications = db.Column(db.String(25))
    vpn_confidence = db.Column(db.String(5))

class TrainingEventDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    event_id = db.Column(db.Integer)
    escalate = db.Column(db.String(15))
    confidence = db.Column(db.String(1))
    time_event_decision = db.Column(db.DateTime)

    def __repr__(self):
        return self.escalate

class TrainingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    should_escalate = db.Column(db.String(25))
    country_of_authentication1 = db.Column(db.String(25))
    number_successful_logins1 = db.Column(db.Integer)
    number_failed_logins1 = db.Column(db.Integer)
    source_provider1 = db.Column(db.String(50))
    country_of_authentication2 = db.Column(db.String(25))
    number_successful_logins2 = db.Column(db.Integer)
    number_failed_logins2 = db.Column(db.Integer)
    source_provider2 = db.Column(db.String(50))
    time_between_authentications = db.Column(db.Float)
    vpn_confidence = db.Column(db.String(5))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    group = db.Column(db.Integer())
    time_begin = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    events = db.Column(db.String(256))
    questionnaire_complete = db.Column(db.Boolean)
    training_complete = db.Column(db.Boolean)
    experiment_complete = db.Column(db.Boolean)
    survey_complete = db.Column(db.Boolean)
    completion_code = db.Column(db.String(6))

    def __repr__(self):
        return self.username


class SurveyAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    mental = db.Column(db.Float(3))
    physical = db.Column(db.Float(3))
    temporal = db.Column(db.Float(3))
    performance = db.Column(db.Float(3))
    effort = db.Column(db.Float(3))
    frustration = db.Column(db.Float(3))
    useful_info = db.Column(db.Text())
    feedback = db.Column(db.Text())

class PrequestionnaireAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    role = db.Column(db.String(50))

    exp_researcher = db.Column(db.String(50))
    exp_admin = db.Column(db.String(50))
    exp_software = db.Column(db.String(50))
    exp_security = db.Column(db.String(50))

    familiarity_none = db.Column(db.Boolean())
    familiarity_read = db.Column(db.Boolean())
    familiarity_controlled = db.Column(db.Boolean())
    familiarity_public = db.Column(db.Boolean())
    familiarity_engineered = db.Column(db.Boolean())

    subnet_mask = db.Column(db.String(256))
    network_address = db.Column(db.String(256))
    tcp_faster = db.Column(db.String(256))
    http_port = db.Column(db.String(256))
    firewall = db.Column(db.String(256))
    socket = db.Column(db.String(256))
    which_model = db.Column(db.String(256))