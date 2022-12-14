# Getting Started with Create Flask

Get started With Flask Social Media project
#socialmedia #flask #flasksocialmedia


Overview
Flask-Social-Media is a Social Media Platforms aimed towards sharing Post or content through Flask Media. Flask-Social-Media provides the user with complete control of their posts such as creation, editing, deletion, like,  as well as saving favourite comments for later reference. 




1. make virtual
python -m venv virt
source virt/Scripts/activate
pip freeze

2. Install Libraries
pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Migrate Flask-Login SQLAlchemy WTForms Werkzeug

then check cmd: pip freeze

3. Make a sqlalchmey database into computer
 winpty python => create sqlalchmey database

 cmd: from app import db
 cmd:  db.create_all()

4. Migrations database 

 git terminal cmd: flask db init
 git terminal cmd: flask db
 git terminal cmd: flask db migrate -m 'Initial Migration'
 cmd: flask db upgrade

5. update migrations database
 then any time need update data with Migrate
 cmd: flask db migrate -m "commit something added new data"
 cmd: flask db upgrade

5.Run Flask Social Media Project
 git terminal cmd: source virt/Scripts/activate
 git terminal cmd: flask run

<h3>Home Page</h3>

![Home_Page_Flask_Social_Screenshot_1](https://user-images.githubusercontent.com/51543360/207629407-1eb404ed-90bf-4f4f-8aa0-94681f2427f7.png)

<h3>Profile Page</h3>

![Profile_Page_Flask_Social_Screenshot_2](https://user-images.githubusercontent.com/51543360/207629607-d1898e8b-ac5e-4d1e-aff7-25abd28041fb.png)

<h3>Like Page</h3>

![Like_Page_Flask_Social_Screenshot_2](https://user-images.githubusercontent.com/51543360/207629720-fd2eb2a8-9a9f-4e0e-b577-8d17ccd8d3f5.png)


<h3>Login Page</h3>

![Login_Page_Flask_Social_Screenshot_2](https://user-images.githubusercontent.com/51543360/207629809-f2c66654-7496-499f-b831-f386971288ee.png)

<h3>Signup Page</h3>

![Signup_Page_Flask_Social_Screenshot_2](https://user-images.githubusercontent.com/51543360/207629878-7f46c845-2187-42e0-8ac0-c4b97a7544f2.png)
