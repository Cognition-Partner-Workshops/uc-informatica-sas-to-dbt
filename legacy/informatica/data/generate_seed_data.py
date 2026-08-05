#!/usr/bin/env python3
"""Deterministic Informatica seed generator for the before-state CSVs."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as fh:
        writer = csv.writer(fh, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)


def main():
    write_csv(ROOT / 'demo_source1.csv', ['LEAD_CO_MNE','BRANCH_CO_MNE','MIS_DATE','ID','DESCRIPTION','SHORT_NAME'], [
        ['BNK01','BR101','2024-01-31','REC00001','General ledger account 1','GL0001'],
        ['BNK02','BR102','2024-01-31','REC00002','General ledger account 2','GL0002'],
        ['BNK03','BR103','2024-01-31','REC00003','General ledger account 3','GL0003'],
        ['BNK04','BR104','2024-01-31','REC00004','General ledger account 4','GL0004'],
        ['BNK05','BR105','2024-01-31','REC00005','General ledger account 5','GL0005'],
        ['BNK06','BR106','2024-01-31','REC00006','General ledger account 6','GL0006'],
        ['BNK07','BR107','2024-01-31','REC00007','General ledger account 7','GL0007'],
    ])
    write_csv(ROOT / 'demo_target1.csv', ['Key','LEAD_CO_MNE','BRANCH_CO_MNE','MIS_DATE','ID','DESCRIPTION','SHORT_NAME','CREATED_BY','CREATED_TIME','UPDATED_BY','UPDATED_TIME','ACTIVE_FLAG','START_DATE','END_DATE'], [
        [1,'BNK01','BR101','2024-01-31','REC00001','Existing account 1','GL0001','IDWUSER','2024-01-15 00:00:00','IDWUSER','2024-01-15 00:00:00','Y','2023-01-01','9999-12-31'],
        [2,'BNK02','BR102','2024-01-31','REC00002','Existing account 2 old key','GL0002','IDWUSER','2024-01-15 00:00:00','IDWUSER','2024-01-15 00:00:00','Y','2023-01-01','9999-12-31'],
        [99,'BNK02','BR102','2024-01-31','REC00002','Existing account 2 new key','GL0002','IDWUSER','2024-01-16 00:00:00','IDWUSER','2024-01-16 00:00:00','Y','2023-01-01','9999-12-31'],
        [3,'BNK03','BR103','2024-01-31','REC00003','Existing account 3','GL0003','IDWUSER','2024-01-15 00:00:00','IDWUSER','2024-01-15 00:00:00','Y','2023-01-01','9999-12-31'],
        [40,'BNK40','BR140','2024-01-31','REC90001','Unrelated existing row','GL9040','IDWUSER','2024-01-15 00:00:00','IDWUSER','2024-01-15 00:00:00','Y','2023-01-01','9999-12-31'],
    ])
    write_csv(ROOT / 'demo_source3.csv', ['TX_ID','ACCT_ID','FIRST_NM','LAST_NM','TX_DTTM','TX_AMT','TX_TYPE_CD','BAL_AMT','TX_DESC','CRDT_SCORE','CUST_ID'], [
        [5001,1001,'MAX','SINGH','2024-01-14 10:28:00',2131.24,'DR',42329.05,'CASH DEPOSIT',420,70031],
        [5002,1001,'MAX','SINGH','2024-01-15 11:00:00',-100.00,'CR',42229.05,'FEE',420,70031],
        [5003,1002,'OMAR','SILVA','2024-01-14 05:49:00',-1238.81,'CR',91291.88,'ONLINE TRANSFER',720,70032],
        [5004,1003,'IVY','COSTA','2024-01-25 21:01:00',2446.85,'CR',86284.15,'POS PURCHASE',715,70033],
        [5005,1004,'NINA','PATEL','2024-01-11 17:00:00',2070.53,'CR',72185.35,'POS PURCHASE',409,70034],
        [5006,1005,'RAVI','WEISS','2024-01-09 08:22:00',199.99,'DR',11111.11,'ATM WITHDRAWAL',615,70035],
    ])
    write_csv(ROOT / 'demo_source4.csv', ['ACCT_ID','ACCT_TYP','ACCT_DESC','CRDT_LN','CR8_DT','CLSR_DT','ACCT_STAT_CD'], [
        [1001,'SB','Account 1001 ledger','  8000','2023-08-18','2025-06-30','A'],
        [1002,'SB','Account 1002 ledger','48000','2017-02-09','','D'],
        [1003,'CA','Account 1003 ledger','7000','2023-12-11','','D'],
        [1004,'CA','Account 1004 ledger','1000','2016-10-19','','A'],
        [1005,'','Account 1005 ledger','9000','2020-01-01','','P'],
    ])
    write_csv(ROOT / 'demo_source5.csv', ['PRODUCT_ID','PRODUCT_NM','PRODUCT_NO','COLOR','STD_COST','LIST_PRICE','SELL_ST_DT','SELL_ED_DT'], [
        ['PRD0001','Card Product 001','P001','Black','186','783','10/02/2020','17/07/2024'],
        ['PRD0002','Card Product 002','P002','Black','908','737','11/07/2021','28/09/2025'],
        ['PRD0003','Card Product 003','P003','Blue','161','351','03/05/2021','23/08/2025'],
        ['PRD0004','Card Product 004','P004','Red','805','836','01/08/2020','20/01/2026'],
    ])
    write_csv(ROOT / 'lkp_demo_source1.csv', ['ACCT_ID','CUST_ID','FIRST_NM','LAST_NM','CUST_ADDR','CUST_PHN','CUST_EML_ADDR','AGE','DOB','CUST_TYP'], [
        [1001,70031,'AVA','BAKER','46 High Street','2580606026','c1001@mail.example',36,'1952-07-23','CORP'],
        [1002,70032,'NINA','WEISS','857 High Street','2317518731','c1002@mail.example',35,'1969-08-06','RET'],
        [1002,70032,'ZOE','WEISS','999 High Street','2317518731','c1002b@mail.example',36,'1968-08-06','CORP'],
        [1003,70033,'IVY','SILVA','449 High Street','2072328507','c1003@mail.example',71,'1963-03-23','CORP'],
        [1004,70034,'AVA','RIVERA','422 High Street','2478922435','c1004@mail.example',55,'1986-01-27','CORP'],
        [1005,70035,'RAVI','PATEL','100 Main Street','2223334444','c1005@mail.example',44,'1980-12-12','SMB'],
    ])
    write_csv(ROOT / 'lkp_demo_source2.csv', ['CUST_ID','CRDT_SCORE','MAX_CRDT_SCORE','MIN_CRDT_SCORE','MAX_CRDT_LMT','CURR_CRDT_BAL_AMT','AVG_INC_AMT'], [
        [70031,699,741,657,182000,21143.19,10527.80],
        [70032,435,470,421,138000,26422.60,11326.72],
        [70032,450,480,430,140000,20000.00,12000.00],
        [70033,677,700,653,86000,23474.97,6015.99],
        [70034,626,635,618,88000,31656.74,2913.69],
        [70035,512,530,500,91000,15000.00,8000.00],
    ])
    write_csv(ROOT / 'lkp_demo_source3.csv', ['ACCT_ID','TX_TYPE_CD','TX_TYPE_DESC'], [
        [1001,'DR','Credit posting'],
        [1002,'TR','Debit posting first'],
        [1002,'DR','Debit posting last'],
        [1003,'DR','Debit posting'],
        [1004,'CR','Credit posting'],
        [1005,'NA','No activity'],
    ])
    write_csv(ROOT / 'demo_source2.csv', ['Title','First_Name','Middle_Name','Last_Name','Member_ID','Member_Suffix','Birth_Date','Gender_Code','Member_Record_Number','Social_Security_Number','Member_Type_Code','Original_Effective_Date','Relationship_to_Subscriber_Code','Relationship_to_Subscriber_Code_Label'], [
        ['MS','Eli','R','Baker',30001,'II','1990-07-12','M',500000,'',1,'2022-05-01',2,'CHILD'],
        ['MR','Omar','K','Okafor',30002,'','1990-11-16','F',500001,100000037,2,'2016-09-01',19,'SELF'],
        ['MS','Omar','I','Novak',30003,'','1998-04-03','M',500002,'',2,'2016-05-01',18,'CHILD'],
        ['MS','Ravi','O','Weiss',30004,'','1948-12-22','F',500003,100000111,2,'2019-02-01',18,'OTHER'],
        ['MR','Mina','Q','Lee',30005,'Jr','1975-06-14','F',500004,'',None,'2020-03-01',3,'CHILD'],
        ['MS','Tara','S','Young',30006,'','1982-11-01','F',500005,100000222,1,'2021-07-01',1,'SPOUSE'],
        ['MR','Nico','T','Singh',30007,'','1992-09-30','M',500006,'',2,'2023-02-14',19,'SELF'],
    ])
    write_csv(ROOT / 'abort' / 'demo_source2.csv', ['Title','First_Name','Middle_Name','Last_Name','Member_ID','Member_Suffix','Birth_Date','Gender_Code','Member_Record_Number','Social_Security_Number','Member_Type_Code','Original_Effective_Date','Relationship_to_Subscriber_Code','Relationship_to_Subscriber_Code_Label'], [
        ['MS','Tara','S','Young',40001,'','1982-11-01','F',600001,100000222,1,'2021-07-01',1,''],
    ])

if __name__ == '__main__':
    main()
