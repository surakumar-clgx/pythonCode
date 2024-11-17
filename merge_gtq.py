# month = "oct"
# p = "\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_aug"
# path=rf"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_{month}"
# path = rf"\\filer-argentina-dev\Argentina\Shared Folder\Prateekesh\KY\Data_Extraction_{month}"
# month = "dec"
# path = rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\KY_data\{month}\b1"
state = "mgt_set4"
path = rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\{state}"
import os
from tqdm import tqdm

datas = os.listdir(path)
print(len(datas))
batches = set()
for i in tqdm(datas):
    #     ocr_lis.append("/".join([path,i,list(filter(lambda x:"_OCR" in x,os.listdir(path+"/"+i)))[0]]))
    #     json_lis.append("/".join([path,i,"output_data.json"]))
    batches.add(i.replace("_OCR.txt", "").replace("_output.json", ""))
batches = list(batches)

import json

path2 = path
lis = []
import os

d = os.listdir(path)
print(len(batches))
for i in tqdm(batches):
    if i + "_OCR.txt" in d and i + "_output.json" in d:
        lis.append(i + "_output.json")

from pathlib import Path

ocr_path = rf"{path}\merged_files"  # combined ocr path
Path(ocr_path).mkdir(exist_ok=True)
test_dict = {"data": []}
try:
    tests = [
        test_dict["data"].append(
            open(
                path + "\\" + i.replace("_output.json", "_OCR.txt"), encoding="utf-8"
            ).read()
        )
        for i in tqdm(lis)
    ]
except Exception as e:
    print(e)
file_name = rf"\{state}_ocr.json"
# # json.dump(test_dict,open(rf"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_{month}_Output\\"+file_name,"w"))
json.dump(test_dict, open(ocr_path + file_name, "w"))

# import sys
# sys.exit(1)

lis2 = []
lis2 = [i.replace("_OCR.txt", "_output.json") for i in lis]

ids = "34,44,99,".split(",")
final = {"data": []}

for j in tqdm(lis2):
    # text_data=open(path2+"/"+j+"_OCR.txt",encoding="utf-8").read().upper().replace("\n"," ")
    # print(path + "/" + j)
    data = json.loads(open(path + "/" + j).read())
    # train_data=list(filter(lambda x:x['id'] in ids,data["data"]))
    train_data = list(data["data"])
    training_dict = {}
    # print(train_data[0])
    # training_dict["text"]=text_data
    training_annotations = {}
    #     for i in train_data:
    #         training_annotations[i['id']]=i['value']
    [training_annotations.__setitem__(i["id"], i["value"]) for i in train_data]
    training_dict["annotations"] = training_annotations
    final["data"].append(training_annotations)

file_name = rf"\{state}_output.json"
json.dump(final, open(ocr_path + file_name, "w"))
print("Completed Merger")
print(path)
