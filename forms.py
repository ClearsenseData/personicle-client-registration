
from crypt import methods
from sys import api_version
from flask import Flask, render_template, url_for, flash, redirect,request, logging
from wtforms import Form, StringField, validators, TextAreaField
from header import headers


class NewSecretDeleteGetForm(Form):
    client_id = StringField("Enter your client id",[validators.DataRequired()])

class RegisterForm(Form):
    client_name = StringField('Your application name', [validators.Length(min=5,max=50), validators.DataRequired()])
    client_uri = StringField('Your application URL', [ validators.DataRequired()])
    redirect_uri = StringField('Your redirect URI', [ validators.DataRequired()])
   

class UpdateForm(Form):
    client_id = StringField("Enter you client id",[validators.DataRequired()])
    client_name = StringField('Your application name', [validators.Length(min=5,max=50), validators.DataRequired()])
    client_uri = StringField('Your application URL', [ validators.DataRequired()])
    redirect_uri = StringField('Your redirect URI', [ validators.DataRequired()])   