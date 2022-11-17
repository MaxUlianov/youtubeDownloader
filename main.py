from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from pytube.exceptions import RegexMatchError
import logging
import json

import config
from downloader import get_video_options


app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = config.secret


@app.route('/', methods=['GET', 'POST'])
def ytdl():
    if request.method == "POST":

        link = request.form["link-field"]
        logging.info(f'Link received: {link}')
        logging.info(f'Request form data: {request.form}')

        params = json.dumps(request.form.to_dict())

        options = []
        try:
            options = get_video_options(link)
        except RegexMatchError as e:
            logging.info(f'Error: {error}')
            return redirect(url_for("error", error=e))

        return render_template("page.html", options=options, params=params)

    elif request.method == "GET":
        return render_template("page.html")


@app.route('/error', methods=["GET"])
def error():
    e = request.args.get("error", None)
    return f'Error {e} in video download'


@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        filename = 'swirl-logo-01.png'
        return send_from_directory(directory='static/files', path=filename, as_attachment=True)
    elif request.method == "GET":
        if request.args:
            itag = request.args.get("itag", None)
            params = request.args.get("params", None)

            p = json.loads(params)
            link = p['link-field']
            timestamps = p['timestamp-field']
            return render_template("dl.html", link=link)
        return render_template("dl.html")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
    app.run(host="0.0.0.0")
