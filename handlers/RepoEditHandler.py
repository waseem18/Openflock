from imports import *
from config import *
from routes import *
from handlers import *
from datetime import timedelta

class RepoEditHandler(BaseHandler):
	def get(self):
		if self.session.get('username'):
			username_session = self.session.get('username')
			current_url = self.request.url
			old_uid = current_url.split('/')[4].split('?')[0]
			is_issue = self.request.get('issue')
			if is_issue == 'True':
				state = 'open'
			else:
				state = 'none'
			url = self.request.get('url')
			verify = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :r",r=old_uid).get()
			#verify is NONE : BUG
			if str(verify.promoting_user) != str(username_session):
				self.response.out.write("You cannot edit someone else's promoted repository!")
				return
			navdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_session).get()
			avatar_url = navdata.avatar_url
			repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :r",r=str(old_uid))
			self.render('editrepo.html', username=str(username_session),navfullname=str(navdata.fullname),avatar_url=str(avatar_url),repodata=repodata,issue=is_issue,url=url,state=state)
		else:
			self.response.out.write("You are not authorized to access this URL.")

	def post(self):
		if self.session.get('username'):
			current_url = self.request.url
			old_uid = current_url.split('/')[4].split('?')[0]
			old_instance = db.GqlQuery("SELECT * FROM PromotedRepos WHERE uid= :r",r=old_uid).get()
			old_view_of = int(old_instance.views_of)
			old_views_gh =  int(old_instance.views_gh)

			old_instance.delete()
			promoting_user = self.session.get('username')
			reponame = self.request.get('issue_title')
			description = self.request.get('issue_description')
			simple_reason = self.request.get('reason')
			detailed_reason = self.request.get('detailed_reason')
			contact_link = self.request.get('contact_link')
			language = self.request.get('language')
			issue = self.request.get('issue')
			state = self.request.get('state')
			is_beginner = self.request.get('isbeginner')
			genre = self.request.get('genre')
			hof = False
			if genre == "0":
				genre=""
			url_entered = self.request.get('url_entered')
			
			ud = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=promoting_user).get()
			pi = PromotedRepos(promoting_user=promoting_user,is_beginner=is_beginner,genre=genre,repo_html_url=url_entered,reponame=reponame,promoting_user_avatar=ud.avatar_url,description=description,language=language,simple_reason=simple_reason,detailed_reason=detailed_reason,contact_link=contact_link,issue=issue,state=state)
			pi.put()
			vid = pi.key().id()
			pi.uid=str(vid)
			pi.views_of = old_view_of
			pi.views_gh = old_views_gh
			pi.put()
			self.redirect('/')


			
