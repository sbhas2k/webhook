from sqlalchemy import create_engine, text
import os
import logging
import pandas as pd

import datetime as dt
from pytz import timezone

conn_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(conn_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_scripts_to_db():
  with engine.connect() as con:
    # Also update the updated scripts to MS SQl db
    con.execute(text("truncate table dhan_allowed_scripts"))
    #Prepare panda
    SHEET_ID = '1XR_ukGBSQ7kp3RnmRRxhEFbc8tu9gmDX'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet(0))'
    df = pd.read_csv(url)

    for index, row in df.iterrows():
      query = text(
        "INSERT INTO dhan_allowed_scripts (script_name,ISIN) VALUES (:script,:isin)"
      )
      con.execute(query, {"script": row[' Symbol'], "isin": row['ISIN No']})

  return len(df)


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
  stks = data['stocks'].split(',')
  tri_price = data['trigger_prices'].split(',')
  strategy = data['scan_name']
  date_time = dt.datetime.now(timezone("Asia/Kolkata"))

  with engine.connect() as con:
    con.execute(text("truncate table positions"))
    for i in range(len(stks)):
      query = text(
        "INSERT INTO positions (strategy,script,c_tp,created_on,modified_on) VALUES (:stra,:stk,:tp,:con,:con)"
      )
      con.execute(query, {
        "stra": strategy,
        "stk": stks[i],
        "tp": tri_price[i],
        "con": date_time
      })
