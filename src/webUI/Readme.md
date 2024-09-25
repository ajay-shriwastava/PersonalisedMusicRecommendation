### Deploy Flask Application
##### Set up environment     
$ export FLASK_APP=app     
$ export FLASK_ENV=development     

##### Set up database.    
$ cd sqlite/    
$ python init_db.py    

##### Run the application
$ flask run    
Open the URL at http://127.0.0.1:5000/    
To hot deploy $ flask --debug run     
To run another server $ flask run -p 5001     




### References
1.[Bootstrap framework for html/CSS/Java Script](https://getbootstrap.com/)     
2.[Flask tutorial](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)     