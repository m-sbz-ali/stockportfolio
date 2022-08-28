import csv
from csv import DictWriter
import os
from os.path import isfile, join
from typing import Dict, List
import xlsxwriter
import string
from share_sight_csv_split import csvRecord

# CSV_PATH = "/home/max/winhome/work/tax/2023/trades/IB/"
# CSV_PATH = "/home/max/stockportfolio/../winhome/Downloads/"
CSV_PATH = "./"
FILE_NAME = "ShareSightsRep.csv"

class weeklyRepPrep:
    def __init__(self) -> None:
        self._hdr_keys = []

    def insert_empty_row(self, file="", at_row_no = 2 ):
        f_in = join(CSV_PATH, FILE_NAME)
        f_out = join(CSV_PATH, FILE_NAME.split('.')[0]+'_tmp.csv')
        row_no = 1
        with open(f_in, mode = 't+r', newline='') as csv_in:
            with open(f_out, mode = 't+w', newline='') as csv_out:
                csv_rd = csv.reader(csv_in, delimiter=',')
                csv_wr = csv.writer(csv_out, delimiter=',')

                for row in csv_rd:
                    # Get Header and Empty row
                    if row_no == 1:
                        self._hdr_keys = row
                        self._empty_row = []
                        for cols in self._hdr_keys:
                            self._empty_row.append('')

                    if row_no == at_row_no:
                        csv_wr.writerow(self._empty_row)

                    csv_wr.writerow(row)
                    row_no += 1

            csv_in.close()
            csv_out.close()
            os.rename(f_out, f_in)

    def insert_column(self, transform_row):

        f_in = join(CSV_PATH, FILE_NAME)
        f_out = join(CSV_PATH, FILE_NAME.split('.')[0]+'_tmp.csv')
        with open(f_in, mode = 't+r', newline='') as csv_in:
            with open(f_out, mode = 't+w', newline='') as csv_out:
                csv_rd = csv.reader(csv_in, delimiter=',')
                csv_wr = csv.writer(csv_out, delimiter=',')

                for row in csv_rd:
                    transform_row(row, csv_rd.line_num)
                    # Get Header and Empty row
                    csv_wr.writerow(row)

            csv_in.close()
            csv_out.close()
            os.rename(f_out, f_in)

def main():
    print("Hello World!")
    weekly_rep_prep = weeklyRepPrep()

    weekly_rep_prep.insert_empty_row(at_row_no = 2)

    def transform_fun_OzPnL(row, line_num):
        if line_num == 1 :
            row.insert(10, 'OzPnL')
        else:
            row.insert(10, '')

    weekly_rep_prep.insert_column(lambda row, line_num: transform_fun_OzPnL(row, line_num))

    def transform_fun_OzComm(row, line_num):
        if line_num == 1 :
            row.insert(16, 'OzComm')
        else:
            row.insert(16, '')
    weekly_rep_prep.insert_column(lambda row, line_num: transform_fun_OzComm(row, line_num))

if __name__ == "__main__":
    main()
