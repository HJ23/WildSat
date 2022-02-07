#                         WildSat
#    This script downloads Gridmet data from the official website.
#    After download it will save it as .nc file.
#    Usage : 
#            python3 gridmet_downloader.py <start_year> <end_year> <thread> 


import argparse
import requests
import datetime
import calendar
import concurrent.futures
import os

URL="https://www.northwestknowledge.net/metdata/data/permanent/{YEAR}/permanent_gridmet_{DATE}.nc"


def downloader(start_date,year):
    try:
        url=URL.format(YEAR=year,DATE=start_date)
        r = requests.get(url, allow_redirects=True)
    except:
        print("Error occured in downloading :"+url)
        return

    dir_path = os.path.dirname(os.path.realpath(__file__))
    PATH=os.path.join(dir_path,"NetCDF")
    
    if(not os.path.exists(PATH)):
        os.mkdir(PATH)

    open(os.path.join(PATH,f'permanent_gridmet_{start_date}.nc'), 'wb').write(r.content)
    print("*Download DONE : "+f'permanent_gridmet_{start_date}.nc')


def run(start_year,end_year,thread):
    dates=[]
    for year in range(start_year,end_year+1):
        DAYS=366 if calendar.isleap(year) else 365
        start_date=str(year)+"01"+"01"
        for _ in range(DAYS):
            dates.append((start_date,year))

            date= datetime.datetime.strptime(start_date, "%Y%m%d")
            date_final=date+ datetime.timedelta(days=1)

            start_date=str(date_final.year)+(str(date_final.month) if(len(str(date_final.month))>1) else "0"
                      +str(date_final.month))+(str(date_final.day) if(len(str(date_final.day))>1) else "0"+str(date_final.day))


    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = []
        for start_date,year in dates:
            futures.append(executor.submit(downloader, start_date=start_date,year=year))

        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Download Gridmet data')
    parser.add_argument('start_year', type=int, help='Start Year')
    parser.add_argument('end_year', type=int, help='End Year')
    parser.add_argument('thread', type=int, help='Number of Threads')
    args = parser.parse_args()
    run(args.start_year,args.end_year,args.thread)
