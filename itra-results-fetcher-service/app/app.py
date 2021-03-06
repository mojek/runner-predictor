from flask import Flask, request
from flask_restful import Api, Resource
from .flask_celery import make_celery
from .itra_fetcher import ItraRaceResultsFetcher
from .itra_result_sender import ItraResultSender

flask_app = Flask(__name__)
api = Api(flask_app)
flask_app.config.update(
    CELERY_BROKER_URL="redis://itra_redis_cache:6379",
    CELERY_RESULT_BACKEND="redis://itra_redis_cache:6379",
)

celery = make_celery(flask_app)


class ItraFetcher(Resource):
    def post(self):
        req_json = request.get_json()
        itra_race_id = req_json["itra_race_id"]
        callback_race_id = req_json["callback_race_id"]
        fetch_data_from_itra.delay(itra_race_id, callback_race_id)

        return "Add to que"


api.add_resource(ItraFetcher, "/")

# celery -A your_application.celery worker
# celery -A app.app.celery worker
@celery.task(name="app.app.fetch_data_from_itra")
def fetch_data_from_itra(itra_race_id, callback_race_id):
    fetcher = ItraRaceResultsFetcher(itra_race_id=itra_race_id)
    fetcher.fetch_results()
    sender = ItraResultSender(fetcher.results, callback_race_id)
    sender.send_to_race_service()
    sender.fetch_data_from_enduhub()
    return "done"
