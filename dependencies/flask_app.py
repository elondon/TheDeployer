from dependencies.dependency import Dependency
from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.operations import sudo


def install_python():
    sudo('apt-get install python3-pip python3-dev')
    sudo('pip3 install virtualenv')


class FlaskApp(Dependency):
    def __init__(self, config):
        super(FlaskApp, self).__init__(config)
        self.app_name = config['app_name']
        self.local_folder = config['local_folder']
        self.remote_folder = config['remote_folder']
        self.remote_user = config['remote_user']
        self.remote_user_pw = config['remote_user_pw']

    def install(self):
        install_python()
        self.setup_virtualenv()


    def configure(self):
        pass

    def uninstall(self):
        pass

    def update(self):
        pass

    def setup_virtualenv(self):
        if exists(self.remote_folder) is False:
            sudo('mkdir %s', self.remote_folder)
        with cd(self.remote_folder):
            sudo('virtualenv .venv')
        sudo('source .venv/bin/activate')

    def copy_files(self):
        pass
