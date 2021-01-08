import pandas as pd


def getStockCode(company):
    stock_code = pd.read_html(
        "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download", header=0)[0]
    stock_code = stock_code[['회사명', '종목코드']]
    stock_code = stock_code.rename(
        columns={'회사명': 'company', '종목코드': 'code'})
    stock_code.code = stock_code.code.map('{:06d}'.format)

    code = stock_code[stock_code.company == company].code.values[0]

    return code


def stockDataframe(company):
    stockCode = getStockCode(company)
    page = 1

    url = f'https://finance.naver.com/item/sise_day.nhn?code={stockCode}'
    url = f'{url}&page={page}'

    df = pd.read_html(url, header=0)[0]
    df = df.dropna()

    df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',
                            '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    # df['date'] = pd.to_datetime(df['date'])
    # date = df['date'][1]
    # price = df['close'][1]
    return df


def stockChart(company):
    stockCode = getStockCode(company)

    url = f'https://ssl.pstatic.net/imgfinance/chart/item/area/day/{stockCode}.png'

    return url
