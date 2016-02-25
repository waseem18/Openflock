#[Openflock](http://www.openflock.co)

Gain contributors to your project or get your issues resolved by promoting them on Openflock.
* Find awesome projects or issues to work on. Also filter your feed according to your favourite language or topic.
* Is your Open source project really useful for the community? Fill in [this form](http://goo.gl/forms/5jLE4J89gK) to get your project on Openflock Hall of Fame.

* 
###Install
 
* Openflock has been written in Python (Webapp2 framework) on top of Google App Engine.
* We use Google datastore to store data.
* Forgive me if the code is inefficient. I hope to receive contributions from you ;)


####Here's how you can install Openflock locally...

* [Download Google App Engine](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
* Clone the repository.
* Download Semantic-UI 2.1.8 (https://github.com/Semantic-Org/Semantic-UI/releases/tag/2.1.8), extract it and place the extracted content in the folder `/static/dist/`.
* Openflock runs on GitHub API. To run Openflock locally, you also need a GitHub client id and client secret id. So [register](https://github.com/settings/applications/new) your GitHub application with `Homepage url` as `http://localhost:8080` and `callback url` as `http://localhost:9000/authorization`. Now you have a client id and client secret id.
* Now open `/handlers/LoginHandler.py` and place client id, client secret id, callback url in the places mentioned in the `LoginHandler.py` file.
* Run the command `python /path/of/dev_appserver.py /path/of/Openflock` (`dev_appserver.py` lies in google_appengine folder)
* Now you can find Openflock running `localhost:8080` and admin server running at `localhost:8000`.
* Raise an issue or contact me if you face any problems in installing Openflock locally.

###Note
* I think the code I wrote is not so efficient. Kindly forgive me for this.
* I hope to receive contributions from the community to improve Openflock :)


