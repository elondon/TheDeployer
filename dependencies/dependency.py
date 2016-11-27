from abc import ABCMeta, abstractmethod


class Dependency:
    def __init__(self, dep_config):
        self.dependency_name = dep_config['name']
        self.config = dep_config

    __metaclass__ = ABCMeta

    @abstractmethod
    def install(self): pass

    @abstractmethod
    def configure(self): pass

    @abstractmethod
    def uninstall(self): pass

    @abstractmethod
    def update(self): pass
