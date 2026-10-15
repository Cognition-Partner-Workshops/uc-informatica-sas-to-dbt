# Proof query as demo user, role `SF_20261015_DS_DBT`

## Query 1

| ACCOUNT_ID | BRANCH_ID | CUSTOMER_ID | FIRST_NAME | LAST_NAME | PRIMARY_EMAIL | PHONE_NUMBER | SSN_HASH | DATE_OF_BIRTH | OFFICER_ID |
|---|---|---|---|---|---|---|---|---|---|
| A00000001 | B015 | C0000001 | Linda | Lopez | linda.lopez1@example.com | 555-943-3892 | a47401f094a96eef71465948a306129a | 1958-08-12 | O0088 |
| A00000002 | B024 | C0000002 | Thomas | Baker | thomas.baker2@example.com | 555-664-0922 | e8f6ac86478b28d9ff260f354890039e | 1999-04-17 | O0039 |
| A00000003 | B019 | C0000002 | Thomas | Baker | thomas.baker2@example.com | 555-664-0922 | e8f6ac86478b28d9ff260f354890039e | 1999-04-17 | O0057 |
| A00000004 | B032 | C0000003 | Richard | Carter | richard.carter3@example.com | 555-659-7317 | 94994914e7f58574ead7ccda59c1224c | 1974-01-17 | O0107 |
| A00000005 | B035 | C0000003 | Richard | Carter | richard.carter3@example.com | 555-659-7317 | 94994914e7f58574ead7ccda59c1224c | 1974-01-17 | O0042 |

## Query 2

| ORIGINAL_EFFECTIVE_DATE | MEMBER_TYPE_CODE | TITLE | FIRST_NAME | LAST_NAME | MEMBER_ID | SOCIAL_SECURITY_NUMBER | BIRTH_DATE | GENDER_CODE |
|---|---|---|---|---|---|---|---|---|
| 2016-05-01 00:00:00 | 2.0 | MS | Omar | Novak | 30003.0 | NULL | 1998-04-03 00:00:00 | M |
| 2016-09-01 00:00:00 | 2.0 | MR | Omar | Okafor | 30002.0 | 100000037.0 | 1990-11-16 00:00:00 | F |
| 2019-02-01 00:00:00 | 2.0 | MS | Ravi | Weiss | 30004.0 | 100000111.0 | 1948-12-22 00:00:00 | F |

## Query 3

| SEED_ROW | CUST_ID | CRDT_SCORE |
|---|---|---|
| 1 | 70031 | 699 |
| 2 | 70032 | 435 |
| 3 | 70032 | 450 |

## Query 4

| CUSTOMER_ID | FIRST_NAME | PRIMARY_EMAIL | DATE_OF_BIRTH | CUSTOMER_SEGMENT |
|---|---|---|---|---|
| C0000031 | Jennifer | jennifer.miller31@example.com | 2003-01-01 | COMM |
| C0000083 | Joseph | joseph.miller83@example.com | 1987-06-27 | COMM |
| C0000106 | Linda | linda.jackson106@example.com | 1980-03-09 | COMM |
