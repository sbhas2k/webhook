from sqlalchemy import create_engine, text
import os

conn_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(conn_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

# with engine.connect() as con:
#   result = con.execute(
#     text(
#       "SELECT id,symbol,tp,ltp,pos_status,profit_loss,(tp-ltp) as pnl from stock_list"
#     ))
#   result_dict = []
#   for row in result.all():
#     result_dict.append(row._asdict())

#   print(result_dict)
#   print(type(result_dict))


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
