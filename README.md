# microblog
Crée avec le tuto de Miguel Grinberg

coller ce qui suit dans son crontab pour avoir une tache qui tourne avec cron 
     * * * * * cd /home/path_vers_le/microblog && venv/bin/flask get-odk-posts >> post_tries.log 2>&1