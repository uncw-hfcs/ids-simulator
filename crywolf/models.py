from crywolf import db
from flask_login.mixins import UserMixin

class EventDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    event_id = db.Column(db.Integer)
    escalate = db.Column(db.String(15))
    confidence = db.Column(db.String(1))

class TrainingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_false_positive = db.Column(db.Boolean())
    country_of_authentication1 = db.Column(db.String(1))
    number_successful_logins1 = db.Column(db.Integer)
    number_failed_logins1 = db.Column(db.Integer)
    source_provider1 = db.Column(db.String(50))
    country_of_authentication2 = db.Column(db.String(1))
    number_successful_logins2 = db.Column(db.Integer)
    number_failed_logins2 = db.Column(db.Integer)
    source_provider2 = db.Column(db.String(50))
    time_between_authentications = db.Column(db.Float)
    vpn_confidence = db.Column(db.String(5))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    group = db.Column(db.Integer())

    def __repr__(self):
        return self.username


class SurveyAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    mental = db.Column(db.String(3))
    physical = db.Column(db.String(3))
    temporal = db.Column(db.String(3))
    performance = db.Column(db.String(3))
    effort = db.Column(db.String(3))
    frustration = db.Column(db.String(3))
    useful_info = db.Column(db.String(1000))
    feedback = db.Column(db.String(1000))

class PrequestionnaireAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    role = db.Column(db.String(1))

    exp_researcher = db.Column(db.Integer())
    exp_admin = db.Column(db.Integer())
    exp_software = db.Column(db.Integer())
    exp_security = db.Column(db.Integer())

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
    
    # TODO: Give the remaining radio button quiz questions good column names. Make them all String(256)
    # TODO: Once you modify the database here, you are going to need re-create the database file itself so the table is created with the right columns.
    
'''
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    classification = db.Column(db.String(100))
    source_ip = db.Column(db.String(15))
    source_port = db.Column(db.String(5))
    destination_ip = db.Column(db.String(15))
    destination_port = db.Column(db.String(5))
    description = db.Column(String(100))

    def __repr__(self):
        return "Event {}: {}".format(self.id, self.description)
'''    