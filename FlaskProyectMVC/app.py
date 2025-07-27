from flask import Flask, session
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_request
    def make_session_non_permanent():
        session.permanent = False

    mysql.init_app(app)
    from controllers.albumController import albumsBP
    from controllers.databaseController import databaseBP
    app.register_blueprint(albumsBP)
    app.register_blueprint(databaseBP)
    return app

if __name__ == "__main__":
    app = createApp()
    app.run(port=3000, debug=True)