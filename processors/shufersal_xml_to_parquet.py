import csv
import gzip
import multiprocessing
import os
import re
import xml.etree.ElementTree as ET
from datetime import date
from multiprocessing import Pool

from tqdm import tqdm

x = dict()


def extract_xml_row_to_dict(row):

    res = dict(
        PriceUpdateDate=row.find("PriceUpdateDate").text,
        ItemCode=int(row.find("ItemCode").text),
        ItemName=row.find("ItemName").text,
        ManufacturerName=row.find("ManufacturerName").text,
        ManufactureCountry=row.find("ManufactureCountry").text,
        ManufacturerItemDescription=row.find("ManufacturerItemDescription").text,
        UnitQty=row.find("UnitQty").text,
        Quantity=row.find("Quantity").text,
        UnitOfMeasure=row.find("UnitOfMeasure").text,
        ItemPrice=float(row.find("ItemPrice").text),
        UnitOfMeasurePrice=float(row.find("UnitOfMeasurePrice").text),
        AllowDiscount=int(row.find("AllowDiscount").text),
    )
    return res


branch_id_regex = re.compile("-(\d{3,})-")


def process_file(filepath):
    rows = []
    branch_id = branch_id_regex.search(filepath).group(1)
    gzip_file = gzip.open(filepath, mode="rt")  # open in text mode:
    mytree = ET.parse(gzip_file)
    xml_root = mytree.getroot()
    items = xml_root.find("Items")
    for row in items:
        extracted = extract_xml_row_to_dict(row)
        extracted["branch_id"] = branch_id
        rows.append(extracted)
    return rows


def file_iterator(base_path):

    csv_writer = None
    output_file = open("/tmp/prices4.csv", "w")
    filepaths = []
    for filename in os.listdir(base_path):
        if filename.endswith(".gz") and "pricefull" in filename.lower():
            filepath = os.path.join(base_path, filename)
            filepaths.append(filepath)
    print("Start")
    pool = Pool(processes=multiprocessing.cpu_count() - 1)
    for rows in tqdm(
        pool.imap_unordered(process_file, filepaths), total=len(filepaths)
    ):
        if csv_writer is None:
            csv_writer = csv.DictWriter(
                output_file,
                rows[0].keys(),
                quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC,
            )
            csv_writer.writeheader()
        csv_writer.writerows(rows)


if __name__ == "__main__":
    file_iterator("/tmp/dir/full")
