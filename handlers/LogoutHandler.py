from imports import *
from config import *
from routes import *
from handlers import *

class LogoutHandler(BaseHandler):
	def get(self):
		if self.session.get('username'):
			del self.session['username']
		self.redirect('/')