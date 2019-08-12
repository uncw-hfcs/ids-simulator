from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, BooleanField, TextAreaField
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
    username = StringField('Please enter a username:', validators=[DataRequired()])
    
class SurveyForm(FlaskForm):
    mental = StringField()
    physical = StringField()
    temporal = StringField()
    performance = StringField()
    effort = StringField()
    frustration = StringField()
    useful_info = TextAreaField()
    feedback = TextAreaField()

class PrequestionnaireForm(FlaskForm):
    role = RadioField('Label', 
                choices=[
                    ('0','Student'),
                    ('1','Researcher'), 
                    ('2','IT/Network Administrator'), 
                    ('3','Software Engineering (developer, tester, project management, etc.)'), 
                    ('4','Cyber Security Specialist')
                    ],
                validators=[DataRequired()]
                )
    exp_researcher = RadioField('Researcher', 
                choices=[
                    ('0','None'),
                    ('1','< 1'), 
                    ('2','1 - 5'), 
                    ('3','5 - 10'), 
                    ('4','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_admin = RadioField('IT/Network Administrator', 
                choices=[
                    ('0','None'),
                    ('1','< 1'), 
                    ('2','1 - 5'), 
                    ('3','5 - 10'), 
                    ('4','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_software = RadioField('Software Engineering', 
                choices=[
                    ('0','None'),
                    ('1','< 1'), 
                    ('2','1 - 5'), 
                    ('3','5 - 10'), 
                    ('4','10+')
                    ],
                validators=[DataRequired()]
                )
    exp_security = RadioField('Cyber Security Specialist', 
                choices=[
                    ('0','None'),
                    ('1','< 1'), 
                    ('2','1 - 5'), 
                    ('3','5 - 10'), 
                    ('4','10+')
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
                        ('0','a) 173.67.14.127'),
                        ('1','b) 173.67.14.0'), 
                        ('2','c) 255.255.255.0'), 
                        ('3','d) 255.255.255.24'), 
                        ('4','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                    )

    network_address = RadioField('Label', 
                        choices=[
                            ('0','a) 173.67.14.127'),
                            ('1','b) 173.67.14.0'), 
                            ('2','c) 255.255.255.0'), 
                            ('3','d) 255.255.255.24'), 
                            ('4','e) I don’t know')
                            ],
                        validators=[DataRequired()]
                        )

    tcp_faster = RadioField('Label', 
                    choices=[
                        ('0','a) True'),
                        ('1','b) False'), 
                        ('2','c) I don’t know')
                        ],
                    validators=[DataRequired()]
                    )

    http_port = RadioField('Label', 
                    choices=[
                        ('0','a) 80'),
                        ('1','b) 443'), 
                        ('2','c) 587'), 
                        ('3','d) 5000'), 
                        ('4','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )    

    firewall =  RadioField('Label', 
                    choices=[
                        ('0','a) Honeypot'),
                        ('1','b) Firewall'), 
                        ('2','c) Botnet'), 
                        ('3','d) Intrusion Detection System'), 
                        ('4','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )  

    socket =  RadioField('Label', 
                    choices=[
                        ('0','a) Socket'),
                        ('1','b) MAC Address'), 
                        ('2','c) Protocol'), 
                        ('3','d) Ping'), 
                        ('4','e) I don’t know')
                        ],
                    validators=[DataRequired()]
                )    

    which_model =  RadioField('Label', 
                        choices=[
                            ('0','a) OSI'),
                            ('1','b) TCP/IP'), 
                            ('2','c) UML'), 
                            ('3','d) HTTPS'), 
                            ('4','e) I don’t know')
                            ],
                        validators=[DataRequired()]
                    )            
    # TODO: Create RadioFields similar to those above. The first parameter is the label. I recommend that you store the actual value of the answer rather than a 
    # integer representing their selection (e.g., store '173.67.14.127' instead of '0' -- it will be easier for you to debug the data in the database.
    
 