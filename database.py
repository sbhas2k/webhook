from sqlalchemy import create_engine, text
import os
import logging
import json

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


def application_submit(id, data):
  # NSERT INTO `webapp1`.`stock_update` (`id`, `updated_price`) VALUES ('10', '200');
  logging.info(f'id - {id} / price = { data["updated_price"] }')
  with engine.connect() as con:
    query = text("INSERT INTO stock_update (updated_price) VALUES ( :sprice)")
    con.execute(query, {"sprice": data['updated_price']})
    # con.execute(
    # text('INSERT INTO stock_update (id, updated_price) VALUES (6, 200)'))


def webhook_submit(data):
  # data1 = json.loads(data)['stocks']
  with engine.connect() as con:
    query = text("INSERT INTO charink_post_req (request) VALUES ( :req)")
    con.execute(query, {"req": data})
