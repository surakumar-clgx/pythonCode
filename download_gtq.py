# path="//10.212.30.30/Share Folder/yokesh/New folder (2)/argentina-prd.json"
from multiprocessing import Process, Queue, current_process
import queue
from google.cloud import storage
import os
import json

# key_path = r"\\filer-argentina-dev\Argentina\Shared Folder\yokesh\Bucket\prd.json"

# key_path = r"\\filer-argentina-dev\Argentina\Shared Folder\Suraj\Bucket\prd.json"

# key_path = "//filer-argentina-dev/Argentina/Shared Folder/Manikanda Gokul/ext report manual/prd.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
# bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"
# bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"


# key_path = "//filer-argentina-dev/Argentina/Shared Folder/Suraj/Bucket/prd1.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
# bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"
# bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"

key_path = r"//filer-argentina-dev/Argentina/Shared Folder/Suraj/Bucket/uat1.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
bucketName = "clgx-xt-uat-cv-gcs01-9247"
bucketName = "clgx-xt-uat-cv-gcs01-9247"

# key_path = r"//filer-argentina-dev/Argentina/Shared Folder/Suraj/Bucket/dev1.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
# bucketName = "clgx-clvision-dev-buck1_test"
# bucketName = "clgx-clvision-dev-buck1_test"

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucketName)


def download_ocr(tasks_to_do, tasks_completed, ocr_path):
    while True:
        try:
            # tasks_to_do.put('1234')
            i = tasks_to_do.get_nowait()
            print(i, current_process().name)
            i = str(i)

        except queue.Empty as e:
            print("emptys", str(e), tasks_to_do.qsize())
            if tasks_to_do.qsize() == 0:
                print("Break", current_process().name)
                break
        else:
            try:
                i_path = "ServerFiles/Pagesanddata/" + i + "/"
                files = bucket.list_blobs(prefix=i_path)
                for file in files:
                    blob = bucket.blob(file.name)
                    if "OCR" in file.name:
                        # blob.download_to_filename(ocr_path + "/" + i + "_OCR.txt")
                        # print("ocr", i)
                        pass
                    elif "output_data" in file.name:
                        # blob.download_to_filename(ocr_path + "/" + i + "_output.json")
                        # print("output_data", i)
                        pass
                    elif "maker" in file.name:
                        blob.download_to_filename(
                            ocr_path + "/" + i + "_maker_spacy.json"
                        )
                        print("spacy", i)
                        # pass
                    del blob
                tasks_completed.put(i)
            except Exception as e:
                print("error", str(e))


if __name__ == "__main__":
    # key_path = "//filer-argentina-dev/Argentina/Shared Folder/Manikanda Gokul/ext report manual/prd.json"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    # bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"
    # bucketName = "clgx-clvtowerb-app-cv-gcs01-prd"

    # key_path = r"//filer-argentina-dev/Argentina/Shared Folder/Suraj/Bucket/dev1.json"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    # bucketName = "clgx-clvision-dev-buck1_test"
    # bucketName = "clgx-clvision-dev-buck1_test"

    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucketName)

    # os.mkdir("PASFA.ZYINT.CU31455.LEGALPACKS.LOANCARE.D230122.T055011-6")
    def list_files(bucketFolder):
        files = bucket.list_blobs(prefix=bucketFolder)
        fileList = [file.name for file in files if "." in file.name]
        return fileList

    # print(list_files("Legal/tax_Documents/PASFA.ZYINT.CU31455.LEGALPACKS.LOANCARE.D230122.T055011-5"))
    def download_file(filename):
        print(filename)
        blob = bucket.blob(filename)
        fileName = blob.name.split("/")[-1]
        blob.download_to_filename("" + fileName)
        return "downloaded"

    def download_file2(filename):
        print(filename)
        blob = bucket.blob(filename)
        fileName = blob.name.split("/")[-1]
        blob.download_to_filename("" + fileName)
        return "downloaded"

    folder = "dec"
    # os.mkdir(r"\\10.212.30.30\Share Folder\yokesh\spacy\TX_TEST_OCR")
    ocr_path = rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\set4\uat"  # destination path for ocr
    print(f"\n\nOcr folder path: {ocr_path} \n\n")
    # ocr_path=r"C:\Users\mabdullah\OneDrive - CoreLogic Solutions, LLC\Downloads\TN\Data_Extraction_June" #destination path for ocr
    from pathlib import Path

    Path(ocr_path).mkdir(exist_ok=True, parents=True)
    batch = []
    import pandas as pd

    batch_df = pd.read_csv(
        rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\batchid.csv"
    )  # path here#
    # batch_df=pd.read_csv(r"C:\Users\mabdullah\OneDrive - CoreLogic Solutions, LLC\Downloads\TN\TN_set1.1_4590new.csv") #path here#

    batch = set(batch_df["set4uat"].dropna().to_list())
    print(len(batch))
    from tqdm import tqdm

    tasks_to_do = Queue()
    tasks_completed = Queue()
    for id in tqdm(batch):
        id = int(id)
        tasks_to_do.put(id)
    print(tasks_to_do.qsize())

    process = []
    for i in range(16):
        p = Process(target=download_ocr, args=(tasks_to_do, tasks_completed, ocr_path))
        p.start()
        print(p.pid, "started")
        process.append(p)

    for p in process:
        p.join(1000)

    for p in process:
        if p.is_alive():
            p.terminate()
            print("terminated")
        print(p.pid, "done")
    import os

    print(tasks_completed.qsize(), tasks_to_do.qsize())
    print(len(os.listdir(ocr_path)))
    print("\n\nit is done")
    print(f"\n\nOcr folder path: {ocr_path} \n\n")
