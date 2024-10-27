### Personalized Music Recommendations System    

##### Introduction:    

The core problem addressed by this project is the enhancement of music recommendation systems to deliver highly personalized and relevant music suggestions to users. 



This project uses [Flask](https://flask.palletsprojects.com/en/stable/) to create the web application and 
[bootstrap](https://getbootstrap.com/) for styling. Flask in turn uses [Jinja Templates](Jinja template engine) 
to dynamically build HTML pages using python constructs. SQLite is used as a database.

##### Set up environment    
$ Go to project root (e.g. cd ~/workspace/research/PersonalisedMusicRecommendation)    
$ Activate virtual environment. (e.g. workon iisc)     
$ export FLASK_APP=app     
$ export FLASK_ENV=development     

##### Set up database. 
Open a new tab and go to project root.    
$ cd src/webUI/sqlite/       
$ python init_db.py     

##### Run the application
Open a new tab and go to project root.    
$ cd src/webUI/    
$ flask run     
Open the URL at http://127.0.0.1:5000/    
To hot deploy     
$ flask --debug run      
To run another server    
$ flask run -p 5001      

##### References
1.[Bootstrap framework for html/CSS/Java Script](https://getbootstrap.com/)     
2.[Flask tutorial](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)   
3.[Sqlite Database](https://www.sqlite.org/)