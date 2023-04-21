from pyodk.client import Client
from app.models import User, Post
from app import db
from datetime import datetime
import time
import click
import requests, json, logging
import csv

log = logging.getLogger("app")

client = Client(config_path="app/.pyodk_config.toml")
project_id = client.config.central.default_project_id
form_id = 'mb_post'

def update_review_state(project_id, form_id, submission_id, review_state):
    """
    Update the review state
    :param projet id : the project id
    :type projecet_id: int
    :param form_id id : the xml form id
    :type form_id: str
    :param review_state id : the value of the state for update
    :type form_id: str ("approved", "hasIssues", "rejected")
    """
    token = client.session.auth.service.get_token(
        username=client.config.central.username,
        password=client.config.central.password,
    )
    review_submission_response = client.patch(
        f"/projects/{project_id}/forms/{form_id}/submissions/{submission_id}",
        data=json.dumps({"reviewState": review_state}),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )
    try:
        assert review_submission_response.status_code == 200
    except AssertionError:
        log.error("Error while update submission state")
        print(review_submission_response.status_code)
    

def write_users():
    with open('users.csv', 'w') as file:
        header=['name', 'label']
        writer = csv.DictWriter(file, fieldnames=header, delimiter=',')
        writer.writeheader()
        users = User.query.all()
        for user in users:
            username=user.username
            id = user.id
            row = {'name' : str(id), 'label' : str(username)}
            writer.writerow(row)


def odk_post():
    modded_lines=0
    print('\n' + str(datetime.now()))
    form_data = client.submissions.get_table(form_id="mb_post", project_id=project_id) #submission data
    for submission in form_data.get('value'):
        review_state = submission.get('__system').get('reviewState')
        if not str(review_state)=='approved':
            modded_lines+=1
            id = int(submission.get('sign_in').get('user'))
            user=User.query.get(id)
            content = submission.get('post').get('content')
            sub_id = submission.get('__id') 
            post = Post(body=str(content), author=user)
            db.session.add(post)
            update_review_state(project_id, 'mb_post', sub_id,  'approved')
    print(str(modded_lines) + " submissons added to db.")        
    db.session.commit()
    
def upload_file(file_name, project_id, form_id):
    with open(file_name) as file:
        data = file.read()
        response = client.post(
            f"projects/{project_id}/forms/{form_id}/draft/attachments/{file_name}",
            data=data.encode('utf-8')
        )
        if response.status_code == 200:
            # print('file uploaded')
            click.echo(click.style('file uploaded', fg='green', bold=True))
        else:
            #print("Error " + str(response.status_code))
            click.echo(click.style("Error " + str(response.status_code), fg='red', bold=True))

def to_draft(project_id, form_id):
    response = client.post(
        f"projects/{project_id}/forms/{form_id}/draft/")
    if response.status_code == 200:
        #print("The form is in draft state")
        click.echo(click.style('The form is in draft state', fg='green', bold=True))
    else:
        #print("Error " + str(response.status_code))
        click.echo(click.style("Error " + str(response.status_code), fg='red', bold=True))

def publish(project_id, form_id):
    version = datetime.now()
    response = client.post(
        f"projects/{project_id}/forms/{form_id}/draft/publish?version={version}"
    )
    if response.status_code == 200:
        click.echo(click.style('form published', fg='green', bold=True))
    else:
        #print("Error " + str(response.status_code))
        click.echo(click.style("Error " + str(response.status_code), fg='red', bold=True))

def add_file_to_published_form(file_name, project_id, form_id):
    write_users()
    to_draft(project_id, form_id)
    upload_file(file_name, project_id, form_id)
    publish(project_id, form_id)
   



