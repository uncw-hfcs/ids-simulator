from crywolf import db

class PrequestionnaireAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    one = db.Column(db.String(1))
    twoA = db.Column(db.String(1))
    twoB = db.Column(db.String(1))
    twoC = db.Column(db.String(1))
    twoD = db.Column(db.String(1))
    threeA = db.Column(db.String(1))
    threeB = db.Column(db.String(1))
    threeC = db.Column(db.String(1))
    threeD = db.Column(db.String(1))
    threeE = db.Column(db.String(1))
    four = db.Column(db.String(1))
    five = db.Column(db.String(1))
    six = db.Column(db.String(1))
    seven = db.Column(db.String(1))
    eight = db.Column(db.String(1))
    nine = db.Column(db.String(1))
    ten = db.Column(db.String(1))
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