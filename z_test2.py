from datetime import datetime, timedelta
import re
import calendar

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

