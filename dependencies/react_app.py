from dependencies.dependency import Dependency
from fabric.contrib.files import exists
from fabric.operations import sudo, put


class ReactApp(Dependency):
    def __init__(self, config):
        super(ReactApp, self).__init__(config)
        self.local_dist_folder = config['local_dist_folder']
        self.remote_deploy_folder = config['remote_deploy_folder']

    def install(self):
        if exists(self.remote_deploy_folder) is False:
            sudo('mkdir %s' % self.remote_deploy_folder)
        put(self.local_dist_folder, self.remote_deploy_folder, use_sudo=True)

    def configure(self):
        pass

    def uninstall(self):
        pass

    def update(self):
        put(self.local_dist_folder, self.remote_deploy_folder, use_sudo=True)
