from imports import *
from config import *
from routes import *
from handlers import *
from datetime import timedelta



class ProfileHandler(BaseHandler):
	def get(self):
		username_session = self.session.get('username')
		if username_session:
			navdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_session).get()
			len_lang_list = len(navdata.lang_list)
			none=""
			lang_list = navdata.lang_list
			
			fullnam = navdata.fullname
			avatar_url = navdata.avatar_url
			current_url = self.request.url
			username_url = current_url.split('/')[4]
			isuser = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_url).fetch(limit=2)
			if len(isuser)==0:
				self.response.out.write("There's no such user currently on Openflock.")
				return
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_url)
			repodata = db.GqlQuery("SELECT * FROM RepoData WHERE username= :u",u=username_url)
			noofrepos = repodata.fetch(limit=2)
			self.render('userprofile.html',userdata=userdata,repodata=repodata,avatar_url=avatar_url,navfullname=fullnam,noofrepos=noofrepos,navusername=username_session,len_lang_list=len_lang_list,lang_list=lang_list)
		else:
			current_url = self.request.url
			username_url = current_url.split('/')[4]
			isuser = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_url).fetch(limit=2)
			if len(isuser)==0:
				self.response.out.write("There's no such user currently on Openflock.")
				return
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_url)
			repodata = db.GqlQuery("SELECT * FROM RepoData WHERE username= :u",u=username_url)
			self.render('userprofile.html',userdata=userdata,repodata=repodata,navfullname="")