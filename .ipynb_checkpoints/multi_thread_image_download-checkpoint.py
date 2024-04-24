from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import threading
import pandas as pd
from urllib.request import urlretrieve
from time import perf_counter
from pathlib import Path
batch_df = pd.read_csv(r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\batchid.csv")
batch = batch_df['docid'].to_list()

start = perf_counter()
count = 0

path = Path(r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\GTQ_images_ocrs\fannie_mae")
path.mkdir(exist_ok=True,parents=True)

def download_images(batchid):
    # path = Path(r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\\5percent_validation_images\pa_set1")
    zip_path = fr"{path}\{batchid}"
    k = urlretrieve(rf"https://clvisiontowerb.kfusw1prd.solutions.corelogic.com//download.php?path=ServerFiles/Pagesanddata/{batchid}/&zip={batchid}.zip&cond=Postprocessing&auto=Off", f"{zip_path}.zip")
    # k = urlretrieve(rf"https://dev-ctt-googlevision-clvisiontowerb.kfusw1dev.solutions.corelogic.com/download.php?path=ServerFiles/Pagesanddata/{batchid}/&zip={batchid}.zip&cond=Postprocessing&auto=Off", f"{zip_path}.zip")
    print(k)
    # count +=1  
    # return k
    
    
def poolingDemo(batch):
    with ThreadPoolExecutor(max_workers=200) as executor:
        executor.map(download_images,batch,timeout=300)
        
        # for r in res:
        #     print(r)

poolingDemo(batch)

end = perf_counter()
print(f"total time = {end-start}")
#total time = 7679.155287900001