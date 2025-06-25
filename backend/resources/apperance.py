# from flask_restful import Resource, reqparse
# from models import Appearance, db

# class AppearanceResource(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('rating', required =False)
#     parser.add_argument('episode_id', required=False)
#     parser.add_argument('guest_id', required=False)
    
#     def post(self):
#         data = self.parser.parse_args()
#         appearances = Appearance(**data)

#         db.session.add(appearances)
#         db.session.commit()
#         return {"message": "Appearance created successfully"}, 201

from flask_restful import Resource, reqparse
from models import Appearance, Guest, Episode, db

class AppearanceResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=int, required=True, help="Rating is required and must be an integer")
    parser.add_argument('episode_id', type=int, required=True, help="Episode ID is required and must be an integer")
    parser.add_argument('guest_id', type=int, required=True, help="Guest ID is required and must be an integer")

    def post(self):
        data = self.parser.parse_args()

        
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])

        if not episode or not guest:
            return {"errors": ["Episode or Guest not found"]}, 404

        # Create appearance using back-references
        appearance = Appearance(
            rating=data['rating'],
            episode=episode,
            guest=guest
        )

        try:
            db.session.add(appearance)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"errors": ["Validation errors"]}, 400

        return {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": guest.id,
            "episode_id": episode.id,
            "episode": {
                "id": episode.id,
                "number": episode.number,
                "date": str(episode.date),
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }, 201
