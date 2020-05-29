List of git commands to work with heroku:

Followed off of this tutorial: https://www.youtube.com/watch?v=BPvg9bndP1U

Login to Heroku
---------------------
heroku login


heroku git:remote -a discord-quote-bot-jon

Adds changes that you have made: 
--------------------------------
git add .  

Pushes the changes to heroku with a comment of what's commiting
--------------------------------
git commit -am "Explain what you're committing"

git push heroku master


To view the logs
---------------------------
heroku logs -a discord-quote-bot-jon