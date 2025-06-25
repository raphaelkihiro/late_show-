from flask_restful import Resource
from models import Guest

class GuestResource(Resource):
    def get(self, id=None):
        if id is None:
            guests = Guest.query.all()
            return [guest.to_dict() for guest in guests], 200  
        else:
            return {"error": "Guest not found"}, 400