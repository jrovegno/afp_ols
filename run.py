from matplotlib import pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import Quandl
from datetime import datetime

# Lee token de Quandl
with open('token.txt', 'rU') as f:
    token = f.readline().rstrip()

# Descarga datos Indicadores
today = datetime.now()
usdclp = Quandl.get("CURRFX/USDCLP", authtoken=token)['Rate']
ipsa = web.DataReader('^IPSA', 'yahoo', start=datetime(2003, 1, 10), end=today)['Close']
spy = web.DataReader('SPY', 'yahoo', start=datetime(1993, 1, 29), end=today)['Close']
eem = web.DataReader('EEM', 'yahoo', start=datetime(2003, 4, 15), end=today)['Close']
vea = web.DataReader('VEA', 'yahoo', start=datetime(2007, 7, 26), end=today)['Close']
stoxx = web.DataReader('^STOXX50E', 'yahoo', start=datetime(1993, 1, 1), end=today)['Close']
# Junta Indicadores en un solo DataFrame
data_index = pd.DataFrame()
data_index['ipsa'] = ipsa
data_index['spy'] = spy
data_index['eem'] = eem
data_index['vea'] = vea
data_index['stoxx'] = stoxx
data_index['usdclp'] = usdclp

# Descarga datos Valores Cuota AFP
karg_csv = dict(delimiter=';', decimal=',', index_col=0, parse_dates=True)
afps = ['CUPRUM', 'HABITAT', 'PLANVITAL', 'PROVIDA', 'MODELO']
data = {}
for afp_name in afps:
    filename = 'https://raw.githubusercontent.com/collabmarket/data_afp/master/data/VC-%s.csv'%afp_name
    data[afp_name] = pd.read_csv(filename, **karg_csv)
# Junta Valores cuota en un Panel
data_afp = pd.Panel(data)

# Crea DataFrame de trabajo
df = data_index.copy()
df['CUPRUM_A'] = data_afp.CUPRUM.A
df.dropna(inplace=True)
# Rentabilidad diaria
df_pct = df.pct_change()
