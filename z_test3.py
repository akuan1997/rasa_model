from datetime import datetime, timedelta
import re

from duckling import *

d = DucklingWrapper(language=Language.CHINESE)

test_words = [
    '明年三月十一號晚上八點',
    '明年三月十一號',
    '明年三月',
    '三月十一號晚上八點',
    '三月十一號',
    '三月',
    '十一號晚上八點',
    '十一號',
    '晚上八點',
    '2024-10-5 20:00',
    '九月的晚上和十月的下午',
    '九月晚上和十月下午',
    '十月和十一月的下午',
    '十一月和十二月 晚上八點之後',
    '十一月和十二月的晚上八點之後',
    '十一月八號晚上九點到十一點之間',
    '十一月八號 晚上九點到十一點之間',
    '下禮拜一',
    '三月和五月',
    '三月到五月之間'
]

test_words1 = [
    '今年和明年',
    '今年與明年',
    '今年 明年',
    '今年',
    '今年五月和七月',
    '明年十月和十一月',
    '今年十一月 十二月 明年一月',
    '一月和二月',
    '一月和三月和七月',
    '二月 三月 七月',
    '四月 五月 和八月',
    '2025年有什麼演唱會嗎'
]

for word in test_words1:
    current_datetime = datetime.now()
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day
    week = int(current_datetime.strftime("%U"))

    next_year_index = -1
    next_year_line = ''
    this_year_line = ''

    if '去年' in word \
            or '前年' in word \
            or '上周' in word \
            or '周前' in word \
            or '昨天' in word \
            or '前天' in word \
            or '天前' in word:
        print('不好意思 我們查詢過去的時間')
    else:
        print(word)
        # 明年
        if word.find('明年') != -1 or word.find(str(year + 1)) != -1:
            if word.find('明年') != -1:
                next_year_line = word[word.find('明年'):].replace('明年', '')
                next_year_index = word.find('明年')
            else:
                next_year_line = word[word.find(str(year + 1)):].replace(str(year + 1), '')
                next_year_index = word.find(str(year + 1))
            # duckling_result = d.parse_time(next_year_line)
            # print(duckling_result)

        # 今年
        if next_year_index == -1:
            this_year_line = word.replace('今年', '')
        else:
            this_year_line = word[:next_year_index].replace('今年', '')

        print('今年字串:', this_year_line)
        print('明年字串:', next_year_line)
        # duckling_result = d.parse_time(this_year_line)
        # print(duckling_result)

        # if str(year + 1) in word:
        #     year = year + 1
        # elif str(year) in word:
        #     year = year
        # else:
        # year = year
        print('---')
        # this_year = word[:word.find('明年')]
        # print(this_year)

        # word = word.replace('與', '和')
        # splits = word.split('和')
        # print(word)
        # last_keyword = []
        # for split in splits:
        #     if '年' in split:
        #         last_keyword.append('year')
        #     elif '月' in split:
        #         last_keyword.append('month')
        #     elif '號' in split:
        #         last_keyword.append('day')
        #     print(last_keyword)
        #     print(split)
        # print('---')
        # # if '今年' in word:
        # #
        # # year_index = word.find('今年')
        # #
        # # print(word)
# text = "我晚上想要去健身。明天晚上八点想要去走路。晚上去看电影。"
#
# 检查文本中是否有晚上后面没有接时间的情况，并替换掉
# text = re.sub(r'(晚上)(?![0-9])', '', text)
#
# print(text)
#
#
texts = ['二月一號到十號', '二月十一號到二十號', '二月二十一號到三十一號', '三月三十一號']
texts1 = ['十月 一日 十月二日']
for text in texts:
    text = re.sub(
        r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*到\s*([一二三]?[十]?[一二三四五六七八九十])號',
        r'\1月\2號到\1月\3號', text)
    text = re.sub(
        r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*和\s*([一二三]?[十]?[一二三四五六七八九十])號',
        r'\1月\2號到\1月\3號', text)
    print(text)
# match = re.findall(
#     r'[十]?[一二三四五六七八九十]月\s*[一二三]?[一二三四五六七八九十]號\s*到\s*[一二三]?[一二三四五六七八九十]號', text)
# print(match)
for text in texts1:
    text = re.sub(r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])日', r'\1月\2號', text)
    print(text)

# text1 = ["我感覺很喜歡 OK", "我真的很喜歡 OK", "我感到很喜歡 OK", '我喜歡']
# for text in text1:
#     match = re.findall(r'我.*?喜歡', text)
#     print(match)

# 幾周後的周幾 X
# 幾周後周幾 X
# 下下周 X
# 下周 OK
# 下周一 下周二 OK
# 上周 or 幾周前 不動作

text2 = ['明年三月和四月有什麼演唱會嗎', '今年三月和明年四月']
for text in text2:
    text = re.sub(r'明年([十]?[一二三四五六七八九十])月\s*和\s*([十]?[一二三四五六七八九十])月', r'明年\1月和明年\2月',
                  text)
    print(text)


def sort_index(matched_indexes, matched_texts):
    sorted_pairs = sorted(zip(matched_indexes, matched_texts))
    matched_indexes = [pair[0] for pair in sorted_pairs]
    matched_texts = [pair[1] for pair in sorted_pairs]

    return matched_indexes, matched_texts


# text = 'year到range'
# matched = []
# matches = re.findall(r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)', text)
# for match in matches:
#     tag1 = re.findall(r'((?:year|month|week|day|hour|minute|second|range)).*?到.*?(?:year|month|week|day|hour|minute|second|range)',text)
#     tag2 = re.findall(r'(?:year|month|week|day|hour|minute|second|range).*?到.*?((?:year|month|week|day|hour|minute|second|range))',text)
#     print('until tag1', tag1)
#     print('until tag2', tag2)
#     text = text.replace(match, '')
#     matched.append(match)
# matches = re.findall(r'year|month|week|day|hour|minute|second|range', text)
# for match in matches:
#     text = text.replace(match, '')
#     matched.append(match)
# print(matched)

# matches = re.findall(r'(?:year|month|week|day|hour|minute|second|range)到(?:year|month|week|day|hour|minute|second|range)', text)
# matches = re.findall(r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)|\b(?:year|month|week|day|hour|minute|second|range)\b', text)
# matches = re.findall(r'(?:year|month|week|day|hour|minute|second|range).*?(?:到|\b)(?:year|month|week|day|hour|minute|second|range)|\b(?:year|month|week|day|hour|minute|second|range)\b', text)

# text = '123'
# match = re.findall(r'year|month|week|day|hour|minute|second|range', text)
# print(match)
def get_until_tags(text):
    tag1 = re.findall(
        r'(year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
        text)
    tag2 = re.findall(
        r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(year|month|week|day|hour|minute|second|range)',
        text)
    return tag1, tag2


text = "這是一個測試，我們要匹配year直到day、hour到range、week到second等 或是簡單的week hour 也是沒問題的。"
while re.findall(r'year|month|week|day|hour|minute|second|range', text):
    matches = re.findall(
        r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
        text)
    # tag到tag
    for match in matches:
        print(match)
        tag1, tag2 = get_until_tags(match)
        print(f'until {tag1}, {tag2}')
        text = text.replace(match, '')
        # search_tags.append(match)
    matches = re.findall(r'year|month|week|day|hour|minute|second|range', text)
    # 單獨
    for match in matches:
        print(match)
        text = text.replace(match, '')

start_time_str = "2024-02-22 00:00:00"
end_time_str = "2024-02-23 00:00:00"
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
print(start_time)
print(end_time)
if start_time < end_time:
    print('okay')
    # if start_time < target

# 寫一個function 把下周六轉換成中文字

# a = datetime(2024, 10, 1, 0, 0)
# b = a - timedelta(seconds=1)
# print(b)
# a.year = a.year + 1
# print(a)

a = ' '
print(f'"{a.strip()}"')

a = '下周日'
b = re.findall(r'下周(?:一|二|三|四|五|六|日)', a)
print(b)

# b = re.findall(r'下下周(?:一|二|三|四|五|六|日)', a)
# print(b)

time_tags = []
matched_texts = []
matched_indexes = []
matched_time_lines = []

text = '下下周一 下下下周三 下下周六 下下周'
sim_text = text
matches = re.findall(r'(下{2,})周(一|二|三|四|五|六|日)', sim_text)
for match in matches:
    grain = 'day'
    print(f'下周{match[1]}')
    duckling_result = d.parse_time(f'下周{match[1]}')
    time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00', '')
    time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7 * (len(match[0]) - 1)))
    if match[1] == '六' or match[1] == '日':
        time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7))
    match_text = f'{match[0]}周{match[1]}'

    matched_text_start_index = text.index(match_text)
    matched_text_end_index = matched_text_start_index + len(match_text)
    print(f'{matched_text_start_index}:{matched_text_end_index}')

    time_tags.append(grain)
    matched_time_lines.append([time_line])
    sim_text = sim_text.replace(text[matched_text_start_index:matched_text_end_index], grain)
    matched_texts.append(match_text)
    matched_indexes.append(matched_text_start_index)

    print('time tags:', time_tags)
    print('matched texts:', matched_texts)
    print('matched texts indexes:', matched_indexes)
    print('matched time lines:', matched_time_lines)
    print(text)
    print(sim_text)

print('time tags:', time_tags)
print('matched texts:', matched_texts)
print('matched texts indexes:', matched_indexes)
print('matched time lines:', matched_time_lines)
