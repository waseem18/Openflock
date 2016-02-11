import webapp2
import jinja2
import requests
import os
import sys
import time
import logging
import urllib2
import json
import re
from operator import itemgetter
from datetime import datetime
from google.appengine.ext import db
from webapp2_extras import sessions
from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)