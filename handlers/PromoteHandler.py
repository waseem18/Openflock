from imports import *
from config import *
from routes import *
from handlers import *
from datetime import timedelta
from urlparse import urlparse

class PromoteHandler(BaseHandler):
	def get(self):
		if self.session.get('username'):
			username_session = self.session.get('username')
			headers = {'User-Agent':'Openflock'}
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_session)
			at = userdata.get()
			current_url = self.request.url
			reponame = current_url.split('/')[4].split('?')[0]
			params = {}
			user_or_org = self.request.get('project')
			if user_or_org == 'org':
				params['flag']=""
				org_username = self.request.get('organization')
				org_repo = urlparse(current_url).path.split('/')[2]
				params_org = {}
				language=""
				urll = 'https://api.github.com/repos/'+str(org_username)+'/'+str(org_repo)+'?access_token='+str(at.access_token)
				cont = requests.get(urll,headers=headers)
				if cont.status_code == 200:
					data = json.loads(cont.content)
					params['reponame'] = str(data['name'])
					params['description'] = str(data['description'])
					params['repo_html_url'] = str(data['html_url'])
					language = str(data['language'])
					if language == 'None':
						language = ""
				else:
					self.response.out.write(str(cont.status_code)+" There's something wrong while connecting to GitHub API!")
					return

				if self.request.get('issue')=="True" and self.request.get('id'):
					params['flag']="1"
					params['iid'] = self.request.get('id')
					url = 'https://api.github.com/repos/'+str(org_username)+'/'+str(org_repo)+'/issues/'+str(params['iid'])+'?access_token='+str(at.access_token)
					cont = requests.get(url)
					if cont.status_code == 200:
						data = json.loads(cont.content)
						params['issue_title'] = str(data['title'])
						params['issue_state'] = str(data['state'])
						params['issue_description'] = str(data['body'])
						language= ""
						url_entered = self.request.get('url_entered')
						self.render('promoting.html',userdata=userdata,url_entered=url_entered,language=language,**params)
					else:
						self.response.out.write(str(cont.status_code)+"There's something wrong while connecting to GitHub API!")
				else:
					self.render('promoting.html',userdata=userdata,language=language,**params)

			elif user_or_org == 'user':
				repodata = db.GqlQuery("SELECT * FROM RepoData WHERE reponame= :r",r=reponame).get()
				if not repodata:
					self.response.out.write("<h3>Currently you cannot promote a forked repository or repository which you are not owner of! If this is not the issue, kindly contact us or raise an issue on GitHub</h3>")
					return
				params['reponame'] = str(repodata.reponame)
				params['description'] = str(repodata.description)
				params['repo_html_url'] = str(repodata.repo_html_url)
				language = str(repodata.language)
				if language == "none":
					language=""
				params['flag'] = ""

				if self.request.get('issue')=="True" and self.request.get('id'):
					params['flag']="1"
					params['iid'] = self.request.get('id')
					url = 'https://api.github.com/repos/'+str(username_session)+'/'+str(reponame)+'/issues/'+str(params['iid'])+'?access_token='+str(at.access_token)
					
					issue_json_data = requests.get(url,headers=headers)
					if issue_json_data.status_code != 200:
						self.response.out.write("Either there's no such issue or there's no such repository!")
						return
					d = json.loads(issue_json_data.content)
					params['issue_title'] = str(d['title'])
					params['issue_state'] = str(d['state'])
					params['issue_description'] = str(d['body'])
					url_entered = self.request.get('url_entered')
					self.render('promoting.html',userdata=userdata,url_entered=url_entered,language=language,**params)
				else:
					self.render('promoting.html',userdata=userdata,language=language,**params)
		else:
			self.redirect('/')

	def post(self):
		if self.session.get('username'):
			promoting_user = self.session.get('username')
			reponame = self.request.get('issue_title')
			description = self.request.get('issue_description')
			simple_reason = self.request.get('reason')
			detailed_reason = self.request.get('detailed_reason')
			if len(detailed_reason)>300:
			    detailed_reason = detailed_reason[:300]
			contact_link = ""
			language = self.request.get('language')
			if language == "not_related":
				language = ""
			issue = self.request.get('issue')
			state = self.request.get('state')
			is_beginner = self.request.get('isbeginner')
			genre = self.request.get('genre')
			hof = False
			if genre == "0":
				genre=""
			url_entered = self.request.get('url_entered')
			if str(issue) == "none":
			    url_entered = "https://github.com/"+str(promoting_user)+"/"+str(reponame)
			    issue = 'False'

			ud = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=promoting_user).get()
			if not ud:
				self.response.out.write("There's no such user")
				return
			pi = PromotedRepos(promoting_user=promoting_user,hof=hof,genre=genre,is_beginner=is_beginner,repo_html_url=url_entered,reponame=reponame,promoting_user_avatar=ud.avatar_url,description=description,language=language,simple_reason=simple_reason,detailed_reason=detailed_reason,contact_link=contact_link,issue=issue,state=state)
			pi.put()
			vid = pi.key().id()

			cial = db.GqlQuery("SELECT * FROM PromotedRepos WHERE detailed_reason= :d",d=str(detailed_reason)).fetch(limit=2)
			if len(cial):
				itbd = db.GqlQuery("SELECT * FROM PromotedRepos WHERE detailed_reason= :d",d=str(detailed_reason)).get()
				itbd.delete()


			pi.uid=str(vid)
			pi.put()
			self.redirect('/')


class PromoteVerify(BaseHandler):
	def get(self):
		if self.session.get('username'):
			username_session = self.session.get('username')
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username_session).get()
			if not userdata:
				self.response.out.write("There's no such user available!")
				return
			orgs = userdata.orgs
			url_entered = self.request.get('url_entered')
			if url_entered[-1]=='/':
				url_entered = url_entered[:-1]
			split_result = urlparse(url_entered)

			if split_result.netloc=="github.com" and len(split_result.path.split('/'))>=3 and split_result.path.split('/')[1]==str(username_session) and split_result.path.split('/')[2]:
				promoting_repo = str(split_result.path.split('/')[2])
				is_repo_present = db.GqlQuery("SELECT * FROM RepoData WHERE reponame= :r",r=promoting_repo).fetch(limit=2)
				if is_repo_present>0 and len(split_result.path.split('/'))==3:
					self.redirect('/promote/'+str(promoting_repo)+'?project=user')
				elif len(split_result.path.split('/'))==5 and split_result.path.split('/')[3]=="issues" and split_result.path.split('/')[4]:
					issue_id = split_result.path.split('/')[4]
					self.redirect('/promote/'+str(promoting_repo)+'?issue=True&id='+str(issue_id)+'&url_entered='+str(url_entered)+'&project=user')
				else:
					self.response.out.write("<h3>There's something wrong with the url. Check the URL once clearly.</h3>")
			

			elif split_result.netloc=="github.com" and len(split_result.path.split('/'))>=3 and split_result.path.split('/')[1] in orgs and split_result.path.split('/')[2]:
				#Check if the user is trying to promote a repository from one of his organizations.
				#self.response.out.write("User is trying to promote a repo from his organization!"+str(split_result.path.split('/')[1]))
				#check if repo exists - cire
				cire = requests.get('https://api.github.com/repos/'+str(split_result.path.split('/')[1])+'/'+str(split_result.path.split('/')[2])+'?access_token='+str(userdata.access_token))
				if cire.status_code == 200 and len(split_result.path.split('/'))==3:
					self.redirect('/promote'+'/'+str(split_result.path.split('/')[2])+'?project=org&organization='+str(split_result.path.split('/')[1]))
				elif cire.status_code==200 and len(split_result.path.split('/'))==5 and split_result.path.split('/')[3]=="issues" and split_result.path.split('/')[4]:
					issue_id = split_result.path.split('/')[4]
					self.redirect('/promote/'+str(split_result.path.split('/')[2])+'?issue=True&id='+str(issue_id)+'&url_entered='+str(url_entered)+'&project=org&organization='+str(split_result.path.split('/')[1]))
				else:
					self.response.out.write("<h3>There's something wrong with the url. Check the URL once clearly.</h3>")



				
			else:
				self.response.out.write("<h3>The URL you have entered in not of a GitHub repository or you are trying to promote someone else's repo.</h3>")

		else:
			self.response.out.write("You are not authorized!")




class MyPromotedRepos(BaseHandler):
	def get(self):
		if self.session.get('username'):
			username = self.session.get('username')
			userdata = db.GqlQuery("SELECT * FROM UserData WHERE username= :u",u=username)
			userdata_get = userdata.get()
			len_lang_list = len(userdata_get.lang_list)
			lang_list = userdata_get.lang_list
			repodata = db.GqlQuery("SELECT * FROM PromotedRepos WHERE promoting_user= :u ",u=username)
			ispromoted = repodata.fetch(limit=2)
			notpromoted = ""
			if len(ispromoted) == 0:
				notpromoted = "1"
			self.render('promoted_repos.html',notpromoted=notpromoted,len_lang_list=len_lang_list,lang_list=lang_list,userdata=userdata,repodata=repodata)
		else:
			self.response.out.write("You are not authorized!")





