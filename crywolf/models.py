from crywolf import db

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
    