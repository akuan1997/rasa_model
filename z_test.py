from duckling import *
import re
from datetime import datetime
import calendar

texts = [
    '我們十一點半見',
    '前天的下午三點之前',
    '下周',
    # '下下周',  #
    # '兩周後',  #
    # '上週',  #
    # '上上周',  #
    # '下下周 周五',  #
    # '兩周後 周五',  #
    # '兩周後的今天',  #
    # '兩周後的週四',  #
    '下個月初',
    '下個月中',
    '下個月底',
    '下周日晚上',
    '下個月初有什麼演唱會',
    '每周一',
    '十一月九號的晚上',
    '明天的下午茶時間有什麼演唱會嗎',
    '十月 一號 早上 到十月五號 晚上',
    '周末',
    '這個月',
    '這個月初',
    '這個月中',
    '這個月底',
    '月初',
    '月中',
    '月底',
    '下個月',
    '下月',
    '十一月初',
    '我下個月 想要去看演唱會',
    '十月 十號到十月 十五號',
    '明年 三月 ',
    '明天 下午五點之後有哪些演唱會活動?',
    '明天 早上十一點之前有哪些演唱會活動?',
    '後天中午十二時',
    '後天中午十二點',
    # '明年三月的',
    # '明年三月十一號',
    # '明年三月十二日晚上8點',
    '十一點半',
    '十一點',
    '三月十一日',
    '三月十二日晚上8點',
    '三月',
    '三月 七月 八月的晚上',
    '三月、七月和八月的晚上',
    '七月一號 還有八月的晚上',
    '一月一號到一月五號',
    '一月一號到一月五號中間',
    '一月一號下午到一月三號晚上',
    '一月一號到一月五號之間 八月',
    '一月一號到五號的晚上',
    '三月一號和二號的晚上',
    '明年三月到五月',
    '明天下午和後天',
    '明天和後天晚上',
    '明天下午到後天',
    '明天到後天下午',
    '十月初還有十一月初有什麼演唱會'
]

wrong_words = [
    '下個月初的晚上有什麼演唱會',
    '下下周的周五',
    '下午茶',  # 改為下午
    '每個月的15號',
]


def conversation():
    d = DucklingWrapper(language=Language.CHINESE)
    for text in texts:
        print('ori msg', text)
        ori_msg = text

        try:
            text = replace_week(text)
            text = text.replace('的', '')
            text = text.replace('下午茶', '下午')

            if '寒假' in text:
                print('每一年的寒假時間都是不固定的，我將為你搜尋一月以及二月相關的活動')
                text = text.replace('寒假', '一月 二月')
            if '暑假' in text:
                print('每一年的暑假時間都是不固定的，我將為你搜尋七月以及八月相關的活動')
                text = text.replace('暑假', '七月 八月')

            text = text.replace('春季', '春天').replace('春天', '三月 四月 五月')
            text = text.replace('夏季', '夏天').replace('夏天', '六月 七月 八月')
            text = text.replace('秋季', '秋天').replace('秋天', '九月 十月 十一月')
            text = text.replace('冬季', '冬天').replace('冬天', '十二月 一月 二月')

            text = re.sub(r'明年([十]?[一二三四五六七八九十])月\s*和\s*([十]?[一二三四五六七八九十])月',
                          r'明年\1月和明年\2月', text)
            text = re.sub(r'明年([十]?[一二三四五六七八九十])月\s*到\s*([十]?[一二三四五六七八九十])月',
                          r'明年\1月到明年\2月', text)

            text = re.sub(r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])日', r'\1月\2號',
                          text)

            text = re.sub(
                r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*到\s*([一二三]?[十]?[一二三四五六七八九十])號',
                r'\1月\2號到\1月\3號', text)
            text = re.sub(
                r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*和\s*([一二三]?[十]?[一二三四五六七八九十])號',
                r'\1月\2號到\1月\3號', text)

            print('pro msg', text)
            pro_msg = text

            matched_texts = []
            time_tags = []
            matched_texts_indexes = []
            while True:
                duckling_result = d.parse_time(text)
                if duckling_result:
                    # print(duckling_result[0])
                    try:
                        grain = duckling_result[0]['value']['grain']
                        time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00',
                                                                                                        '')
                        matched_text = str(duckling_result[0]['text'])

                        if grain == 'month':
                            year = int(time_line.split('-')[0])
                            month = int(time_line.split('-')[1])
                            if '月初' in text:
                                grain = 'range'

                                matched_text = matched_text.replace('月', '月初')

                                start_date = datetime(year=year, month=month, day=1)
                                end_date = datetime(year=year, month=month, day=10, hour=23, minute=59)
                                print(f'月初 {start_date} ~ {end_date}')
                            elif '月中' in text:
                                grain = 'range'

                                matched_text = matched_text.replace('月', '月中')

                                start_date = datetime(year=year, month=month, day=11)
                                end_date = datetime(year=year, month=month, day=20, hour=23, minute=59)
                                print(f'月中 {start_date} ~ {end_date}')
                            elif '月底' in text:
                                grain = 'range'

                                matched_text = matched_text.replace('月', '月底')

                                start_date = datetime(year=year, month=month, day=21)
                                days_in_month = calendar.monthrange(year, month)[1]
                                end_date = datetime(year=year, month=month, day=days_in_month, hour=23, minute=59)
                                print(f'月中 {start_date} ~ {end_date}')
                            else:
                                pass
                        elif grain == 'week':
                            pass
                        elif grain == 'day':
                            pass
                        elif grain == 'hour':
                            pass
                        elif grain == 'minute':
                            pass
                        elif grain == 'second':
                            pass

                        time_tags.append(grain)

                        if grain != 'range':  # test
                            print(f"{matched_text} / {time_line} / {grain}")

                    except Exception as e:
                        grain = 'range'
                        matched_text = str(duckling_result[0]['text'])
                        time_tags.append(grain)

                        print('from', str(duckling_result[0]['value']['value']['from']).replace('T', ' ').replace(
                            ':00.000+08:00', ''), 'to',
                              str(duckling_result[0]['value']['value']['to']).replace('T', ' ').replace(':00.000+08:00',
                                                                                                        ''))  # test

                    matched_text_start_index = duckling_result[0]['start']
                    matched_text_end_index = matched_text_start_index + len(matched_text)
                    text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                    matched_texts.append(matched_text)
                    matched_texts_indexes.append(matched_text_start_index)

                    print('matched text:', matched_text)  # test

                else:
                    break

            # if not matched_texts:
            #     if '下下周' in text:
            #         print('我等等處理你')

            # 全部字串處理完畢
            print('!!!')
            print(f'{ori_msg} -> {pro_msg}')
            # print(f'pro msg: {pro_msg}')
            print(f'sim msg: {text}')
            sorted_pairs = sorted(zip(matched_texts_indexes, matched_texts))
            # sorted_indexes  = [pair[0] for pair in sorted_pairs]
            matched_texts = [pair[1] for pair in sorted_pairs]

            sorted_pairs = sorted(zip(matched_texts_indexes, time_tags))
            matched_texts_indexes = [pair[0] for pair in sorted_pairs]
            time_tags = [pair[1] for pair in sorted_pairs]

            print('time tags:', time_tags)
            print('matched texts:', matched_texts)
            print('matched texts indexes:', matched_texts_indexes)

            # if len(time_tags) == 1 and time_tags[0] != 'range':
            #     if '前' in text:
            #         print(f'< {time_tags[0]}')
            #     elif '後' in text:
            #         print(f'> {time_tags[0]}')
            #     else:
            #         print(f'= {time_tags[0]}')
            # elif len(time_tags) == 1 and time_tags[0] == 'week':
            #     print('for loop, if week == week')
            # elif len(time_tags) == 1 and time_tags[0] == 'range':
            #     print(f'RANGE')
            print('------------------------------------------------------------------------')
        except Exception as e:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(f'{text} have error: {e}')
            print('---')
            continue


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
    '明年三月和五月',
    '明年三月到五月之間',
    '今年八月和九月',
    '今年 八月 九月 十月'
]


def replace_week(text):
    text = text.replace('週', '周').replace('星期天', '星期日').replace('禮拜天', '禮拜日').replace('星期',
                                                                                                    '周').replace(
        '禮拜', '周')
    return text


def conversation1():
    d = DucklingWrapper(language=Language.CHINESE)
    for text in test_words:
        if '今年' in text:
            text = text.replace('今年', '')
        elif '明年' in text:
            text = text.replace('明年', '')
        try:
            text = replace_week(text)
            text = text.replace('下午茶', '下午')
            # replace('的', '').\
            print('ori msg', text)

            matched_texts = []
            while True:
                duckling_result = d.parse_time(text)
                if duckling_result:
                    print(duckling_result[0])
                    print(duckling_result[0]['value']['value'])
                    # 範圍
                    try:
                        if duckling_result[0]['value']['value']['to']:
                            print('hello')
                    # 沒有範圍
                    except:
                        pass
                    text = text.replace(text[duckling_result[0]['start']:duckling_result[0]['end']], '')
                    matched_texts.append(duckling_result[0]['text'])
                    # if len(matched_texts) == 1 and (matched_texts[0] == '下周' or matched_texts[0] == '下星期' or matched_texts[0] == '下禮拜'):
                    # print()
                else:
                    break
            print(f'duckling配對到{len(matched_texts)}個')
            print(matched_texts)
            print('---')
        except Exception as e:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(f'{text} have error: {e}')
            print('---')
            continue


conversation()
# conversation1()

# for word in test_words:
#     current_datetime = datetime.now()
#     year = current_datetime.year
#     month = current_datetime.month
#     day = current_datetime.day
#
#     week = int(current_datetime.strftime("%U"))
#     print(f'{year}-{month}-{day} / {year}的第{week}周')
#
#     print(word)
#
#     if '今年' in word:
#         word = word.replace('今年', '')
#         last_keyword = year
#     elif '明年' in word:
#         year = year + 1
#         word = word.replace('明年', '')
#         last_keyword = year
#
#     print(word)
#
#     word = word.replace('與', '和')
#     word = word.replace('號', '日')
#     if '和' in word:
#         word_splits = word.split('和')
#         for word_split in word_splits:
#             print(word_split)
#     print('---')
