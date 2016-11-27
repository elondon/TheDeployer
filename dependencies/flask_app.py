from dependencies.dependency import Dependency
from fabric.context_managers import cd, path
from fabric.contrib.files import exists, local
from fabric.operations import sudo, put


def install_python():
    sudo('apt-get install python3-pip python3-dev')
    sudo('pip3 install virtualenv')


class FlaskApp(Dependency):
    def __init__(self, config):
        super(FlaskApp, self).__init__(config)
        self.app_name = config['app_name']
        self.local_folder = config['local_folder']
        self.remote_folder = config['remote_folder']
        self.remote_system_user = config['remote_system_user']
        self.deploy_files = config['deploy_files']
        self.deploy_folders = config['deploy_folders']
        self.remote_log_folder = config['remote_log_folder']
        self.virtual_env = config['virtual_env']
        self.use_alembic = config['use_alembic']
        self.alembic_deploy_script = config['alembic_deploy_script']

    def install(self):
        install_python()

    def configure(self):
        sudo('adduser --system %s' % self.remote_system_user)
        if exists(self.remote_folder) is False:
            sudo('mkdir %s', self.remote_folder)
        self.setup_virtualenv()
        self.copy_files()
        sudo(self.virtual_env + 'pip install -r %s/requirements.txt' % self.remote_folder)
        if self.remote_log_folder is not None and exists(self.remote_log_folder) is False:
            sudo('mkdir %s' % self.remote_log_folder)
        if self.use_alembic:
            self.deploy_alembic()

    def uninstall(self):
        pass

    def update(self):
        pass

    def setup_virtualenv(self):
        with cd(self.remote_folder):
            sudo('virtualenv .venv')

    def copy_files(self):
        for app_file in self.deploy_files:
            put(self.local_folder + '/%s' % app_file, self.remote_folder, use_sudo=True)
        for app_folder in self.deploy_folders:
            put(self.local_folder + '/' + app_folder, self.remote_folder, use_sudo=True)

    def deploy_alembic(self):
        sudo('source %s' % self.alembic_deploy_script)
