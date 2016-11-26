from fabric.context_managers import settings, hide
from fabric.operations import sudo, run

from dependencies.dependency import Dependency


def run_as_pg(command):
    return sudo('sudo -u postgres %s' % command)


def pg_user_exists(username):
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(username)s';"''' % locals())
    return res == "1"


def pg_database_exists(database):
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_database WHERE datname = '%(database)s';"''' % locals())
    return res == "1"


def pg_create_user(username, password):
    run_as_pg('''psql -t -A -c "CREATE USER %(username)s WITH PASSWORD '%(password)s';"''' % locals())


def pg_create_database(database, owner):
    run_as_pg('createdb %(database)s -O %(owner)s' % locals())


class Postgres(Dependency):
    def __init__(self, config):
        super(Postgres, self).__init__(config)
        self.db_user = config['db_user']
        self.db_password = config['db_password']
        self.create_db = config['create_db']

    def install(self):
        sudo('apt-get install postgresql postgresql-contrib')

    def configure(self):
        if not pg_user_exists(self.db_user):
            pg_create_user(self.db_user, self.db_password)
        if not pg_database_exists(self.create_db):
            pg_create_database(self.create_db, self.db_user)

    def uninstall(self):
        pass

    def update(self):
        pass

