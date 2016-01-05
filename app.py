# coding=utf8
#

"""
app module.
included all configs in this module
"""

import os
from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import Response
from flask import redirect

from const import admin_meta
from utils.config import Config


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')


app = Flask(__name__, template_folder=tmpl_dir)
app.config['admin_meta'] = admin_meta

app.secret_key = 'PS#yio`%_!((f_or(%)))s'

config = Config()
