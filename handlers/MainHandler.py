from imports import *
from config import *
from routes import *
from handlers import *




class MainHandler(BaseHandler):
	def get(self):
		if self.session.get('username'):
			username = self.session.get('username')
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username)
			f = self.request.get('filter')
			value = self.request.get('value')
			if f == 'language':
				repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE language= :l",l=str(value))
			elif f== 'genre':
				repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE genre= :g",g=str(value))
			elif f == 'bitesize':
				repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE is_beginner= :b",b='Beginner')

			else:
				repodata = db.GqlQuery("SELECT * FROM PromotedRepos ORDER BY promoted_time DESC")
			self.render('homepage.html',repodata=repodata,userdata=userdata)
		else:
			self.render('index.html')