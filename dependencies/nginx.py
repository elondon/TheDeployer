from fabric.context_managers import lcd, cd
from fabric.contrib.files import exists
from fabric.operations import sudo, put

from dependencies.dependency import Dependency


class Nginx(Dependency):
    def __init__(self, config):
        super(Nginx, self).__init__(config)
        self.local_config_folder = config['local_config_folder']
        self.remote_config_folder = config['remote_config_folder']
        # todo validate paths.
        self.local_ssl_crt = config['local_ssl_crt']
        self.local_ssl_key = config['local_ssl_key']

    def install(self):
        sudo('apt-get install nginx')

    def configure(self):
        sudo('/etc/init.d/nginx start')
        if exists('/etc/nginx/sites-enabled/default'):
            sudo('rm /etc/nginx/sites-enabled/default')
        if exists('/etc/nginx/sites-enabled/%s' % self.dependency_name) is False:
            sudo('touch /etc/nginx/sites-available/%s' % self.dependency_name)
            sudo('ln -s /etc/nginx/sites-available/%s' % self.dependency_name +
                 ' /etc/nginx/sites-enabled/%s' % self.dependency_name)
        with lcd(self.local_config_folder):
            with cd(self.remote_config_folder):
                put(self.local_config_folder, '/etc/nginx/sites-available/', use_sudo=True)

        if exists('/etc/ssl') is False:
            sudo('mkdir /etc/ssl')
        if exists('/etc/ssl/certs') is False:
            sudo('mkdir /etc/ssl/certs')
        if exists('/etc/ssl/private') is False:
            sudo('mkdir /etc/ssl/private')

        put(self.local_ssl_crt, '/etc/ssl/certs', use_sudo=True)
        put(self.local_ssl_key, '/etc/ssl/private', use_sudo=True)

        sudo('/etc/init.d/nginx restart')

    def uninstall(self):
        sudo('apt-get uninstall nginx')

    def update(self):
        pass
