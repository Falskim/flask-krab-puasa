from flask import Flask, send_file
from datetime import datetime
import image_generation as ImageGeneration
import pytz

app = Flask(__name__)

TZ = pytz.timezone("Asia/Jakarta")

START_DATE = datetime(2021, 4, 12, tzinfo=TZ)


@app.route("/", methods=["GET"])
def index():
    day = (datetime.now(tz=TZ) - START_DATE).days
    return get_image_response(day)


@app.route("/<day>", methods=["GET"])
def custom(day):
    return get_image_response(day)


def get_image_response(day):
    filepath = ImageGeneration.create_new_image(day)
    return send_file(filepath, mimetype="image/jpg")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = 0
    return r
