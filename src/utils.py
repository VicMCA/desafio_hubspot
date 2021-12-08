import re
from datetime import datetime, timezone


def check(obj):
  regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  return re.search(regex, obj)


def validate_hs_property(action, data):
  if isinstance(data, list):
    try:
      if action == "create":
        for i in data:
          if "email" in i.values():
            return 1
          else:
            return 0
      else:
        return 1
    except:
      raise Exception("Error with data. List must have only -> {'property': 'email','value': email}")
  else:
    raise Exception("List/Array Only")


def hs_templates(data):
  d = dict()
  d["properties"] = data
  return d


## To customise the starting date, just modify year, month, day
def expiry_timestamp(duration, year=datetime.utcnow().year, month=datetime.utcnow().month, day=datetime.utcnow().day):
  start_dt = datetime(year,month,day)
  day = start_dt.day
  val_month = (start_dt.month + duration) % 12
  if val_month:
    exp_month = val_month
  else:
    exp_month = 12
  year = start_dt.year + (duration // 12)
  expired_at = round(datetime(year, exp_month, day, 00, 00, 00, tzinfo=timezone.utc).timestamp()) * 1000
  d = dict()
  d['expired_at'] = f"{year}-{exp_month}-{day} 00:00:00"
  d['expired_at_tmstp'] = expired_at
  return d