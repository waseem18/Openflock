from imports import *
from config import *
from routes import *
from handlers import *


class UserData(db.Model):
	username = db.StringProperty()
	email = db.StringProperty()
	fullname = db.StringProperty()
	website = db.StringProperty()
	location = db.StringProperty()
	lang_list = db.ListProperty(str,default=[])
	public_repos = db.StringProperty()
	followers = db.StringProperty()
	following = db.StringProperty()
	avatar_url = db.StringProperty()
	access_token = db.StringProperty()
	orgs = db.ListProperty(str,default=[])


class RepoData(db.Model):
	reponame=db.StringProperty()
	repo_html_url=db.StringProperty()
	username = db.StringProperty()
	language = db.StringProperty()
	forks = db.StringProperty()
	stars = db.StringProperty()
	website = db.StringProperty()
	description = db.StringProperty()


class PromotedRepos(db.Model):
	promoting_user = db.StringProperty()
	reponame = db.StringProperty()
	uid = db.StringProperty()
	language = db.StringProperty()
	is_beginner = db.StringProperty()
	repo_html_url=db.StringProperty()
	description=db.StringProperty(multiline=True)
	simple_reason = db.StringProperty()
	detailed_reason = db.StringProperty(multiline=True)
	promoted_time = db.DateTimeProperty(auto_now_add=True)
	contact_link = db.StringProperty()	
	promoting_user_avatar = db.StringProperty()
	issue = db.StringProperty()
	state = db.StringProperty()
	genre = db.StringProperty()
	views_of = db.IntegerProperty(default=0)
	views_gh = db.IntegerProperty(default=0)
	hof = db.BooleanProperty()
