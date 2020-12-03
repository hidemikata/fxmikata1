from Model.pricing import FxDataUsdJpy1M
import json

class RestApi(object):
    @classmethod
    def test(cls):
        return '{\'key2\':\'value2\'}'

    @classmethod
    def root(cls):
        return '{\'key\':\'value\'}'

    @classmethod
    def getCandleData(cls,limit=100):
        filter_time = []
        filter_time.append(FxDataUsdJpy1M.time.like('%-%-% %:%:%'))#time.likeを後で調べる
        data = FxDataUsdJpy1M.get_close_past_date(limit, past_offset=1, filter_time=filter_time)

        ret_data = {}
        high = 0
        low = 9999999
        for index, v in enumerate(data):
            if high < v.high:
                high = v.high
            if low > v.low:
                low = v.low

            time = v.time.strftime('%Y-%m-%d %H:%M:%S')
            d = {time:[v.open, v.high, v.low, v.close]}
            ret_data.update(d)
        ret_data.update({'high': high, 'low':low})
        return json.dumps(ret_data)
