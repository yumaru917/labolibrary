import csv
import gspread
import json

# ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('lablib.json', scope)

# OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

# 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1OJnU1BcwWLJcGSIItdkvuN0GAvTEgKZKkZ7yQWyOwbQ'

# 共有設定したスプレッドシートを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

worksheet_list = workbook.worksheets()

print(worksheet_list)

# faculty = '工学系研究科'
# worksheet = workbook.worksheet('工学系研究科')

faculty = '新領域創成科学研究科'
worksheet = workbook.worksheet('新領域創生科学研究科')

cell_list = worksheet.get_all_values()

with open('laboratory_info.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in cell_list:
        if row[0] != '' and 'http' not in row[0]:
            department = row[0]
        else:
            print('except-----------------------------')
            pass
        if row[2]:
            laboratory = row[2]
            laboratory = laboratory.replace('\u3000', '')
        else:
            laboratory = 'unknown'
        if row[3]:
            professor = row[3]
            professor = professor.replace('\u3000', ' ')
        else:
            professor = 'unknown'
        if row[4]:
            laboratory_info = row[4]
            laboratory_info = laboratory_info.replace('\r', '')
            laboratory_info = laboratory_info.replace('\n', '')
        else:
            laboratory_info = 'unknown'
        if row[5]:
            laboratory_HP = row[5]
        else:
            laboratory_HP = ''
        if row[6]:
            research_keyword = row[6]
        else:
            research_keyword = ''
        if row[7]:
            site_from = row[7]
        elif row[5]:
            site_from = row[5]
        else:
            site_from = 'unknown'

        laboratory_dictionary = {
            'faculty': faculty,
            'department': department,
            'laboratory': laboratory,
            'professor': professor,
            'laboratory_info': laboratory_info,
            'laboratory_HP': laboratory_HP,
            'research_keyword': research_keyword,
            'site_from': site_from
        }

        print(laboratory_dictionary)

        laboratory_csv_row = [
            faculty,
            department,
            laboratory,
            professor,
            laboratory_info,
            laboratory_HP,
            research_keyword,
            site_from
        ]

        # writer.writerow(row)
        writer.writerow(laboratory_csv_row)

# print(cell_list)

# A1セルの値を受け取る
# import_value = worksheet.acell('A1').value

# A1セルの値に100加算した値をB1セルに表示させる
# export_value = import_value + 100
# worksheet.update_cell(1, 2, export_value)

# print(import_value)
