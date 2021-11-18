from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, BooleanField, TextAreaField, IntegerField, SelectField
from wtforms.validators import InputRequired, ValidationError, Optional, NumberRange


class OptionalConfidence(Optional):
    # a validator which makes a field optional if
    # another field has a desired value

    def __init__(self, *args, **kwargs):
        super(OptionalConfidence, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        if form.escalate.data == "I don't know":
            super(OptionalConfidence, self).__call__(form, field)


class EventDecisionForm(FlaskForm):
    escalate = RadioField(
        choices=[
            ('Escalate', 'Escalate'),
            ("Don't escalate", "Don't escalate"),
            ("I don't know", "I don't know")
        ],
        validators=[InputRequired()]
    )
    confidence = RadioField(choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
                            validators=[OptionalConfidence()])


class UserForm(FlaskForm):
    username = StringField('username:', validators=[InputRequired()])


class SurveyForm(FlaskForm):
    mental = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    physical = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    temporal = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    performance = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    effort = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    frustration = IntegerField(validators=[InputRequired(), NumberRange(min=1.0, max=10.0)])
    useful_info = TextAreaField(validators=[InputRequired()])
    feedback = TextAreaField()


class PrequestionnaireForm(FlaskForm):

    def validate_familiarity_none(form, field, message=None):
        if not any(f.data for f in
                   [form.familiarity_none, form.familiarity_read, form.familiarity_controlled, form.familiarity_public,
                    form.familiarity_engineered]):
            raise ValidationError(u"Please check at least one box.")

    role = SelectField('Which role best describes your current experience?',
                       choices=[
                           (None, "Select"),
                           ('Student', 'Student'),
                           ('Researcher', 'Researcher'),
                           ('IT/Network Administrator', 'IT/Network Administrator'),
                           ('Software Engineering',
                            'Software Engineering (developer, tester, project management, etc.)'),
                           ('Cyber Security Specialist', 'Cyber Security Specialist')
                       ],
                       validators=[InputRequired()]
                       )
    exp_researcher = SelectField('Researcher',
                                 choices=[
                                     (None, "Select"),
                                     ('No Experience', 'No Experience'),
                                     ('< 1', '< 1'),
                                     ('1 - 5', '1 - 5'),
                                     ('5 - 10', '5 - 10'),
                                     ('10+', '10+')
                                 ],
                                 validators=[InputRequired()]
                                 )
    exp_admin = SelectField('IT/Network Administrator',
                            choices=[
                                (None, "Select"),
                                ('No Experience', 'No Experience'),
                                ('< 1', '< 1'),
                                ('1 - 5', '1 - 5'),
                                ('5 - 10', '5 - 10'),
                                ('10+', '10+')
                            ],
                            validators=[InputRequired()]
                            )
    exp_software = SelectField('Software Engineering',
                               choices=[
                                   (None, "Select"),
                                   ('No Experience', 'No Experience'),
                                   ('< 1', '< 1'),
                                   ('1 - 5', '1 - 5'),
                                   ('5 - 10', '5 - 10'),
                                   ('10+', '10+')
                               ],
                               validators=[InputRequired()]
                               )
    exp_security = SelectField('Cyber Security Specialist',
                               choices=[
                                   (None, "Select"),
                                   ('No Experience', 'No Experience'),
                                   ('< 1', '< 1'),
                                   ('1 - 5', '1 - 5'),
                                   ('5 - 10', '5 - 10'),
                                   ('10+', '10+')
                               ],
                               validators=[InputRequired()]
                               )

    familiarity_none = BooleanField('None/very little')
    familiarity_read = BooleanField('I have read about how attacks work')
    familiarity_controlled = BooleanField('I have attacked or defended against an attack in a controlled setting')
    familiarity_public = BooleanField('I have defended or investigated attacks on a public network')
    familiarity_engineered = BooleanField(
        'I have engineered software that explicitly involves attacks or defense of network cyber security attacks')

    subnet_mask = RadioField('Label',
                             choices=[
                                 ('173.67.14.127', 'a) 173.67.14.127'),
                                 ('173.67.14.0', 'b) 173.67.14.0'),
                                 ('255.255.255.0', 'c) 255.255.255.0'),
                                 ('255.255.255.24', 'd) 255.255.255.24'),
                                 ('I don’t know', 'e) I don’t know')
                             ],
                             validators=[InputRequired()]
                             )

    network_address = RadioField('Label',
                                 choices=[
                                     ('173.67.14.127', 'a) 173.67.14.127'),
                                     ('173.67.14.0', 'b) 173.67.14.0'),
                                     ('255.255.255.0', 'c) 255.255.255.0'),
                                     ('255.255.255.24', 'd) 255.255.255.24'),
                                     ('I don’t know', 'e) I don’t know')
                                 ],
                                 validators=[InputRequired()]
                                 )

    tcp_faster = RadioField('Label',
                            choices=[
                                ('True', 'a) True'),
                                ('False', 'b) False'),
                                ('I don’t know', 'c) I don’t know')
                            ],
                            validators=[InputRequired()]
                            )

    http_port = RadioField('Label',
                           choices=[
                               ('80', 'a) 80'),
                               ('443', 'b) 443'),
                               ('587', 'c) 587'),
                               ('5000', 'd) 5000'),
                               ('I don’t know', 'e) I don’t know')
                           ],
                           validators=[InputRequired()]
                           )

    security_device = RadioField('Label',
                                 choices=[
                                     ('Honeypot', 'a) Honeypot'),
                                     ('Firewall', 'b) Firewall'),
                                     ('Botnet', 'c) Botnet'),
                                     ('Intrusion Detection System', 'd) Intrusion Detection System'),
                                     ('I don’t know', 'e) I don’t know')
                                 ],
                                 validators=[InputRequired()]
                                 )

    ip_port = RadioField('Label',
                         choices=[
                             ('Socket', 'a) Socket'),
                             ('MAC Address', 'b) MAC Address'),
                             ('Protocol', 'c) Protocol'),
                             ('Ping', 'd) Ping'),
                             ('I don’t know', 'e) I don’t know')
                         ],
                         validators=[InputRequired()]
                         )

    which_model = RadioField('Label',
                             choices=[
                                 ('OSI', 'a) OSI'),
                                 ('TCP/IP', 'b) TCP/IP'),
                                 ('UML', 'c) UML'),
                                 ('HTTPS', 'd) HTTPS'),
                                 ('I don’t know', 'e) I don’t know')
                             ],
                             validators=[InputRequired()]
                             )
