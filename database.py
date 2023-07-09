from sqlalchemy import create_engine, text
import os

conn_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(conn_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_scripts_from_db():
  with engine.connect() as con:
    result = con.execute(
      text(
        "SELECT id,symbol,tp,ltp,pos_status,profit_loss,case when type=1 then (tp-ltp) else (ltp-tp) end as pnl from stock_list"
      ))
  SCRIPTS = []
  for row in result.all():
    SCRIPTS.append(row._asdict())

  return SCRIPTS


def load_script_from_db(id):
  with engine.connect() as con:
    result = con.execute(text("SELECT * from stock_list where id = :val"),
                         {"val": id})

  rows = result.all()
  if len(rows) == 0:
    return None
  else:
    return rows[0]._asdict()
  # SCRIPTS = []
  # for row in result.all():
  #   SCRIPTS.append(row._asdict())

  # return SCRIPTS
