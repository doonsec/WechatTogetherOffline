# -*- coding: utf-8 -*-
"""
@project ： src
@Time ： 2020/11/1 15:05
@Auth ： AJay13
@File ：manage.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from exts import db

app = create_app()

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
