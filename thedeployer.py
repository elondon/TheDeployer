# The Deployer - python 2.7 app to configure and deploy apps to Ubuntu VMs.
# Eric London
# Current app support: Python, Flask, React, Nginx, Supervisor, Celery
import io
import json
import os

import click

from fabric.api import cd, env, lcd, put, prompt, local, sudo
from fabric.contrib.files import exists

from objectview import ObjectView

error_color = 'red'
info_color = 'green'
warning_color = 'yellow'


def load_config(app):
    config = {}
    with open('thedeployer.json', 'r') as f:
        config_location = json.load(f)
        with open(config_location[app], 'r') as f:
            data = json.load(f)
            config = data
    if config is None:
        click.echo(click.style(
            'Could not open config file. Please make sure you run set_config with the location of a config file '
            'with valid json.',
            fg=error_color))
    env.host_string = [config['remote_server']]
    env.user = config['remote_deploy_user']
    return config


@click.group()
def cli():
    pass


@cli.command()
@click.argument('app')
@click.argument('config')
def set_config(app, config):
    """Set the deployer config file path for an app. This file defines apps and how to configure and deploy them."""
    config_exists = os.path.isfile(config)
    if not config_exists:
        click.echo(click.style('Specified config file does not exist.', fg=error_color))
        return
    with open('thedeployer.json', 'w') as f:
        config_data = {app: config}
        json.dump(config_data, f)
    click.echo(click.style('Set config file for %s to %s' % (app, f), fg=info_color))


@cli.command()
@click.argument('app')
def install_dependencies(app):
    """Updates all packages and installs all app dependencies. This is meant to run once before the first deploy"""
    config = ObjectView(load_config(app))
    click.echo(click.style('Installing dependencies for %s on %s@%s' %
                           (app, config.remote_deploy_user, config.remote_server), fg=info_color))
    click.echo(click.style('Updating packages...', fg=info_color))
    sudo('apt-get -y update')
    sudo('apt-get upgrade')


def install_requirements():
    pass


def update_flask_app():
    pass


def update_react_app():
    pass


def deploy_and_configure_flask_app():
    pass


def deploy_and_configure_react_app():
    pass


def configure_nginx_for_flask():
    pass


def configure_nginx_for_react():
    pass


def configure_supervisor():
    pass


def configure_celery():
    pass
