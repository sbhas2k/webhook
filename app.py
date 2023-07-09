from flask import Flask, render_template, jsonify
from database import load_scripts_from_db, load_script_from_db
# from sqlalchemy import text

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


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
