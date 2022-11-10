from flask import Flask, request, render_template
from pytube.exceptions import RegexMatchError

from downloader import get_video_options


app = Flask(__name__, static_folder="static", static_url_path="")


@app.route('/', methods=['GET', 'POST'])
def ytdl():
    if request.method == "POST":
        link = request.form["link-field"]
        print(link)
        print(request.form)

        options = []
        try:
            options = get_video_options(link)
        except RegexMatchError as e:
            error(repr(e))
            options = [repr(e)]
        return render_template("page.html", options=options)

    elif request.method == "GET":
        return render_template("page.html")
    return


@app.route('/error', methods=["GET"])
def error(e):
    return f'Error {e} in video download'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
