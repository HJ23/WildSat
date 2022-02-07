import pandas as pd
import os

PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'EPA_Dataset',"epa_co_daily_summary.csv")
OUT_PATH=os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","epa_co_clean.csv")

csv=pd.read_csv(PATH)

df=csv[["arithmetic_mean","latitude","longitude","date_local","sample_duration"]]

df=df.loc[df["sample_duration"]=="8-HR RUN AVG END HOUR"]

df=df.drop(["sample_duration"],axis=1)

df=df.loc[df["arithmetic_mean"]>0]

df['date'] = pd.to_datetime(df['date_local'], format='%Y-%m-%d')

df["year"]=df["date"].dt.year
df["month"]=df["date"].dt.month
df["day"]=df["date"].dt.day

df.drop(["date_local","date"],axis=1,inplace=True)

df.to_csv(OUT_PATH,index=False)

