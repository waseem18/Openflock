from imports import *
from config import *
from routes import *
from handlers import *
from datetime import timedelta


class RepoHandler(BaseHandler):
	def get(self):
		username=""
		fullname=""
		avatar_url=""
		if self.session.get('username'):
			username_session = self.session.get('username')
			navdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_session).get()
			username = navdata.username
			fullname=navdata.fullname
			avatar_url = navdata.avatar_url
		current_url = self.request.url
		promoted_repo_uid = current_url.split('/')[4]
		verify = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :r",r=promoted_repo_uid).fetch(limit=2)
			

		if len(verify) > 0:
			clicked = self.request.cookies.get(str(promoted_repo_uid))
			repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :r",r=promoted_repo_uid)
			repodata_views = repodata.get()
			genre = repodata_views.genre
			difficulty = repodata_views.is_beginner
			if clicked != 'True':
				self.response.set_cookie(str(promoted_repo_uid),'True',max_age=10800,path='/')
				repodata_views.views_of += 1
				repodata_views.put()
			self.render('repo_info.html',repodata=repodata,genre=genre,difficulty=difficulty,username=username,fullname=fullname,avatar_url=avatar_url)
		else:
			self.response.out.write("Repository/Issue with such name hasn't yet been promoted!")
			return


class GitHubView(BaseHandler):
	def get(self):
		current_url = self.request.url
		uid = current_url.split('?')[0].split('/')[4]
		url = current_url.split('?')[1].split('=')[1]
		clicked = self.request.cookies.get(str(uid+'gh'))
		if clicked != 'True':
			self.response.set_cookie(str(uid+'gh'),'True',max_age=10800,path='/')
			repodata_views = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :u",u=uid).get()
			repodata_views.views_gh += 1
			repodata_views.put()
		self.redirect(url)



