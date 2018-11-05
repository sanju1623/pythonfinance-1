from flask import Flask, render_template,request
import requests
import sys
import time
import datetime
from dateutil.tz import tzlocal
from tzlocal import get_localzone
from yahoofinancials import YahooFinancials




app = Flask(__name__)


@app.route('/')
def input():
    return render_template('input.html')



@app.route('/post',methods=['POST'])
def calculate():
    url = 'http://www.google.com/'
    timeout = 2
    try:
        _ = requests.get(url, timeout=timeout)
        symbol = (request.form['ticketSymbol'])
        try:
            data = YahooFinancials(symbol)
            date = datetime.datetime.now(tzlocal())
            timezone = str(time.asctime(time.localtime(time.time())))
            strftime = date.strftime("%Z")
            financials = data.get_stock_quote_type_data()
            name = str(financials.get(symbol).get('longName'))
            sym = financials.get(symbol).get('symbol')
            current = str(data.get_current_price())
            currentchange = str(round(data.get_current_change(),2))
            percentchange = str(round(data.get_current_percent_change()*100,2))+'%'
            return render_template('output.html', symbol=symbol, data=data, timezone=timezone, strftime=strftime, financials=financials, name=name,
                               sym=sym, current=current, currentchange=currentchange, percentchange=percentchange)
        except:
            return 'INVALID SYMBOL'
    except:
        return 'NO INTERNET CONNECTION'


if __name__ == '__main__':
    app.run()

