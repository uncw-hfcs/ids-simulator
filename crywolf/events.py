# import things
from flask_table import Table, Col

# Declare your table
class EventsTable(Table):
    id = Col('id')
    date = Col('date')
    classification = Col('classification')
    source_ip = Col('source_ip')
    source_port = Col('source_port')
    destination_ip = Col('destination_ip')
    destination_port = Col('destination_port')
    description = Col('description')

# Get some objects
class EventItem(object):
    def __init__(self, id, date, classification, source_ip, source_port, destination_ip, destination_port, description):
        self.id = id
        self.date = date
        self.classification = classification
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.description = description

    def __str__(self):
        return "{}\t{}\t{}".format(self.id, self.date, self.description)