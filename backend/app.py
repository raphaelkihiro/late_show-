from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from models import db
# from resources.hero_powers import HeroPower
# from resources.heroes import HeroesListResource, HeroDetailResource
# from resources.powers import PowersResources
# intialize our app

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///lateshow.db'

api=Api(app)

migrate=Migrate(app, db)

db.init_app(app)

# api.add_resource(HeroesListResource, "/heroes")
# api.add_resource(HeroDetailResource, "/heroes/<int:id>")
# api.add_resource(HeroPower, "/hero_powers")
# api.add_resource(PowersResources, "/powers", "/powers/<int:id>")

if __name__ == '__main__':
    app.run(port=5555)

    
