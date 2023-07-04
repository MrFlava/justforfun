import argparse
from os import getenv
from pprint import pprint

import pandas as pd
from loguru import logger
from dotenv import load_dotenv


def create_dataframe_from_csv_in_drive(document_url: str) -> pd.DataFrame:
    file_id = document_url.split("/")[-2]
    dwn_url = f'{getenv("URL_FOR_READ_CSV")}{file_id}'

    full_data = pd.read_csv(dwn_url)
    return full_data


def get_fields_from_terminal():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--fields",  nargs='+', help="fields to display")
    args = argParser.parse_args()

    return args.fields


def create_sub_dataframe(full_dataframe: pd.DataFrame, fields: list) -> pd.DataFrame:
    try:
        return full_dataframe[fields]

    except KeyError:
        logger.error(f"Key error: there's no fields like {fields} in the DataFrame")
        raise KeyError


def main():
    # Loading necessary variables from .env file
    load_dotenv()
    fields = get_fields_from_terminal()

    # Creating a dataframe from the .CSV file
    full_dataframe = create_dataframe_from_csv_in_drive(getenv("DOCUMENT_URL"))

    # if we have a fields argument from the terminal we will create the sub-dataframe,
    # otherwise it will be the full dataframe
    if fields:
        result_dataframe = create_sub_dataframe(full_dataframe, fields)

    else:
        result_dataframe = full_dataframe

    pprint({"data": result_dataframe.to_dict(orient="records")})


if __name__ == "__main__":
    main()

