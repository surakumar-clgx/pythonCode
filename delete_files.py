from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(
    filename=r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\pythonCode\delete_files.log",
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s- %(message)s",
)
logging.info(
    "=================================> Start of program <=========================================="
)

# logging.disable(logging.DEBUG)


def delete_empty_files(folder):
    for file in folder.iterdir():
        size = file.stat().st_size
        if size == 0:
            print(f"deleting empty file : {file.name}")
            file.unlink()


def delete_files(batchid_list):
    logging.debug(f"type of batchid values passed: {type(batchid_list[0])}")
    deleted_files_count = 0
    for b in batchid_list:
        b = int(b)
        ocr_name = f"{b}_OCR.txt"
        ocr_path = Path.joinpath(mort_dir, ocr_name)
        out1 = ocr_path.is_file()

        keyed_name = f"{b}_output.json"
        keyed_path = Path.joinpath(mort_dir, keyed_name)
        out2 = keyed_path.is_file()

        # zip_name = f"{b}.zip"
        # zip_path = Path.joinpath(mort_dir,zip_name)
        # out3 = zip_path.is_file()

        if (not out1) or (not out2):  # or (not out3):
            deleted_files_count += 1
            ocr_path.unlink(missing_ok=True)
            keyed_path.unlink(missing_ok=True)
            # zip_path.unlink(missing_ok=True)
            print(f"deleted {b} ocr and json")
            logging.info(f"deleted {b} ocr and json")
    return deleted_files_count


if __name__ == "__main__":
    # mort_dir = Path(r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\GTQ_images_ocrs\Prod\mortgage\FL\\")
    month = "dec"
    mort_dir = Path(
        rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\KY_data\{month}\adcNew"
    )
    batch_df = pd.read_csv(
        rf"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\Billing\KY_{month.upper()}_adc.csv"
    )
    batchid_list = batch_df[f"docid"].dropna().to_list()

    delete_empty_files(mort_dir)
    deleled_files_count = delete_files(batchid_list)
    print(deleled_files_count)
