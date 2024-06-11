from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import asyncio
from pyinputplus import inputYesNo

import cProfile
import pstats

# from tqdm import tqdm


def delete(file):
    file.unlink()


async def multi_thread_delete(task_num, folder):
    print(f"started : {task_num}")
    with ThreadPoolExecutor(max_workers=200) as pool:
        loop = asyncio.get_running_loop()
        tasks = map(
            lambda files: loop.run_in_executor(pool, delete, files), folder.iterdir()
        )
        # tasks = [
        #     loop.run_in_executor(pool, lambda x: x.unlink(), f)
        #     for f in folder.iterdir()
        # ]
        # tasks = (
        #     loop.run_in_executor(pool, delete, files) for files in folder.iterdir()
        # )
        await asyncio.gather(*tasks)

    folder.rmdir()
    print(f"ended : {task_num}")
    print("-------------------")


async def main(folders):
    coros = [
        multi_thread_delete(item.name, item) for task_num, item in enumerate(folders)
    ]
    results = await asyncio.gather(*coros, return_exceptions=False)
    print(results)


if __name__ == "__main__":
    mani = [
        folder
        for folder in Path(
            r"\\filer-argentina-dev\Argentina\Shared Folder\Mani\\"
        ).iterdir()
        if "_" in folder.name and folder.is_dir()
    ]
    # mani = [
    #     Path(
    #         r"C:\Users\surakumar\OneDrive - CoreLogic Solutions, LLC\Downloads\KY_data"
    #     )
    # ]
    print(f"\n\n\nTotal number of folders to be deleted -: {len(mani)}\n\n")
    for folder in mani:
        print(f"==> {folder}")

    choice = inputYesNo(prompt="\n\nEnter Y to proceed else enter N -: ", default="N")
    if choice.lower() != "yes":
        exit("Exiting program as user don't want to delete listed folders.")

    with cProfile.Profile() as pr:
        asyncio.run(main(mani))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename=f"{__file__.replace('.py','.prof')}")

# =================================================
# mani = [
#     folder
#     for folder in list(
#         Path(r"\\filer-argentina-dev\Argentina\Shared Folder\Mani\\").iterdir()
#     )
#     if "_" in folder.name and folder.is_dir()
# ]

# print(f"\n\n\nTotal number of folders to be deleted -: {len(mani)}")
# for folder in mani:
#     print(folder)

# choice = inputYesNo(prompt="\n\nEnter Y to proceed else enter N -: ", default="N")
# if choice.lower() != "yes":
#     exit("Exiting program as user don't want to delete listed folders.")


# def delete(path):
#     path.unlink()


# for folder in tqdm(mani):
#     if "_" not in str(folder.name):
#         continue
#     print(folder)
#     with ThreadPoolExecutor(max_workers=200) as executor:
#         executor.map(delete, list(folder.iterdir()))
#     folder.rmdir()

# print("All files and folder has been deleted")


# ==========================================================
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
# from pathlib import Path

# def delete_file(file):
#     try:
#         file.unlink()
#     except Exception as e:
#         print(f"Failed to delete {file}: {e}")

# async def delete_files_in_folder(folder):
#     with ThreadPoolExecutor() as executor:
#         print(folder)
#         loop = asyncio.get_running_loop()
#         futures = [loop.run_in_executor(executor, delete_file, file) for file in folder.iterdir()]
#         await asyncio.gather(*futures)
#         try:
#             folder.rmdir()  # Delete the folder after all files have been deleted
#         except Exception as e:
#             print(f"Failed to delete {folder}: {e}")

# async def main():
#     root_path = Path(r"\\filer-argentina-dev\Argentina\Shared Folder\Mani\\")
#     folders = list(root_path.iterdir())
#     await asyncio.gather(*(delete_files_in_folder(folder) for folder in folders if '_' in folder.name))

# if __name__ == "__main__":
#     asyncio.run(main())
