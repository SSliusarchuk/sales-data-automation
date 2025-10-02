from datetime import datetime, timedelta
import pandas as pd
from random import randint

companies=["kaka","dupa", "sraka","gowno"]
today=datetime.today()
yesterday=today -timedelta(days=1)

if 1 <= today.weekday()<=5:
    d={
        "dt":[yesterday.strftime("%m/%d/%Y")]*len(companies)*2,
        "company": companies*2,
        "trans_type":["buy"]*len(companies)+["sell"]*len(companies),
        "amount":[randint(0,1000) for _ in range(len(companies)*2)]
    }
    df=pd.DataFrame(d)
    df.to_csv("sales-data.csv", index=False)