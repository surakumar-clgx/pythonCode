from pathlib import Path
import win32com.client as win32
from tqdm import tqdm
import os
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("path")

args = parser.parse_args()

target_dir = Path(args.path)


def convert_xls_to_xlsx(path: Path) -> None:
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    wb = excel.Workbooks.Open(path.absolute())
    # FileFormat=51 is for .xlsx extension
    wb.SaveAs(str(path.absolute().with_suffix(".xlsx")), FileFormat=51)
    wb.Close()
    excel.Application.Quit()
    os.remove(path)


for xls in tqdm(list(target_dir.glob(r"*.xls"))):
    print(xls)
    convert_xls_to_xlsx(xls)
