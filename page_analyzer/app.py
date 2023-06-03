import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, url_for, flash
from page_analyzer.services.models import db_connect, DBUrlsModel
from validators import url as validate_url
from urllib.parse import urlparse

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    db_conn = db_connect(DATABASE_URL)
    repo_urls = DBUrlsModel(db_conn)
    urls = repo_urls.get_urls_list()
    db_conn.close()
    return render_template('urls_index.html', urls=urls)


@app.route('/urls/<id>')
def get_url(id):
    db_conn = db_connect(DATABASE_URL)
    repo_urls = DBUrlsModel(db_conn)
    url = repo_urls.get_url(id)
    db_conn.close()
    if not url:
        return render_template("404.html"), 404
    return render_template('show_url.html', url=url)


@app.post("/urls")
def urls_post():
    url = request.form.get('url')

    if validate_url(url):
        parsed_url = "https://" + urlparse(url).hostname

        db_conn = db_connect(DATABASE_URL)
        repo_urls = DBUrlsModel(db_conn)
        url_id = repo_urls.find_url(parsed_url)
        if url_id:
            message = ('Страница уже существует', 'info')
        else:
            url_id = repo_urls.save_and_get_id(parsed_url)
            message = ('Страница успешно добавлена', 'success')
        db_conn.close()
        flash(*message)
        return redirect(url_for('get_url', id=url_id), code=302)

    flash('Некорректный URL', 'danger')
    return render_template('index.html', uncorrect_url=url)


if __name__ == '__main__':
    app.run
