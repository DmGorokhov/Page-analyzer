### Hexlet tests and linter status:
[![Actions Status](https://github.com/DmGorokhov/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/DmGorokhov/python-project-83/actions)
[![Github Actions Status](https://github.com//DmGorokhov/python-project-83/workflows/Python%20CI/badge.svg)](https://github.com//DmGorokhov/python-project-83/actions/pyci.yaml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6540f825b182f6bfaa13/maintainability)](https://codeclimate.com/github/DmGorokhov/python-project-83/maintainability)


### About:
[Page analyzer](https://page-analyze.up.railway.app)
 is the simple SEO analyzer for any website.
Try it and analyze your SEO!


### Requirements:

* python >= 3.10
* flask >= 2.3.2
* gunicorn >= 20.1.0
* python-dotenv >= 1.0.0
* install >= 1.3.5
* psycopg2-binary >= 2.9.6
* validators >= 0.20.0
* requests >= 2.31.0
* beautifulsoup4 >= 4.12.2
* postgres >= 4.0
* Make (is used to run utility through console-command)



### Page analyzer is available on GitHub:

```shell
$ git clone https://github.com/DmGorokhov/python-project-83.git
```

### Basic commands:
When cloning app repository, you may need to install Make for run short console-commands described below.
```
make install   # install poetry for dependency management
```
```
make dev   # starts the app on the local server in the development environment
```
```
make start   # start the app in the production environment
```
```
make db-reset   # allow clean and reset local database
```
