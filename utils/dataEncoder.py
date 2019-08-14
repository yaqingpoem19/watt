import json
import datetime
import decimal


class DataEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return super(DataEncoder, self).default(obj)

