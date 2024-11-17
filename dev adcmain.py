import json


def extract(data1):
    try:
        import os
        from google.cloud import storage
        import io
        import re
        import pandas as pd
        from datetime import date
        from validationrules import (
            integer,
            non_numeric,
            date,
            validate_integer,
            validate_non_numeric,
            validate_date,
        )
        import ADC_Rptgen
        import base
        from base import bucketName
        from queue import deque
        from pytz import timezone
        from datetime import datetime, timedelta
        import Mail_the_Text
        from download_and_mail import extract
        from code_helper import (
            txt_to_layout_df,
            finaldf_to_validated_df,
            save_to_bucket,
            excel_to_text,
            is_all_records_success,
        )

        #         storage_client = storage.Client()
        json_string = os.environ["clvision-dev-GCS"]
        json_key = json.loads(json_string)
        storage_client = storage.Client.from_service_account_info(json_key)

        bucket = storage_client.get_bucket(bucketName)

        todaydate = (
            (datetime.now().date() - timedelta(days=1))
            .strftime("%d-%m-%Y")
            .replace("-", "")
        )

        todaydate1 = (
            datetime.now(timezone("America/Los_Angeles")) - timedelta(days=1)
        ).strftime("%m%d%Y")

        fromatted = datetime.now(timezone("America/Los_Angeles")).strftime("%Y%m%d")

        fromatted1 = (
            datetime.now(timezone("America/Los_Angeles")).date() - timedelta(days=1)
        ).strftime("%Y%m%d")

        todaydatere = datetime.now(timezone("America/Los_Angeles")).strftime("%m%d%Y")

        check_is_any = bucket.list_blobs(
            prefix="ADC_Transmission/non_merged_files/{0}/".format(todaydatere)
        )

        Adc_trans_blob = bucket.blob(
            "ADC_Transmission/Input_Files/{0}/TCS{1}A.txt".format(
                todaydatere, fromatted
            )
        )

        Adc_secall_blob = bucket.blob(
            "ADC_Transmission/SecondAllocation_MergedOutput/{0}/TCS{1}A.txt".format(
                todaydatere, fromatted
            )
        )

        Adc_secall_blob1 = bucket.blob(
            "ADC_Transmission/SecondAllocation_MergedOutput/{0}/TCS{1}A.txt".format(
                todaydate1, fromatted1
            )
        )

        today_Date = (
            datetime.now(timezone("America/Los_Angeles")).today().strftime("%A")
        )

        finalblobfpost2 = [file.name for file in check_is_any if "." in file.name]

        total_records = ""

        non_duplicate_records = ""

        if len(finalblobfpost2):
            for each in finalblobfpost2:
                blob_read = bucket.blob(each)

                temp_str = blob_read.download_as_string().decode("utf-8")

                total_records = temp_str + "\n" + total_records

            Adc_trans_blob.upload_from_string(total_records)

        total_records = ""

        total_txt_records = ""

        if not Adc_trans_blob.exists() and not len(finalblobfpost2):
            real_out = bucket.list_blobs(
                prefix="MergedOutput/ADC/4000/{0}/".format(todaydate)
            )

            finalblobfpost3 = [file.name for file in real_out if "." in file.name]

            if today_Date == "Monday":
                Date_Fetch = (
                    datetime.now(timezone("America/Los_Angeles")).date()
                    - timedelta(days=2)
                ).strftime("%d%m%Y")

                real_out1 = bucket.list_blobs(
                    prefix="MergedOutput/ADC/4000/{0}/".format(Date_Fetch)
                )

                finalblobfpost4 = [file.name for file in real_out1 if "." in file.name]

                finalblobfpost3 = finalblobfpost3 + finalblobfpost4

                print(finalblobfpost3)

            for each in finalblobfpost3:
                blob_read = bucket.blob(each)

                temp_str = blob_read.download_as_string().decode("utf-8")

                total_records = temp_str + "\n" + total_records
            # DUPLICATE CHECK

            if Adc_secall_blob1.exists():
                blob_read1 = bucket.blob(
                    "ADC_Transmission/SecondAllocation_MergedOutput/{0}/TCS{1}A.txt".format(
                        todaydate1, fromatted1
                    )
                )

                temp_str1 = blob_read1.download_as_string().decode("utf-8").split("\n")

                blob_read2 = total_records.split("\n")

                check_set1 = set(temp_str1)

                check_set2 = set(blob_read2)

                final_check_set = check_set2 - check_set1

                for line in final_check_set:
                    non_duplicate_records = line + "\n" + non_duplicate_records

                Adc_trans_blob.upload_from_string(non_duplicate_records)

            else:
                Adc_trans_blob.upload_from_string(total_records)

        if data1 == "Re-Upload":
            excelpath = "ADC_Transmission/QC_Reports/{0}/TCS{1}A.xlsx".format(
                todaydatere, fromatted
            )

            blob_excel = bucket.blob(excelpath)

            if blob_excel.exists():
                input_text_file = excel_to_text(blob_excel)
            else:
                return "Excel File is Missing"

        elif data1 == "Txt-Upload":
            check_txt_files = bucket.list_blobs(
                prefix="ADC_Transmission/SecondAllocation_InputFiles/{0}/".format(
                    todaydatere
                )
            )

            finalblobfpost5 = [
                file.name for file in check_txt_files if "." in file.name
            ]

            if len(finalblobfpost5) and not Adc_secall_blob.exists():
                for each in finalblobfpost5:
                    blob_read = bucket.blob(each)

                    temp_str = blob_read.download_as_string().decode("utf-8")

                    total_txt_records = temp_str + "\n" + total_txt_records

                Adc_secall_blob.upload_from_string(total_txt_records)

            else:
                return "Second Allocation Already Done"

            Adc_secall_blob = bucket.blob(
                "ADC_Transmission/SecondAllocation_MergedOutput/{0}/TCS{1}A.txt".format(
                    todaydatere, fromatted
                )
            )

            if Adc_secall_blob.exists():
                input_text_file = (Adc_secall_blob.download_as_string()).decode("utf-8")

            else:
                return "No Second Allocation Text files found....Please Verify the same"
        else:
            Adc_trans_blob = bucket.blob(
                "ADC_Transmission/Input_Files/{0}/TCS{1}A.txt".format(
                    todaydatere, fromatted
                )
            )

            if not Adc_trans_blob.exists():
                path = "MergedOutput/ADC/4000/{0}/TCS{1}A.txt".format(
                    todaydate, fromatted
                )

                adcblob = bucket.blob(path)

                if adcblob.exists():
                    blob_input_text_file = bucket.blob(path)

                    bucket.copy_blob(
                        blob_input_text_file,
                        bucket,
                        "ADC_Transmission/Input_Files/{0}/TCS{1}A.txt".format(
                            todaydatere, fromatted
                        ),
                    )

                    input_text_file = (Adc_trans_blob.download_as_string()).decode(
                        "utf-8"
                    )

                else:
                    message = "Hi ADC Team,\n\n Tool Could'nt find any ADC files/Records to proceed with QC for the date {0}\n\n Please verify the same.\n\nRegards, \n Xtractly Transmission team".format(
                        todaydate
                    )
                    is_done = Mail_the_Text.extract(message + "   " + "ADC")
                    return "No Text File Found"
            else:
                input_text_file = (Adc_trans_blob.download_as_string()).decode("utf-8")

        layoutblob = bucket.blob("ADC_Transmission/helper_files/ADC_ layout.xlsx")

        if layoutblob.exists():
            byte_to_excel = io.BytesIO()
            input_layout_xl = layoutblob.download_to_file(byte_to_excel)
            layoutdf = pd.read_excel(byte_to_excel)
        else:
            message = "Hi ADC Team,\n\n Tool Could'nt find some of the necessary helper files to proceed with QC for the date {0}\n\nPlease connect with IT Team for a Fix.\n\nRegards, \n Xtractly Transmission team".format(
                todaydate
            )
            Mail_the_Text.extract(message + "   " + "ADC")
            return "No Helper Excels found.."

        final_df = txt_to_layout_df(input_text_file, layoutdf)

        try:
            if final_df.shape[0] != 0:
                validated_df = finaldf_to_validated_df(final_df, mode=data1)

            else:
                return "Error in final_df" + str(final_df)

        except Exception as err:
            message = "Hi ADC Team,\n\n Tool Could'nt Complete the QC for the date {0} due to the exception {1} and {2}\n\n Please connect with IT team for a Fix.\n\nRegards, \n Xtractly Transmission team".format(
                todaydate, str(err), str(final_df)
            )
            Mail_the_Text.extract(message + "   " + "ADC")
            return message

        try:
            if data1 == "Txt-Upload" and validated_df.shape[0] != 0:
                path_to_save = "ADC_Transmission/Second_Allocation_QCReports/{0}/TCS{1}A.xlsx".format(
                    todaydatere, fromatted
                )

                is_save = save_to_bucket(path_to_save, validated_df)

            elif validated_df.shape[0] != 0:
                path_to_save = "ADC_Transmission/QC_Reports/{0}/TCS{1}A.xlsx".format(
                    todaydatere, fromatted
                )

                is_save = save_to_bucket(path_to_save, validated_df)

            else:
                return "Error in Validated_df" + str(validated_df)

        except Exception as err:
            message = "Hi ADC Team,\n\n Tool Could'nt Complete the QC for the date {0} due to the exception {1} and {2} \n\n Please connect with IT team for a Fix.\n\nRegards, \n Xtractly Transmission team".format(
                todaydate, str(err), str(validated_df)
            )
            Mail_the_Text.extract(message + "   " + "ADC")
            return message

        try:
            if data1 == "Txt-Upload" and is_save == "Saved Successfully":
                mailblob = "ADC_Transmission/Second_Allocation_QCReports/{0}/".format(
                    datetime.now(timezone("America/Los_Angeles")).strftime("%m%d%Y")
                )

                is_mailed = extract(mailblob + "   " + "ADC")

            elif is_save == "Saved Successfully":
                mailblob = "ADC_Transmission/QC_Reports/{0}/".format(
                    datetime.now(timezone("America/Los_Angeles")).strftime("%m%d%Y")
                )

                is_mailed = extract(mailblob + "   " + "ADC")

            else:
                return "Not Saved......due to - " + str(is_save)

        except Exception as err:
            return "From Save" + str(err)

        if data1 != "Txt-Upload":
            check_if_all_success = is_all_records_success(validated_df)

            if check_if_all_success:
                is_rpt_gen = ADC_Rptgen.extract(todaydatere + "   " + fromatted)

                return "Success"
            else:
                return "Failed"

    except Exception as err:
        import traceback

        err = traceback.format_exc()
        import Mail_the_Text

        todaydate = datetime.now(timezone("America/Los_Angeles")).strftime("%d/%m/%Y")
        message = "Hi ADC Team,\n\n Tool Could'nt Complete the QC for the date {0} due to the exception {1}\n\n Please connect with It team for a Fix.\n\nRegards, \n Xtractly Transmission team".format(
            todaydate, str(err)
        )
        Mail_the_Text.extract(message + "   " + "ADC")
        return str(err)


# print(extract("Init-Upload"))
