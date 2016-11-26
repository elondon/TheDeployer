from dependencies.dependency import Dependency


class Supervisor(Dependency):
    def __init__(self, config):
        super(Supervisor, self).__init__(config)

    def install(self):
        pass

    def configure(self):
        pass

    def uninstall(self):
        pass

    def update(self):
        pass
