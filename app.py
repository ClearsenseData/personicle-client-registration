from crypt import methods
from sys import api_version
from flask import Flask, render_template, url_for, flash, redirect,request, logging
import requests
from header import headers
from config import client_registration,group_assignment_id, group_assignment_endpoint
from forms import NewSecretDeleteGetForm, RegisterForm, UpdateForm
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        client_name = form.client_name.data
        client_uri = form.client_uri.data
        redirect_uri = form.redirect_uri.data

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
        # 'initiate_login_uri': 'https://www.example-application.com/oauth2/login',
    }

        res = requests.post(f"{client_registration}", json=json_data, headers=headers)
        
        if res.status_code == 201:
            assign_users = requests.put(f"{group_assignment_endpoint}/{res.json()['client_id']}/groups/{group_assignment_id}", headers=headers)
            if assign_users.status_code == 200:
            
                flash(f"Your client id is {res.json()['client_id']}. Your client secret it {res.json()['client_secret']}",'success')
                return redirect(url_for('index'))

            flash(f"Something went wrong. Please try again",'warning')
            return redirect(url_for('index'))

    return render_template('register.html', form=form) 


@app.route('/update', methods=['GET','POST','PUT'])
def update_app():
    form = UpdateForm(request.form)

    if request.method == 'POST' and form.validate():
        client_id = form.client_id.data
        client_name = form.client_name.data
        client_uri = form.client_uri.data
        redirect_uri = form.redirect_uri.data

        json_data = {
            'client_id': client_id,
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
            # 'initiate_login_uri': 'https://www.example-application.com/oauth2/login',
        }

        res = requests.put(f"{client_registration}/{client_id}", json=json_data, headers=headers)
        print(res.json())
        if res.status_code == 200:
            flash("Your app settings are successfully updated",'success')
            return redirect(url_for('index'))
        else:
            flash(f"Something went wrong. Please try again.",'warning')
    return render_template('update.html', form=form)


@app.route('/newSecret', methods=['GET','POST'])
def new_secret():
    form = NewSecretDeleteGetForm(request.form)

    if request.method == 'POST' and form.validate():
        client_id = form.client_id.data

        res = requests.post(f"{client_registration}/{client_id}/lifecycle/newSecret", headers=headers)

        if res.status_code == 200:
            print(res.json())
            flash(f"Your new client secret is {res.json()['client_secret']}", 'success')
        else :
            flash(f"Something went wrong. Unable to generate new secret", 'warning')
    return render_template('newSecret.html',form=form)


@app.route('/client', methods=['GET','POST'])
def get_details():
    form = NewSecretDeleteGetForm(request.form)
    if request.method == 'POST' and form.validate():
        client_id = form.client_id.data

        res = requests.get(f"{client_registration}/{client_id}", headers=headers)
        
        if res.status_code == 200:
            flash(f"Your client app  details are {res.json()}",'success')
            print(res.json())
        else:
            flash(f"Unable to fetch your app details.",'warning')
    return render_template('details.html', form=form) 


@app.route('/delete',methods=['GET','DELETE','POST'])
def delete_app():
    form = NewSecretDeleteGetForm(request.form)
    
    if request.method == 'POST' and form.validate():
        client_id = form.client_id.data

        res = requests.delete(f"{client_registration}/{client_id}", headers=headers)
        
        if res.status_code == 204:
            flash(f"Your client app  {client_id} is deleted.",'warning')
            return redirect(url_for('index'))
        else:
                flash(f"Unable to delete {client_id}. Please make sure your client id is correct.",'warning')
    return render_template('delete.html', form=form) 



   



if __name__ == '__main__':
    app.secret_key="secret_key"
    app.run(debug=True)


    