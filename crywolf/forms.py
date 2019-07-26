from flask_wtf import FlaskForm
from wtforms.fields import StringField, RadioField, BooleanField
from wtforms.validators import DataRequired

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

    # TODO: Create RadioFields similar to those above. The first parameter is the label. I recommend that you store the actual value of the answer rather than a 
    # integer representing their selection (e.g., store '173.67.14.127' instead of '0' -- it will be easier for you to debug the data in the database.
    
    # four = StringField("four", validators=[DataRequired()])
    # five = StringField("five", validators=[DataRequired()])
    # six = StringField("six", validators=[DataRequired()])
    # seven = StringField("seven", validators=[DataRequired()])
    # eight = StringField("eight", validators=[DataRequired()])
    # nine = StringField("nine", validators=[DataRequired()])
    # ten = StringField("ten", validators=[DataRequired()])
