# import Flask Script object
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from APP import app, db
# Init manager object via app object
manager = Manager(app)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server())

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
