from flask_restful import Resource
from models import Episode

class EpisodeResource(Resource):
    def get(self, id=None):
        if id is None:
            episodes = Episode.query.all()
            return [episode.to_dict() for episode in episodes], 200  
        else:
            episode = Episode.query.filter_by(id=id).first()
            if episode:
                return episode.to_dict(), 200
            return {"error": "Guest not found"}, 400