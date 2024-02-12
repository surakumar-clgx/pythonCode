#path="//10.212.30.30/Share Folder/yokesh/New folder (2)/argentina-prd.json"
from multiprocessing import Process,Queue,current_process,Pipe
import queue
key_path=r"\\filer-argentina-dev\Argentina\Shared Folder\Santosh\Data_Extraction\Bucket\prd.json"
import os,json
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=key_path
bucketName = "clgx-xt-prd-cv-gcs01"
bucketName="clgx-xt-prd-cv-gcs01-820c"
from google.cloud import storage
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucketName)
def download_ocr(tasks_to_do,tasks_completed,ocr_path):
  while True:
    try:
      #tasks_to_do.put('1234')
      i=tasks_to_do.get_nowait()
      print(i,current_process().name)
      i=str(i)
      
    except queue.Empty as e:
      print("emptys",str(e),tasks_to_do.qsize())
      if tasks_to_do.qsize()==0:
        print("Break",current_process().name)
        break
    else:
      try:
        i_path = 'ServerFiles/Pagesanddata/'+i+'/'
        files = bucket.list_blobs(prefix=i_path)
        for file in files:
            blob = bucket.blob(file.name)
            if 'OCR' in file.name:                                                                         
                blob.download_to_filename(ocr_path+"/"+i+'_OCR.txt')
                #print("ocr",i)
            elif 'output_data' in file.name:
                blob.download_to_filename(ocr_path+"/"+i+'_output.json')
                #print("output_data",i)
            del blob
        tasks_completed.put(i)
      except Exception as e:
        print("error",str(e))
if __name__ == "__main__":
  key_path=r"\\filer-argentina-dev\Argentina\Shared Folder\Santosh\Data_Extraction\Bucket\prd.json"
  import os,json
  os.environ['GOOGLE_APPLICATION_CREDENTIALS']=key_path
  bucketName = "clgx-xt-prd-cv-gcs01"
  bucketName="clgx-xt-prd-cv-gcs01-820c"
  from google.cloud import storage
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucketName)
  #os.mkdir("PASFA.ZYINT.CU31455.LEGALPACKS.LOANCARE.D230122.T055011-6")
  def list_files(bucketFolder):
      files = bucket.list_blobs(prefix=bucketFolder)
      fileList = [file.name for file in files if '.' in file.name]
      return fileList

  #print(list_files("Legal/tax_Documents/PASFA.ZYINT.CU31455.LEGALPACKS.LOANCARE.D230122.T055011-5"))
  def download_file(filename):
      print(filename)
      blob = bucket.blob(filename)
      fileName = blob.name.split('/')[-1]
      blob.download_to_filename(""+fileName)
      return "downloaded"
  def download_file2(filename):
      print(filename)
      blob = bucket.blob(filename)
      fileName = blob.name.split('/')[-1]
      blob.download_to_filename(""+fileName)
      return "downloaded"

  folder=""
  # os.mkdir(r"\\10.212.30.30\Share Folder\yokesh\spacy\TX_TEST_OCR")
  ocr_path=r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\Data_Extraction_Sept" #destination path for ocr
  os.mkdir(ocr_path)
  batch=[]
  import pandas as pd
  batch_df=pd.read_csv(r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\KY_set1.1_4159.csv") #path here#

  batch=batch_df['Batch'].to_list()#[:20000]
  print(len(batch))
  from tqdm import tqdm

  tasks_to_do=Queue()
  tasks_completed=Queue()
  for id in tqdm(batch):
    tasks_to_do.put(id)
  print(tasks_to_do.qsize())

  process=[]
  for i in range(16):
    p=Process(target=download_ocr,args=(tasks_to_do,tasks_completed,ocr_path))
    p.start()
    print(p.pid,"started")
    process.append(p)
  print("----------"*10)
  for p in process:
    p.join(300)
    if p.is_alive():
      p.terminate()
      print(f"{i} - terminated")
    print(p.pid,"done")
    print("----"*10)
  import os
  print(tasks_completed.qsize(),tasks_to_do.qsize())
  print(len(os.listdir(ocr_path)))

  print("downloading completed. Now Merge")



# =======================



# path=r"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_Sept"
# import os
# from tqdm import tqdm
# datas=os.listdir(path)
# print(len(datas))
# batches=set()
# for i in tqdm(datas):
# #     ocr_lis.append("/".join([path,i,list(filter(lambda x:"_OCR" in x,os.listdir(path+"/"+i)))[0]]))
# #     json_lis.append("/".join([path,i,"output_data.json"]))
#     batches.add(i.replace("_OCR.txt","").replace("_output.json",""))
# batches=list(batches)

# import json
# path2=path
# lis=[]
# import os
# d=os.listdir(path)
# print(len(batches))
# for i in tqdm(batches):
#     if i+"_OCR.txt" in d and i+"_output.json" in d:
#         lis.append(i+"_output.json")
# test_dict={"data":[]}
# tests=[test_dict["data"].append(open(path+"\\"+i.replace("_output.json","_OCR.txt"),encoding="utf-8").read()) for i in tqdm(lis)]
# json.dump(test_dict,open(r"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_Sept_Output"+"/Sept_PA_train_ocr.json","w"))

# #ids=['25','18','65','94','7','10','13','23','61','62']
# lis2=[]
# lis2=[i.replace("_OCR.txt","_output.json") for i in lis]
# ids=['5', '92', '93', '504', '6']
# #ids=['10','11']
# final={"data":[]}

# for j in tqdm(lis2):    
#     #text_data=open(path2+"/"+j+"_OCR.txt",encoding="utf-8").read().upper().replace("\n"," ")
#     print(path+"/"+j)
#     data=json.loads(open(path+"/"+j).read())
#     #train_data=list(filter(lambda x:x['id'] in ids,data["data"]))
#     train_data=list(data["data"])
#     training_dict={}
#     #print(train_data[0])
#     #training_dict["text"]=text_data
#     training_annotations={}
# #     for i in train_data:
        
# #         training_annotations[i['id']]=i['value']
#     [training_annotations.__setitem__(i['id'],i['value']) for i in tqdm(train_data)]
#     training_dict["annotations"]=training_annotations
#     final["data"].append(training_annotations)
    
# json.dump(final,open(r"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\PA\Data_Extraction_Sept_Output"+"/Sept_PA_train_output.json","w"))
# print("Completed Merger")