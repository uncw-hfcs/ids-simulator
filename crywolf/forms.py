from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

class PrequestionnaireForm(Form):
    one = StringField("one", validators=DataRequired())
    twoA = StringField("twoA", validators=DataRequired())
    twoB = StringField("twoB", validators=DataRequired())
    twoC = StringField("twoC", validators=DataRequired())
    twoD = StringField("twoD", validators=DataRequired())
    threeA = StringField("threeA")
    threeB = StringField("threeB")
    threeC = StringField("threeC")
    threeD = StringField("threeD")
    threeE = StringField("threeE")
    four = StringField("four", validators=DataRequired())
    five = StringField("five", validators=DataRequired())
    six = StringField("six", validators=DataRequired())
    seven = StringField("seven", validators=DataRequired())
    eight = StringField("eight", validators=DataRequired())
    nine = StringField("nine", validators=DataRequired())
    ten = StringField("ten", validators=DataRequired())
