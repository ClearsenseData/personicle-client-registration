
from crypt import methods
from sys import api_version
from flask import Flask, render_template, url_for, flash, redirect,request, logging
from wtforms import Form, StringField, validators, SelectMultipleField, TextAreaField
from header import headers

scope_choices = [('com.personicle.individual.datastreams.heartrate', 'heartrate read'),
    #  ('com.personicle.individual.datastreams.heartrate.write', 'heartrate write') ,
     ('com.personicle.individual.datastreams.heart_intensity_minutes', 'heart intensity minutes read'),
    #  ('com.personicle.individual.datastreams.heart_intensity_minutes.write', 'heart intensity minutes write'),
     ('events.read', 'events read'),
    #  ('events.write', 'events write') ,
    ('com.personicle.individual.datastreams.step.cumulative', 'step cumulative read'),
    ('com.personicle.individual.datastreams.resting_calories', 'resting calories read'),
    ('com.personicle.individual.datastreams.active_calories', 'active calories read'),
    ('com.personicle.individual.datastreams.total_calories', 'total calories read'),
    ('com.personicle.individual.datastreams.distance', 'distance read'),
    ('com.personicle.individual.datastreams.weight', 'weight read'),
    ('com.personicle.individual.datastreams.cycling.cadence', 'cycling cadence read'),
    ('com.personicle.individual.datastreams.cycling.power', 'cycling power read'),
    ('com.personicle.individual.datastreams.step.cadence', 'step cadence read'),
    ('com.personicle.individual.datastreams.body_fat', 'body fat read'),
    ('com.personicle.individual.datastreams.height', 'height read'),
    ('com.personicle.individual.datastreams.location', 'location read'),
    ('com.personicle.individual.datastreams.speed', 'speed read'),
    ('com.personicle.individual.datastreams.blood_glucose', 'blood glucose read'),
    ('com.personicle.individual.datastreams.blood_pressure.systolic', 'blood pressure systolic read'),
    ('com.personicle.individual.datastreams.blood_pressure.diastolic', 'blood pressure diastolic read'),
    ('com.personicle.individual.datastreams.body_temperature', 'body temperature read')
     ]
class NewSecretDeleteGetForm(Form):
    client_id = StringField("Enter your client id",[validators.DataRequired()])

class GetScopesForm(Form):
    client_id = StringField("Enter your client id",[validators.DataRequired()])
  

class UpdateScopesForm(Form):
    client_id = StringField("Enter your client id",[validators.DataRequired()])
    access_scopes = SelectMultipleField('Update your scopes (Ctrl + click to select multiple fields)', [ validators.DataRequired()],
     choices=scope_choices)

class RegisterForm(Form):
    client_name = StringField('Your application name', [validators.Length(min=5,max=50), validators.DataRequired()])
    client_uri = StringField('Your application URL', [ validators.DataRequired()])
    redirect_uri = StringField('Your redirect URI', [ validators.DataRequired()])
    access_scopes = SelectMultipleField('What user data would you like to access? (Ctrl + click to select multiple fields)', [ validators.DataRequired()],
     choices=scope_choices)

class UpdateForm(Form):
    client_id = StringField("Enter you client id",[validators.DataRequired()])
    client_name = StringField('Your application name', [validators.Length(min=5,max=50), validators.DataRequired()])
    client_uri = StringField('Your application URL', [ validators.DataRequired()])
    redirect_uri = StringField('Your redirect URI', [ validators.DataRequired()])   