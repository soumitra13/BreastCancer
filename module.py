from wtforms import Form, FloatField, validators, StringField
from wtforms.validators import DataRequired


class AddPatientForm(Form):
    first_name = StringField('First Name', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])
    last_name = StringField('Last Name', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])
    contact_no = StringField('Contact Number', [
        validators.Length(min = 12, max = 12),
        validators.DataRequired()
    ])
    address = TextAreaField('Address', [
        validators.Length(min = 12, max = 50),
        validators.DataRequired()
    ])
    dob = DateField('Date of Birth', [
        validators.Length(min = 12, max = 12),
        validators.DataRequired()
    ])
    ct = FloatField('Clump Thickness', [
    validators.Length(min=1,max=2),
    validators.DataRequired()
    ])
    ucsi = FloatField('Uniformity of Cell Size',[
        validators.Length(min =1, max=2),
        validators.DataRequired()
    ])
    ucsh = FloatField('Uniformity of Cell Shape',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    ma = FloatField('Marginal Adhesion',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    secs = FloatField('Single Epithelial Cell Size',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    bn = FloatField('Bare Nuclei',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    bc = FloatField('Bland Chromatin',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    nm = FloatField('Normal Nucleoli',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    mi = FloatField('Mitoses',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
