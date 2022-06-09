# This uploads xml files into an existing database called shufersalist. For the shufersalist SQL create statement see shufersalist_creator.sql


import sqlite3
from datetime import date

today = date.today()
print("Today's date:", today)

import os

path = os.path.join(r"C:\..\Kimonaim\shufersal", str(today))

os.chdir(path)

import xml.etree.ElementTree as ET

xml_files = []

for file in os.listdir(os.getcwd()):
    if file.endswith(".xml"):
        xml_files.append(file)

print(xml_files)
# for xml_file in xml_files:
#     date = str((xml_file[27:])[:-12] + "-" + (xml_file[31:])[:-10] + "-" + (xml_file[33:])[:-8])
#     print(date)


for xml_file in xml_files:

    mytree = ET.parse(xml_file)
    myroot = mytree.getroot()
    items = myroot.find("Items")
    df_cols = [
        "filename",
        "date",
        "PriceUpdateDate",
        "ItemCode",
        "ItemType",
        "ItemName",
        "ManufacturerName",
        "ManufactureCountry",
        "ManufacturerItemDescription",
        "UnitQty",
        "Quantity",
        "bIsWeighted",
        "UnitOfMeasure",
        "QtyInPackage",
        "ItemPrice",
        "UnitOfMeasurePrice",
        "AllowDiscount",
        "ItemStatus",
    ]
    conn = sqlite3.connect((r"C:\..\Kimonaim\shufersalist.db"))
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    fileList = cur.execute("SELECT filename FROM shufersalPrices").fetchall()
    if xml_file[:-4] in fileList:
        print("File already loaded.")
        conn.close()
        continue
    for i in items:
        filename = xml_file[:-4]
        store_id = (filename[:-13])[23:]
        date = str(
            (xml_file[27:])[:-12]
            + "-"
            + (xml_file[31:])[:-10]
            + "-"
            + (xml_file[33:])[:-8]
        )
        PriceUpdateDate = i.find("PriceUpdateDate").text
        ItemCode = int(i.find("ItemCode").text)
        ItemName = i.find("ItemName").text
        ManufacturerName = i.find("ManufacturerName").text
        ManufactureCountry = i.find("ManufactureCountry").text
        ManufacturerItemDescription = i.find("ManufacturerItemDescription").text
        UnitQty = i.find("UnitQty").text
        Quantity = i.find("Quantity").text
        UnitOfMeasure = i.find("UnitOfMeasure").text
        ItemPrice = float(i.find("ItemPrice").text)
        UnitOfMeasurePrice = float(i.find("UnitOfMeasurePrice").text)
        AllowDiscount = int(i.find("AllowDiscount").text)

        conn = sqlite3.connect(r"C:\..\Kimonaim\shufersalist.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO shufersalPrices VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                filename,
                store_id,
                date,
                PriceUpdateDate,
                ItemCode,
                ItemName,
                ManufacturerName,
                ManufactureCountry,
                ManufacturerItemDescription,
                UnitQty,
                Quantity,
                UnitOfMeasure,
                ItemPrice,
                UnitOfMeasurePrice,
                AllowDiscount,
            ),
        )
        conn.commit()
        conn.close()

print("ALl finished!")
