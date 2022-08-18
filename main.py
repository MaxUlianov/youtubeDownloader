from flask import Flask, request, render_template


app = Flask(__name__, static_folder="static", static_url_path="")


@app.route('/', methods=['GET', 'POST'])
def ytdl():
    if request.method == "GET":
        return render_template("page.html")
    return


if __name__ == '__main__':
    app.run(host="0.0.0.0")
