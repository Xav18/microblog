from pyodk.client import Client
from app.models import User, Post
from app import db
from datetime import datetime
import time

import requests, json, logging

log = logging.getLogger("app")

client = Client(config_path="app/.pyodk_config.toml")


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
    review_submission_response = requests.patch(
        f"{client.config.central.base_url}/v1/projects/{project_id}/forms/{form_id}/submissions/{submission_id}",
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
    client.close()






def odk_post():
    i=0
    print('+\n' + str(datetime.now()))
    user = User.query.filter_by(username='odk').first_or_404()
    form_data = client.submissions.get_table(form_id="mb_post", project_id=6) #submission data
    for submission in form_data.get('value'):
        review_state = submission.get('__system').get('reviewState')
        if not str(review_state)=='approved':
            i+=1
            content = submission.get('content')
            sub_id = submission.get('__id') 
            post = Post(body=str(content), author=user)
            db.session.add(post)
            update_review_state(6, 'mb_post', sub_id,  'approved')
    print(str(i) + " submissons added to db.")        
    db.session.commit()
    

   



