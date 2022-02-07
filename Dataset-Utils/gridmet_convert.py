#                             WildSat
#         This script will convert the netcdf file to csv file.
#         Only usefull columns for this project will be kept.
#         (latitude , longitude temperature , specific_humidity , radiation)
#         Usage :
#                  python3 gridmet_convert.py <thread>

import netCDF4 as nc
import pandas as pd
import os
import concurrent.futures
import argparse

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
filenames=os.listdir(os.path.join(ROOT_PATH,"NetCDF"))
filenames=list(filter(lambda x: x.endswith(".nc"),filenames))

if(not os.path.exists(os.path.join(ROOT_PATH,"CSV_DATA"))):
    os.mkdir(os.path.join(ROOT_PATH,"CSV_DATA"))
    

OUTPUT_PATHS=[os.path.join(ROOT_PATH,"CSV_DATA",filename.split(".")[0][-8:]+".csv") for filename in filenames]
INPUT_PATHS=[os.path.join(ROOT_PATH,"NetCDF",filename) for filename in filenames]

def read_convert2csv(out,inp):
    ds = nc.Dataset(inp)

    output_dict={"lon":[],"lat":[],"max_temp":[],"specific_humidity":[],"radiation":[]}

    max_temperatures=ds["maximum_air_temperature"][:]
    lon=ds["lon"][:]
    lat=ds["lat"][:]
    humidity=ds["specific_humidity"][:]
    radiation=ds["surface_downwelling_shortwave_flux_in_air"][:]

    for x in range(len(max_temperatures)):
        for y in range(len(max_temperatures[x])):
            if(str(max_temperatures[x][y])!="--"):
                output_dict["lon"].append(str(lon[y]))
                output_dict["lat"].append(str(lat[x]))
                output_dict["max_temp"].append(str(max_temperatures[x][y]))
                output_dict["specific_humidity"].append(str(humidity[x][y]))
                output_dict["radiation"].append(str(radiation[x][y]))

    df=pd.DataFrame(output_dict)
    df.to_csv(out)
    print("* DONE -> "+out)

def run(threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for input,output in zip(INPUT_PATHS,OUTPUT_PATHS):
            futures.append(executor.submit(read_convert2csv, inp=input,out=output))

        for future in concurrent.futures.as_completed(futures):
             future.result()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Convert NetCDF to CSV')
    parser.add_argument('thread', type=int, help='Number of Threads')
    args = parser.parse_args()
    run(args.thread)
