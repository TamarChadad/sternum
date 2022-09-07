# sternum
home task from sternum statup

## Parking lot with license number restrictions

The service gets an image of an Israeli license plate and extract the digits license by public API [ocr](https://ocr.space/ocrapi) and returns a decision whether a vehicle may enter the parking
lot, the decision should be determined by the following rules:

● Public transportation vehicles may enter the parking lot (their license plates always end
with 25 or 26).
● digits numbers whose two last digits are 85/86/87/88/89/00, should not enter.
● If the license plate number consists of 7 digits, and ends with 0 or 5, he cannot enter.

Addinial:

-- The service will allow all vehicles to exit.

-- Each decision write in a local database (attach script_tables_in_sql_server.sql)

-- Parking lot have a capacity, if the parking lot is full, The system will not allow to enter.

-- There are 2 tables in DB, EntrancesAndExitsVehicles table to save all entrances and exits with timestamp, 
NotAllowedEnterVehicles table to save all the vehicles that where not allowed enter both because invalid license and because the OCR.SPCAE was not succeeded extract the text)

--The tables with indexes on columns timestamp and number license for data can be easily retrieved from it.

--The service write log in file parking_lot.log .

--There are options to select from DB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install
requests,
pyodbc,
Flask

```bash
pip install requests
pip install pyodbc
pip install Flask
```

## Usage
1.run file parking_lot_service/parking_lot_server.py

2.run file parking_lot_client/main.py

3.Follow the instructions that appear on the main.py console
