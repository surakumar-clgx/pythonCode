




month = "sept"
# p = "\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_aug"
# path=rf"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_{month}"
path = rf"\\filer-argentina-dev\Argentina\Shared Folder\Prateekesh\KY\Data_Extraction_{month}"
import os
from tqdm import tqdm
datas=os.listdir(path)
print(len(datas))
batches=set()
for i in tqdm(datas):
#     ocr_lis.append("/".join([path,i,list(filter(lambda x:"_OCR" in x,os.listdir(path+"/"+i)))[0]]))
#     json_lis.append("/".join([path,i,"output_data.json"]))
    batches.add(i.replace("_OCR.txt","").replace("_output.json",""))
batches=list(batches)

import json
path2=path
lis=[]
import os
d=os.listdir(path)
print(len(batches))
for i in tqdm(batches):
    if i+"_OCR.txt" in d and i+"_output.json" in d:
        lis.append(i+"_output.json")

from pathlib import Path
Path(rf"\\filer-argentina-dev\Argentina\Shared Folder\Prateekesh\KY\Data_Extraction_{month}_Output").mkdir(exist_ok=True)
test_dict={"data":[]}
tests=[test_dict["data"].append(open(path+"\\"+i.replace("_output.json","_OCR.txt"),encoding="utf-8").read()) for i in tqdm(lis)]
file_name = f"/{month}_KY_train_ocr.json"
# # json.dump(test_dict,open(rf"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_{month}_Output\\"+file_name,"w"))
json.dump(test_dict,open(rf"\\filer-argentina-dev\Argentina\Shared Folder\Prateekesh\KY\Data_Extraction_{month}_Output\\"+file_name,"w"))

# import sys
# sys.exit(1)

#ids=['25','18','65','94','7','10','13','23','61','62']
lis2=[]
lis2=[i.replace("_OCR.txt","_output.json") for i in lis]
# ids=['5', '92', '93', '504', '6']
ids=['5', '92', '93', '6']
#ids=['10','11']
final={"data":[]}

for j in tqdm(lis2):    
    #text_data=open(path2+"/"+j+"_OCR.txt",encoding="utf-8").read().upper().replace("\n"," ")
    print(path+"/"+j)
    data=json.loads(open(path+"/"+j).read())
    #train_data=list(filter(lambda x:x['id'] in ids,data["data"]))
    train_data=list(data["data"])
    training_dict={}
    #print(train_data[0])
    #training_dict["text"]=text_data
    training_annotations={}
#     for i in train_data:
#         training_annotations[i['id']]=i['value']
    [training_annotations.__setitem__(i['id'],i['value']) for i in tqdm(train_data)]
    training_dict["annotations"]=training_annotations
    final["data"].append(training_annotations)

file_name = f"/{month}_KY_train_output.json"    
json.dump(final,open(rf"\\filer-argentina-dev\Argentina\Shared Folder\Prateekesh\KY\Data_Extraction_{month}_Output\\"+file_name,"w"))
print("Completed Merger")