# The Deployer - python 2.7 app to configure and deploy apps to Ubuntu VMs.
# Eric London
# Current app support: Python, Flask, React, Nginx, Supervisor, Celery
import json
import os
import sys

import click
from fabric.api import env

from dependencies.dependency_factory import get_dependency
from dependencies.nginx import Nginx
from fabric.operations import sudo

error_color = 'red'
info_color = 'green'
warning_color = 'yellow'


class Config(dict):
    def load(self):
        config = {}
        with open('thedeployer.json', 'r') as f:
            config_locations = json.load(f)
            for app_config in config_locations:
                with open(config_locations[app_config], 'r') as f:
                    data = json.load(f)
                    config[app_config] = data
                if config is None:
                    click.echo(click.style(
                        'Could not open config file. Please make sure you run set_config with the location'
                        ' of a config file with valid json.',
                        fg=error_color))
        self.update(config)


def get_config_for_app(config, app):
    if (config[app]) is None:
        click.echo(click.style('Config file for %s does not exist. Run set_config and define a config for %s' % app,
                               fg=error_color))
        return None
    env.host_string = config[app]['remote_server']
    env.user = config[app]['remote_deploy_user']
    env.password = config[app]['remote_deploy_password']  # todo obviously get rid of this!
    return config[app]


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
def cli(config):
    config.load()


@cli.command()
@click.argument('app')
@click.argument('config_path')
def set_config(app, config_path):
    """Set the deployer config file path for an app. This file defines apps and how to configure and deploy them."""
    config_exists = os.path.isfile(config_path)
    if not config_exists:
        click.echo(click.style('Specified config file does not exist.', fg=error_color))
        return
    with open('thedeployer.json', 'w') as f:
        config_data = {app: config_path}
        json.dump(config_data, f)
    click.echo(click.style('Set config file for %s to %s' % (app, f), fg=info_color))


@cli.command()
@click.argument('app')
@pass_config
def install_dependencies(config, app):
    """Updates all packages, installs, and configures all app dependencies.
    This is meant to run once before the first deploy"""
    config = get_config_for_app(config, app)
    if config is None:
        return
    click.echo(click.style('Installing dependencies for %s on %s@%s' %
                           (app, config['remote_deploy_user'], config['remote_server']), fg=info_color))
    click.echo(click.style('Updating packages...', fg=info_color))
    # sudo('apt-get -y update')
    # sudo('apt-get upgrade')
    for dep in config['app_requirements']:
        if dep['name'] != 'Supervisor':
            continue
        dep_class = get_dependency(dep)
        install_dependency(dep_class)
        configure_dependency(dep_class)
    click.echo(click.style('Dependencies for %s have been installed.' % app, fg=info_color))


def install_dependency(dependency):
    click.echo(click.style('Installing %s.' % dependency.dependency_name, fg=info_color))
    dependency.install()


def configure_dependency(dependency):
    click.echo(click.style('Configuring %s.' % dependency.dependency_name, fg=info_color))
    dependency.configure()


# just for fabric experiments.
@cli.command()
@click.argument('app')
@pass_config
def scratch_pad(config, app):
    config = get_config_for_app(config, app)
    if config is None:
        return
    res = sudo('id -u testSystemUser')
    click.echo(res)
    res = sudo('id -u testSystemUser2')
    click.echo(res)
