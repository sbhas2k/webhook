from flask import Flask, render_template, jsonify, request
from database import load_scripts_from_db, load_script_from_db, application_submit, webhook_submit
# from sqlalchemy import text
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
  SCRIPTS = load_scripts_from_db()
  return render_template(
    'home.html',
    scripts=SCRIPTS,
  )


@app.route("/api/scripts")
def list_scripts():
  SCRIPTS = load_scripts_from_db()
  return jsonify(SCRIPTS)


@app.route("/api/script/<id>")
def show_script(id):
  script = load_script_from_db(id)
  return jsonify(script)
  # return render_template('script.html', script=script)


@app.route("/script/<id>")
def show_script_id(id):
  script = load_script_from_db(id)
  if not script:
    return "Not Found", 404
  return render_template('script.html', script=script)


@app.route("/script/<id>/apply", methods=['post'])
def submit_script(id):
  # data = request.args
  data = request.form
  application_submit(id, data)
  # return jsonify(data)
  return render_template('application-submit.html', application=data)
  # return "Not Found - " + id, 404


@app.route("/webhook", methods=['post'])
def submit_webhook():
  # data = request.args
  # data = request.form
  data = request.data.decode('utf8')
  webhook_submit(data)
  # return jsonify(data)
  return render_template('application-submit1.html', application=data)
  # return "Not Found - " + id, 404


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
