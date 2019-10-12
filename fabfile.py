import os

from fabric import Connection, task, Config

host = os.getenv('DEPLOY_HOST')
port = os.getenv('DEPLOY_PORT')
user = os.getenv('DEPLOY_USER')
password = os.getenv('DEPLOY_PASSWORD')
project_dir = os.getenv('PROJECT_DIR')
service = os.getenv('SERVICE_NAME')
python = os.getenv('PYTHON')

config = Config({
    'reject-unknown-hosts': True,
    'shell': '/bin/bash -lic'
})


@task
def deploy(ctx):
    with Connection(host=host, port=int(port), user=user,
                    connect_kwargs={'key_filename': 'deploy_key'}, config=config) as con:
        with con.cd(os.path.join('$HOME', project_dir)):
            con.run('git checkout master')
            con.run('git pull origin master')
            with con.prefix(f'source {os.path.join("$HOME", project_dir, ".env", "bin", "activate")}'):
                con.run(f'{python} manage.py migrate --noinput')
                con.run(f'{python} manage.py collectstatic --noinput')
        con.sudo(f'systemctl stop {service}')
        con.sudo(f'systemctl start {service}')
