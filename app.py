from crypt import methods
from sys import api_version

from flask import Flask, render_template, url_for, flash, redirect,request, logging
from wtforms import Form, StringField, validators, TextAreaField
import requests
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

api_server = config_object["APISERVER"]  
client_registration = config_object["CLIENT_REGISTRATION"]
group_assignment=config_object["GROUP_ASSIGNMENT"]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


class DeleteFrom(Form):
    client_id = StringField("Enter you client id",[validators.DataRequired()])


    @app.route('/delete',methods=['GET','DELETE','POST'])
    def delete_app():
        form = DeleteFrom(request.form)
        
        if request.method == 'POST' and form.validate():
            client_id = form.client_id.data

            headers = {
            'Accept': 'application/json',
            'Authorization': f'{api_server["TOKEN"]}'
            }
            res = requests.delete(f"{client_registration['ENDPOINT']}/{client_id}", headers=headers)
            
            if res.status_code == 204:
             flash(f"Your client app  {client_id} is deleted.",'warning')
             return redirect(url_for('index'))
            else:
                 flash(f"Unable to delete {client_id}. Please make sure your client id is correct.",'warning')
        return render_template('delete.html', form=form) 

class RegisterForm(Form):
    client_name = StringField('Your application name', [validators.Length(min=5,max=50), validators.DataRequired()])
    client_uri = StringField('Your application URL', [ validators.DataRequired()])
    redirect_uri = StringField('Your redirect URI', [ validators.DataRequired()])
   



    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
          client_name = form.client_name.data
          client_uri = form.client_uri.data
          redirect_uri = form.redirect_uri.data
 
          headers = {
            'Accept': 'application/json',
            'Authorization': f'{api_server["TOKEN"]}'
            }
       
          json_data = {
            'client_name': client_name,
            'client_uri': client_uri,
            'application_type': 'web',
            'redirect_uris': [
                redirect_uri,
            ],
            'post_logout_redirect_uris': [
                'http://localhost:3000/oauth/callback/postLogoutRedirectUri',
            ],
            'response_types': [
                'code',
                'id_token',
                'token',
            ],
            'grant_types': [
                'authorization_code',
                'refresh_token',
                'implicit',
                'client_credentials',
            ],
            'token_endpoint_auth_method': 'client_secret_basic',
            'initiate_login_uri': 'https://www.example-application.com/oauth2/login',
        }

          res = requests.post(f"{client_registration['ENDPOINT']}", json=json_data, headers=headers)
          
          if res.status_code == 201:
            assign_users = requests.put(f"{group_assignment['ENDPOINT']}/{res.json()['client_id']}/groups/{group_assignment['GROUP_ID']}", headers=headers)
            if assign_users.status_code == 200:
           
                flash(f"Your client id is {res.json()['client_id']}. Your client secret it {res.json()['client_secret']}",'success')
                return redirect(url_for('index'))
        
          flash(f"Something went wrong. Please try again",'warning')
          return redirect(url_for('index'))

        return render_template('register.html', form=form) 


if __name__ == '__main__':
    app.secret_key="secret_key"
    app.run(debug=True)