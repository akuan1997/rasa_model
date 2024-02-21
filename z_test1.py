from duckling import *
from datetime import datetime
import calendar
import re

weekday_mapping = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def get_how_many_weeks_after(text):
    start_index = text.find('下下周')
    if start_index != -1:
        end_index = start_index + 2
        while True:
            if text[start_index - 1] == '下':
                start_index = start_index - 1
            else:
                break
        print(len(text[start_index:end_index]))

        return text[start_index:end_index + 1], len(text[start_index:end_index])
    else:
        return -1


def get_how_many_weeks_before(text):
    start_index = text.find('上上周')
    if start_index != -1:
        end_index = start_index + 2
        while True:
            if text[start_index - 1] == '上':
                start_index = start_index - 1
            else:
                break
        # print(len(text[start_index:end_index]))

        return text[start_index:end_index + 1], len(text[start_index:end_index])
    else:
        return -1


def get_weekday_number(text):
    '''
    周一到周日的文字轉換為數字
    譬如說想要找到周三
    while two_weeks_later.weekday() != 2:  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    two_weeks_later += timedelta(days=1)
    '''
    if text in weekday_mapping:
        weekday_number = weekday_mapping.index(text)
        return weekday_number
    else:
        return -1


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


def kuan(text):
    # 處理字串
    text = text.replace('週', '周').replace('星期天', '星期日').replace('禮拜天', '禮拜日'). \
        replace('星期', '周').replace('禮拜', '周').replace('的', '').replace('下午茶', '下午')
    # 取得時段 沒有時段period就返回-1
    text, period = check_period(text)
    # 目前的年/月/日/周
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day
    week = int(current_datetime.strftime("%U"))
    print(f'{year}-{month}-{day} / {year}的第{week}周')
    # week_day = -1

    # 下下周 獲得要往後幾周 從字串中移除關鍵字
    if '下下周' in text:
        print(f'week: {week}')
        weeks_text, plus_weeks = get_how_many_weeks_after(text)
        week += plus_weeks
        text = text.replace(weeks_text, '')
        print(f'week: {week}')
    # 上上周 告知無法提供資訊 從字串中的關鍵字移除
    elif '上上周' in text:
        print('不好意思，我們無法提供過去的演唱會資訊')
        weeks_text, minus_weeks = get_how_many_weeks_before(text)
        text = text.replace(weeks_text, '')

    # 1~10
    if '月初' in text:
        start_date = datetime(year=year, month=month, day=1)
        end_date = datetime(year=year, month=month, day=10)
        print(f'月初 {start_date} ~ {end_date}')
        text = text.replace('月初', '月')
    # 11~20
    elif '月中' in text:
        start_date = datetime(year=year, month=month, day=11)
        end_date = datetime(year=year, month=month, day=20)
        print(f'月中 {start_date} ~ {end_date}')
        text = text.replace('月中', '月')
    # 21~底
    elif '月底' in text:
        start_date = datetime(year=year, month=month, day=21)
        days_in_month = calendar.monthrange(year, month)[1]
        end_date = datetime(year=year, month=month, day=days_in_month)
        print(f'月底 {start_date} ~ {end_date}')
        text = text.replace('月底', '月')

    print(text)
    '''
    範圍
    N 和 N 之間 ? (N 到 N)
        yes -> from to
        no -> N 和 N?
            yes -> split('和') -> ...
            no -> ...
    '''

def month_beg_mid_end(text):
    # 1~10
    if '月初' in text:
        start_date = datetime(year=year, month=month, day=1)
        end_date = datetime(year=year, month=month, day=10)
        print(f'月初 {start_date} ~ {end_date}')
        text = text.replace('月初', '月')
        return text
    # 11~20
    elif '月中' in text:
        start_date = datetime(year=year, month=month, day=11)
        end_date = datetime(year=year, month=month, day=20)
        print(f'月中 {start_date} ~ {end_date}')
        text = text.replace('月中', '月')
    # 21~底
    elif '月底' in text:
        start_date = datetime(year=year, month=month, day=21)
        days_in_month = calendar.monthrange(year, month)[1]
        end_date = datetime(year=year, month=month, day=days_in_month)
        print(f'月底 {start_date} ~ {end_date}')
        text = text.replace('月底', '月')
    else:
        return text
def kuan1(text):
    if '年' in text:
        text[:text.index('年')+1]
    # day_period
    # if '月初' in text:

    text = text.replace('年', '年 ').replace('月', '月 ').replace('天', '天 ')


# kuan('我下個月初想要去看比賽')
# kuan('我上上上周去了日本')
kuan('我下個月底的晚上想要去看演唱會')

# '我明年三月底想要去日本'
# '我明天下午三點想要去健身房'
# '明天下午五點之後有哪些演唱會活動?'
# '明天早上十一點之前有哪些演唱會活動?'

test_words = [
    '明年三月十一號晚上八點',
    '明年三月十一號',
    '明年三月',
    '三月十一號晚上八點',
    '三月十一號',
    '三月',
    '十一號晚上八點',
    '十一號',
    '晚上八點'
]
print('---')
for text in test_words:
    if '年' in text and '月' in text and ('日' in text or '號' in text):
        duckling_time = '2025-03-12T20:00:00.000+08:00'
        year_month_day = duckling_time.split('T')[0]
        year = year_month_day.split('-')[0]
        month = year_month_day.split('-')[1]
        day = year_month_day.split('-')[2]
        hour_minutes_seconds_timezone = duckling_time.split('T')[1]
        hour = hour_minutes_seconds_timezone.split(':')[0]
        minutes = hour_minutes_seconds_timezone.split(':')[1]
        print(f'{year}-{month}-{day} {hour}:{minutes}')
    elif '年' in text and '月' in text:
        duckling_time = '2025-03-01T00:00:00.000+08:00'
        year_month_day = duckling_time.split('T')[0]
        year = year_month_day.split('-')[0]
        month = year_month_day.split('-')[1]
        day = year_month_day.split('-')[2]

根據最後一個關鍵字判斷?