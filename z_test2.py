from datetime import datetime, timedelta
import re
import calendar
import json

# 獲取當前日期
current_date = datetime.now()

# 加上兩周
two_weeks_later = current_date + timedelta(weeks=2)

# 找到兩周後的周三
while two_weeks_later.weekday() != 2:  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    two_weeks_later += timedelta(days=1)

print("兩周後的周三日期是:", two_weeks_later.strftime('%Y-%m-%d'))

weekday_mapping = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
print(weekday_mapping.index('周日'))


def check_period(text):
    periods = ['早上', '中午', '下午', '晚上']

    morning = list(set(re.findall(r'早上', text)))
    morning_number = len(morning)

    noon = list(set(re.findall(r'中午', text)))
    noon_number = len(noon)

    afternoon = list(set(re.findall(r'下午', text)))
    afternoon_number = len(afternoon)

    night = list(set(re.findall(r'晚上', text)))
    night_number = len(night)

    if morning_number + noon_number + afternoon_number + night_number == 1:
        print('do something')
        for period in periods:
            if period in text:
                break
        return text.replace(period, ''), period
    else:
        return text, -1


text, period = check_period('我早上去上廁所 明天早上還要去運動')
if period != -1:
    print('單獨一個時段', period)
text, period = check_period('我晚上想要去打球')
if period != -1:
    print('單獨一個時段', period)

month = 3
year = datetime.now().year + 1
print(year)
days_in_month = calendar.monthrange(year, month)[1]
print(days_in_month)


text = ' 台北 台北'
cities = re.findall(r"(台北|雲林|連江|台南|花蓮|屏東|高雄|彰化|新竹|台中|桃園|金門|宜蘭|澎湖|新北|苗栗|南投|基隆|台東|嘉義)", text)
print(cities)
print(text.find('台北'))

text = 'week range year'
matches = re.findall(r'year|month|week|day|hour|minute|second|range', text)
print(matches)

text = '下周到下下周 123123123123'
print(text[:3])
print(text[6:])
print(f"{' ' * len(text)}")


with open('concert.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

indexes = [94, 137, 174]
for index in indexes:
    print(data[index]['pdt'])

chinese_num_map = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '日': '6'}

current_time = datetime.now()
print(current_time)

current_week = current_time.isocalendar()[1]
print(current_week)

current_day_of_week = current_time.weekday()
print(current_day_of_week)

furute_week_day = ()

texts = ['下下周四', '下下周五', '下下下下周六']
current_weekday = datetime.now().weekday()
print(f'current weekday = {current_weekday}')
for text in texts:
    chinese_week_num_map = {'一': '0', '二': '1', '三': '2', '四': '3', '五': '4', '六': '5', '日': '6'}
    # 下下周一、下下周二 ...
    matches = re.findall(r'(下{2,})周(一|二|三|四|五|六|日)', text)
    for match in matches:
        grain = 'day'
        match_text = f'{match[0]}周{match[1]}'
        # # print(f'after {len(match[0])} weeks')
        # # print(f'>> {chinese_num_map[match[1]]}')
        # days_after = (int(chinese_week_num_map[match[1]]) - current_weekday) % 7 + 7 * len(match[0])
        # # print(f'future week day = {days_after}')
        # future_date = datetime.now() + timedelta(days=days_after)
        # # print(f'future date = {future_date}')
        # # print(future_date.replace(hour=0, minute=0, second=0, microsecond=0))
        # print(str(future_date.replace(hour=0, minute=0, second=0, microsecond=0)))
        # time_line = str(datetime.now() + timedelta(days=days_after))
        days_after = (int(chinese_week_num_map[match[1]]) - datetime.now().weekday()) % 7 + 7 * len(match[0])
        future_date = datetime.now() + timedelta(days=days_after)
        time_line = str(future_date.replace(hour=0, minute=0, second=0, microsecond=0))
        print(time_line)
        print(type(time_line))
        print('---')
