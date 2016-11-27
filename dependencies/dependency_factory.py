from dependencies.flask_app import FlaskApp
from dependencies.nginx import Nginx
from dependencies.postgres import Postgres
from dependencies.supervisor import Supervisor

# todo change this to dynamic instantiation?


def get_dependency(dep):
    if dep['name'].upper() == 'FLASKAPP':
        return FlaskApp(dep)
    if dep['name'].upper() == 'NGINX':
        return Nginx(dep)
    if dep['name'].upper() == 'POSTGRES':
        return Postgres(dep)
    if dep['name'].upper() == 'SUPERVISOR':
        return Supervisor(dep)
