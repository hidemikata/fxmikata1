from Controller.RestApi import RestApi

urls = {
    '/test':RestApi.test,
    '/':RestApi.root,
    '/get_candle_data':RestApi.getCandleData,

}

