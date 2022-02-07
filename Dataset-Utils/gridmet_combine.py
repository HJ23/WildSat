#
#
#                                WildSat 
#       This script will combine all the converted gridmet files previously downloaded.
#       It will also create a new file with the combined data.
#       Output will be saved as output.csv in the same directory as the script.
#       
#       *** Instead of using whole dataset which is pretty big, we will use a 
#                random sample of 1000 points for each file. ***
#       
#

import os
import random
import pandas as pd

ROOT_PATH=os.path.dirname(os.path.realpath(__file__))
CSV_PATH=os.path.join(ROOT_PATH,"CSV_DATA")
OUTPUT=os.path.join(ROOT_PATH,"..","output.csv")


def combine_graidmet():
    csv_filenames=os.listdir(CSV_PATH)
    csv_filenames=list(filter(lambda x: x.endswith(".csv"),csv_filenames))
        
    out_dict={"date":[],"lon":[],"lat":[],"max_temp":[],"radiation":[],"specific_humidity":[]}
    for i,csv in enumerate(csv_filenames):
        date=csv.split(".")[0]
        df=pd.read_csv(os.path.join(CSV_PATH,csv))
        unique=set()
        for _ in range(1000):
            num=random.randint(0,len(df["lon"])-1)
            while(num in unique):
                num=random.randint(0,len(df["lon"]))
            unique.add(num)
        
            out_dict["date"].append(date)
            out_dict["lon"].append(df["lon"][num])
            out_dict["lat"].append(df["lat"][num])
            out_dict["max_temp"].append(df["max_temp"][num])
            out_dict["radiation"].append(df["radiation"][num])
            out_dict["specific_humidity"].append(df["specific_humidity"][num])
        
        # Save each 100*1000 lines  of data batch in a file.
        if((i+1)%100==0):
            out_df=pd.DataFrame(out_dict)

            if(os.path.isfile(OUTPUT)):
                out_df.to_csv(OUTPUT,mode="a",header=False)
            else:
                out_df.to_csv(OUTPUT)
            out_dict={"date":[],"lon":[],"lat":[],"max_temp":[],"radiation":[],"specific_humidity":[]}
            print(f"Batch saved : {str(i)}")

#   save rest of the data
    if((i+1)%100!=0):
        out_df=pd.DataFrame(out_dict)
        out_df.to_csv(OUTPUT,mode="a",header=False)


if __name__=="__main__":
    combine_graidmet()