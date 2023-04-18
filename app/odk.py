from pyodk.client import Client
from app.models import User, Post
from app import db


submitted = []

def odk_post():
    user = User.query.filter_by(username='odk').first_or_404()
    client = Client(config_path="app/.pyodk_config.toml")
    projects = client.projects.list()
    forms = client.forms.list()
    submissions = client.submissions.list("mb_post") #submission object
    form_data = client.submissions.get_table(form_id="mb_post", project_id=6) #submission data
    i = 0
    while i < len(form_data.get('value')) :
        submission = form_data.get('value')[i]
        if submission not in submitted:
            content = submission.get('content')
            post = Post(body=str(content), author=user)
            submitted.append(submission)
            db.session.add(post)
        i = i+1
    db.session.commit()



