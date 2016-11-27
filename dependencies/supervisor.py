from dependencies.dependency import Dependency
from fabric.operations import sudo, put


class Supervisor(Dependency):
    def __init__(self, config):
        super(Supervisor, self).__init__(config)
        self.local_config_file = config['local_config_file']

    def install(self):
        sudo('apt-get install -y supervisor')

    def configure(self):
        put(self.local_config_file, '/etc/supervisor/conf.d/', use_sudo=True)

    def uninstall(self):
        pass

    def update(self):
        pass
