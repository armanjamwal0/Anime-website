#---------------------------------------------------------------------------------------------------
#_----------------------------------- Flask_Migartion______________________________________________
# i use Flask_Migration library -> for it change schema  without lose database data like that when you change 
# your models (like adding row or removing collumns) it update without lose your data 

#2>#Version Control for Database

  #It keeps a history of database changes, so you can rollback or upgrade easily.

#Works Well With Cloud Deployment

#When deploying on Render, AWS, Heroku, or other cloud services, migrations help apply
# database updates automatically.


# and if you want to search more about migartion folder then you can search on google 


#You can create migartion folder 

#command 
#1> flask db init
#2> Generate Migrations
#Whenever you modify your database models (e.g., adding a new column), run:

#use this command 2.5> flask db migrate -m "Added a new column to User"


#Apply Migrations
#After generating migrations, apply them to the database:

#flask db upgrade

#if you want to go back then use this command

#Rolling Back Changes (If Needed)
#If you make a mistake and need to undo the last migration:

#use this com > flask db downgrade


#Deploying with Flask-Migrate
#If you're deploying your app (e.g., on Render, Heroku, etc.), after pulling the latest code, run:

#flask db upgrade  # Ensures the database is updated on the server

#------------------------------------------------------------------------------------