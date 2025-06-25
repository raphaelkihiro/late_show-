from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from models import db
from resources.episode import EpisodeResource
from resources.guests import GuestResource
from resources.apperance import AppearanceResource
# intialize our app

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///lateshow.db'

api=Api(app)

migrate=Migrate(app, db)

db.init_app(app)

api.add_resource(AppearanceResource, "/appearances")
api.add_resource(EpisodeResource, "/episodes/episodes/<int:id>")
api.add_resource(GuestResource, "/guests")


if __name__ == '__main__':
    app.run(port=5555)

    
