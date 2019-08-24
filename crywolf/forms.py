from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired

class eventDecisionForm(FlaskForm):
    escalate = RadioField(
                    choices=[
                        ('Escalate','Escalate'),
                        ("Don't escalate","Don't escalate"),
                        ("I don't know","I don't know")
                    ]
                )
    confidence = RadioField(choices=[("1","1"),("2","2"),("3", "3"),("4","4"),("5","5")])

class UserForm(FlaskForm):
    username = StringField('username:', validators=[DataRequired()])
    
class SurveyForm(FlaskForm):
    mental = DecimalField(places=1)
    physical = DecimalField(places=1)
    temporal = DecimalField(places=1)
    performance = DecimalField(places=1)
    effort = DecimalField(places=1)
    frustration = DecimalField(places=1)
    useful_info = TextAreaField()
    feedback = TextAreaField()

class PrequestionnaireForm(FlaskForm):
    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        
        for field in [self.familiarity_none, self.familiarity_read, self.familiarity_controlled, self.familiarity_public, self.familiarity_engineered]:
            if field.data is True:
                return False                
                     
        return result

    role = RadioField('Which role best describes your current experience?', 
                choices=[
                    ('Student','Student'),
                    ('Researcher','Researcher'), 
                    ('IT/Network Administrator','IT/Network Administrator'), 
                    ('Software Engineering','Software Engineering (developer, tester, project management, etc.)'), 
                    ('Cyber Security Specialist','Cyber Security Specialist')
                    ],
                validators=[DataRequired()]
                )
    exp_researcher = RadioField('Researcher', 
                choices=[
                    ('None','None'),
                    ('< 1','< 1'), 
                    ('1 - 5','1 - 5'), 
                    ('5 - 10','5 - 10'), 
                    ('10+','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_admin = RadioField('IT/Network Administrator', 
                choices=[
                    ('None','None'),
                    ('< 1','< 1'), 
                    ('1 - 5','1 - 5'), 
                    ('5 - 10','5 - 10'), 
                    ('10+','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_software = RadioField('Software Engineering', 
                choices=[
                    ('None','None'),
                    ('< 1','< 1'), 
                    ('1 - 5','1 - 5'), 
                    ('5 - 10','5 - 10'), 
                    ('10+','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_security = RadioField('Cyber Security Specialist', 
                choices=[
                    ('None','None'),
                    ('< 1','< 1'), 
                    ('1 - 5','1 - 5'), 
                    ('5 - 10','5 - 10'), 
                    ('10+','10+')
                    ],
                validators=[DataRequired()]
                )

    familiarity_none = BooleanField('None/very little')
    familiarity_read = BooleanField('I have read about how attacks work')
    familiarity_controlled = BooleanField('I have attacked or defended against an attack in a controlled setting')
    familiarity_public = BooleanField('I have defended or investigated attacks on a public network')
    familiarity_engineered = BooleanField('I have engineered software that explicitly involves attacks or defense of network cyber security attacks')

    subnet_mask = RadioField('Label', 
                    choices=[
                        ('a) 173.67.14.127','a) 173.67.14.127'),
                        ('b) 173.67.14.0','b) 173.67.14.0'), 
                        ('c) 255.255.255.0','c) 255.255.255.0'), 
                        ('d) 255.255.255.24','d) 255.255.255.24'), 
                        ('e) I don’t know','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                    )

    network_address = RadioField('Label', 
                        choices=[
                        ('a) 173.67.14.127','a) 173.67.14.127'),
                        ('b) 173.67.14.0','b) 173.67.14.0'), 
                        ('c) 255.255.255.0','c) 255.255.255.0'), 
                        ('d) 255.255.255.24','d) 255.255.255.24'), 
                        ('e) I don’t know','e) I don’t know')
                            ],
                        validators=[DataRequired()]
                        )

    tcp_faster = RadioField('Label', 
                    choices=[
                        ('True','a) True'),
                        ('False','b) False'), 
                        ('I don’t know','c) I don’t know')
                        ],
                    validators=[DataRequired()]
                    )

    http_port = RadioField('Label', 
                    choices=[
                        ('80','a) 80'),
                        ('443','b) 443'), 
                        ('587','c) 587'), 
                        ('5000','d) 5000'), 
                        ('I don’t know','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )    

    firewall =  RadioField('Label', 
                    choices=[
                        ('Honeypot','a) Honeypot'),
                        ('Firewall','b) Firewall'), 
                        ('Botnet','c) Botnet'), 
                        ('Intrusion Detection System','d) Intrusion Detection System'), 
                        ('I don’t know','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )  

    socket =  RadioField('Label', 
                    choices=[
                        ('Socket','a) Socket'),
                        ('MAC Address','b) MAC Address'), 
                        ('Protocol','c) Protocol'), 
                        ('Ping','d) Ping'), 
                        ('I don’t know','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )    

    which_model =  RadioField('Label', 
                        choices=[
                            ('OSI','a) OSI'),
                            ('TCP/IP','b) TCP/IP'), 
                            ('UML','c) UML'), 
                            ('HTTPS','d) HTTPS'), 
                            ('I don’t know','e) I don’t know')
                            ],
                        validators=[DataRequired()]
                    )