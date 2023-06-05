import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, url_for, flash
from page_analyzer.services.models import DBUrlsModel, make_urlcheck
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
    repo_urls = DBUrlsModel(DATABASE_URL)
    repo_urls.db_conn()
    urls = repo_urls.get_urls_list()
    repo_urls.db_close

    return render_template('urls_index.html', urls=urls)


@app.route('/urls/<id>')
def get_url(id):
    repo_urls = DBUrlsModel(DATABASE_URL)
    repo_urls.db_conn()
    url = repo_urls.get_url(id)
    checks_list = repo_urls.get_url_checks(id)
    repo_urls.db_close()
    if not url:
        return render_template("404.html"), 404
    return render_template('show_url.html', url=url, checks_list=checks_list)


@app.post("/urls")
def urls_post():
    url = request.form.get('url')

    if validate_url(url):
        parsed_url = f"https://{urlparse(url).hostname}"

        repo_urls = DBUrlsModel(DATABASE_URL)
        repo_urls.db_conn()
        url_id = repo_urls.find_url(parsed_url)
        if url_id:
            message = ('Страница уже существует', 'info')
        else:
            url_id = repo_urls.add_url(parsed_url)
            message = ('Страница успешно добавлена', 'success')
        repo_urls.db_close()
        flash(*message)
        return redirect(url_for('get_url', id=url_id), code=302)

    flash('Некорректный URL', 'danger')
    return render_template('index.html', uncorrect_url=url)


@app.post('/urls/<id>/checks')
def check_url(id):
    repo_urls = DBUrlsModel(DATABASE_URL)
    repo_urls.db_conn()
    url = repo_urls.get_url(id)
    url_check = make_urlcheck(url['id'], url['name'])
    current_check = repo_urls.add_check(url_check)
    repo_urls.db_close()

    if current_check:
        message = ('Страница успешно проверена', 'success')
    else:
        message = ('Произошла ошибка при проверке', 'danger')
    flash(*message)
    return redirect(url_for('get_url', id=url['id']))


if __name__ == '__main__':
    app.run
