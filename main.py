from flask import Flask, request, render_template, redirect, url_for, send_from_directory, after_this_request
from pytube.exceptions import RegexMatchError
import logging
import json

import config
import os
from downloader import get_options, download_controller


app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = config.secret


def check_audio_only(form):
    if 'audio-only' in form and form['audio-only'] == 'on':
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def ytdl():
    if request.method == "POST":

        link = request.form["link-field"]
        logging.info(f'Link received: {link}')
        logging.info(f'Request form data: {request.form}')

        params = json.dumps(request.form.to_dict())

        ao = check_audio_only(request.form)

        try:
            options = get_options(link, ao)
        except RegexMatchError as e:
            logging.info(f'Error: {error}')
            return redirect(url_for("error", error=e))

        return render_template("page.html", options=options, params=params)

    elif request.method == "GET":
        return render_template("page.html")


@app.route('/error', methods=["GET"])
def error():
    e = request.args.get("error", None)
    error_message = f'Error {e} in video download, please, try again'
    return render_template("error_page.html", error_message=error_message)


@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":

        try:
            params = json.loads(request.form['params'])
            link = params['link-field']
            timestamps = params['timestamp-field']
            ao = check_audio_only(params)
            itag = request.args.get('itag', None)

            logging.info(f'Params: link: {link}, timestamps: {timestamps}, itag: {itag}, audio-only: {ao}')

            f = download_controller(link, timestamps, itag=itag, a_only=ao)
            filename = os.path.basename(f)
            logging.info(f'File: {f}')

        except Exception as e:
            logging.info(f'Error: {error}')
            return redirect(url_for("error", error=e))

        @after_this_request
        def delete_file(response):
            try:
                os.remove(f)
            except Exception as e:
                logging.debug(f'File delete error: {repr(e)}')
            return response

        return send_from_directory(directory='static/files', path=filename, as_attachment=True)

    elif request.method == "GET":
        if request.args:
            itag = request.args.get("itag", None)
            params = request.args.get("params", None)

            p = json.loads(params)
            link = p['link-field']
            return render_template("dl.html", link=link, params=params, itag=itag)
        return render_template("dl.html")


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO)
    app.run(host="0.0.0.0")
