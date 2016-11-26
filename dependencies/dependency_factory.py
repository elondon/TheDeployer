from dependencies.nginx import Nginx
from dependencies.postgres import Postgres
from dependencies.supervisor import Supervisor

# todo change this to dynamic instantiation?


def get_dependency(dep):
    if dep['name'] == 'Nginx':
        return Nginx(dep)
    if dep['name'] == 'Postgres':
        return Postgres(dep)
    if dep['name'] == 'Supervisor':
        return Supervisor(dep)
