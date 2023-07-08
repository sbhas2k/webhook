from flask import Flask, render_template, jsonify
from database import load_scripts_from_db
# from sqlalchemy import text

app = Flask(__name__)

# SCRIPTS = [{
#   'id': 1,
#   'symbol': 'INFY',
#   'traded_price': '111.11',
#   'ltp': '111.11'
# }, {
#   'id': 2,
#   'symbol': 'TCS',
#   'traded_price': '1011.11',
#   'ltp': '1101.11'
# }, {
#   'id': 3,
#   'symbol': 'HCL',
#   'traded_price': '2123.11',
#   'ltp': '2123'
# }]


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


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
