import calendar

print('カレンダーアプリを開始します。')

while True:
    year = int(input('年を入力してください: '))
    month = int(input('月を入力してください: '))
    print(calendar.month(year, month))
    cont = input('続けますか？（yes/no）: ')
    if cont.lower() != 'yes':
        break

print('カレンダーアプリを終了します。')