import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'digiapproval_project.settings'
# allow us to import digiapproval_project
# digimail/config/../..
sys.path.append(os.path.join(os.path.dirname(__file__),'..','..'))

# This file contains python variables that configure Lamson for email processing.
import logging


# You may add additional parameters such as `username' and `password' if your
# relay server requires authentication, `starttls' (boolean) or `ssl' (boolean)
# for secure connections.
relay_config = {'host': 'localhost', 'port': 8825}

receiver_config = {'host': '0.0.0.0', 'port': 25}

handlers = ['app.handlers.digimail']

router_defaults = {'host': 'digiactive.com.au'}

template_config = {'dir': 'app', 'module': 'templates'}

# the config/boot.py will turn these values into variables set in settings
