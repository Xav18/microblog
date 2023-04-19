from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task
from app.odk import odk_post

import click

app = create_app()
cli.register(app)


@app.cli.command("get-odk-posts")
def get_odk_posts():
    # coller ce qui suit dans son crontab pour avoir une tache qui tourne avec cron
    # * * * * * cd /home/path_vers_le/microblog && venv/bin/flask get-odk-posts >> post_tries.log 2>&1
    odk_post()




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification, 'Task': Task}