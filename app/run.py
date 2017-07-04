#!flask/bin/python
from app import app
from app.Model.database import Db
if __name__ == '__main__':
    db = Db()
    # session = db.createSession()
    app.run(debug=True)
    db.shutdown()
