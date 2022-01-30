# blindSQLInjection
Automated script to run a Blind SQL Injection. Getting elements of the table information.

## Description:
The implementation of the code is based on the use of three SQL statements to obtain information relative to:
- Total number of entries in the TableName.
- Total size of each of the elements of the TableName.
- Getting the data fo the content of the TableName.
To work fine, the script needs the following input parameters:
- Url -> The Url of the target
- Table Name -> the name of the target table
- Columns Name -> the column names of the target table
- Output file -> the output file where it stores the data (.txt)

```
> python3 blindSQLInjection.py --h
usage: blindSQLInjection.py [-h] -u URLBASE -t TABLENAME -c COLUMNNAME -o FILE

Blind SQLi Script v1.0 by Josan Garrido

optional arguments:
  -h, --help     show this help message and exit
  -u URLBASE     url web application
  -t TABLENAME   table name of data base
  -c COLUMNNAME  list of column name in a table
  -o FILE        path to output file .txt
```

## Commands
1. Get information of Script functionalities, using `--h`:\
`> python3 blindSQLInjection.py --h`
2. Execute script:\
`> python3 blindSQLInjection.py -u 'http://example/test.php' -t 'TableName' -c 'columnName1, columnName2, columnName3' -o result_Output.txt`

## Requirements
- [Python](http://www.python.org/download/) version **3.x** is required for running this program.
