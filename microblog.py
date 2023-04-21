from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task
from app.odk import odk_post, add_file_to_published_form, write_users
import click

app = create_app()
cli.register(app)


@app.cli.command("get-odk-posts")
def get_odk_posts():
    """Puts the posts submitted on ODK into the database"""
    # coller ce qui suit dans son crontab pour avoir une tache qui tourne avec cron
    # * * * * * cd /home/path_vers_le/microblog && venv/bin/flask get-odk-posts >> post_tries.log 2>&1
    odk_post()


@app.cli.command("update-odk")
@click.argument('file_name')
@click.argument('project_id')
@click.argument('form_id')
def update_odk_file(file_name, project_id, form_id):
    """updates ODK  project {project_id} form {form_id} with the updated file {file_name}"""
    add_file_to_published_form(file_name, project_id, form_id)



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message, 'Notification': Notification, 'Task': Task}