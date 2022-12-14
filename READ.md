
1. make virtual
python -m venv virt
source virt/Scripts/activate
pip freeze

2. Install Libraries
pip install Flask Flask-SQLAlchemy Flask-WTF Flask-Migrate Flask-Login SQLAlchemy WTForms Werkzeug

then check cmd: pip freeze

3. Make a sqlalchmey database into computer
 winpty python => create sqlalchmey database

# cmd: from app import db
# cmd:  db.create_all()

4. Migrations database 

# git terminal cmd: flask db init
# git terminal cmd: flask db
# git terminal cmd: flask db migrate -m 'Initial Migration'
# cmd: flask db upgrade

5. update migrations database
# then any time need update data with Migrate
# cmd: flask db migrate -m "commit something added new data"
# cmd: flask db upgrade

5.Run Flask Social Media Project
# git terminal cmd: source virt/Scripts/activate
# git terminal cmd: flask run


