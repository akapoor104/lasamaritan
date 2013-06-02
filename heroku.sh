mkdir heroku
cd heroku/
virtualenv --no-site-packages env
source env/bin/activate
pip install bottle gevent
pip freeze > requirements.txt


chmod a+x lasamaritan.py
chmod a+x sessionDAO.py
chmod a+x userDAO.py

echo 'web: lasamaritan.py' > Procfile
echo 'web: sessionDAO.py' > Procfile
echo 'web: userDAO.py' > Procfile
echo 'env/' > .gitignore

git init
git add .
git commit -m "Initial commit"

heroku create
git push heroku master














