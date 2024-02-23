from duckling import *
import re
from datetime import datetime, timedelta
import calendar
from z_test4 import kuannn


def get_until_tags(text):
    tag1 = re.findall(
        r'(year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
        text)
    tag2 = re.findall(
        r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(year|month|week|day|hour|minute|second|range)',
        text)
    return tag1, tag2


texts = kuannn()
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

            time_tags = []
            matched_texts = []
            matched_indexes = []
            matched_time_lines = []

            matches = re.findall(r'(下{2,})周(一|二|三|四|五|六|日)', text)
            for match in matches:
                grain = 'day'
                match_text = f'{match[0]}周{match[1]}'
                print(match_text)

                duckling_result = d.parse_time(f'下周{match[1]}')
                time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00', '')
                time_line = str(
                    datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7 * (len(match[0]) - 1)))
                if match[1] == '六' or match[1] == '日':
                    time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7))

                matched_text_start_index = text.index(match_text)
                matched_text_end_index = matched_text_start_index + len(match_text)
                print(f'{matched_text_start_index}:{matched_text_end_index}')

                time_tags.append(grain)
                matched_time_lines.append([time_line])
                text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                matched_texts.append(match_text)
                matched_indexes.append(matched_text_start_index)

            ''''''

            matches = re.findall(r'(下{2,})周', text)
            for match in matches:
                grain = 'week'
                match_text = f'{match}周'

                duckling_result = d.parse_time(f'下周')
                time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00', '')
                print(time_line)
                time_line = str(
                    datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7 * (len(match) - 1)))
                print(time_line)

                matched_text_start_index = text.index(match_text)
                matched_text_end_index = matched_text_start_index + len(match_text)
                print(f'{matched_text_start_index}:{matched_text_end_index}')

                time_tags.append(grain)
                matched_time_lines.append([time_line])
                text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                matched_texts.append(match_text)
                matched_indexes.append(matched_text_start_index)

            ''''''

            while True:
                duckling_result = d.parse_time(text)
                if duckling_result:
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
                                matched_time_lines.append([str(start_date), str(end_date)])
                                print(f'月初 {start_date} ~ {end_date}')
                            elif '月中' in text:
                                grain = 'range'

                                matched_text = matched_text.replace('月', '月中')

                                start_date = datetime(year=year, month=month, day=11)
                                end_date = datetime(year=year, month=month, day=20, hour=23, minute=59)
                                matched_time_lines.append([str(start_date), str(end_date)])
                                print(f'月中 {start_date} ~ {end_date}')
                            elif '月底' in text:
                                grain = 'range'

                                matched_text = matched_text.replace('月', '月底')

                                start_date = datetime(year=year, month=month, day=21)
                                days_in_month = calendar.monthrange(year, month)[1]
                                end_date = datetime(year=year, month=month, day=days_in_month, hour=23, minute=59)
                                matched_time_lines.append([str(start_date), str(end_date)])
                                print(f'月中 {start_date} ~ {end_date}')
                            else:
                                matched_time_lines.append([time_line])
                        elif grain == 'day' and re.findall(r'下周(?:|六|日)', matched_text):
                            print('hello i am here')
                            time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7))
                            print(time_line)
                            matched_time_lines.append([time_line])
                        else:
                            matched_time_lines.append([time_line])

                        time_tags.append(grain)

                        if grain != 'range':  # test
                            print(f"{matched_text} / {time_line} / {grain}")


                    except Exception as e:
                        grain = 'range'
                        matched_text = str(duckling_result[0]['text'])
                        time_tags.append(grain)

                        print('from', str(duckling_result[0]['value']['value']['from']).replace('T', ' ').replace(
                            ':000+08:00', ''), 'to',
                              str(duckling_result[0]['value']['value']['to']).replace('T', ' ').replace('.000+08:00',
                                                                                                        ''))  # test
                        matched_time_lines.append(
                            [str(duckling_result[0]['value']['value']['from']).replace('T', ' ').replace(
                                '.000+08:00', ''),
                                str(duckling_result[0]['value']['value']['to']).replace('T', ' ').replace(
                                    '.000+08:00', '')])

                    ''''''

                    matched_text_start_index = duckling_result[0]['start']
                    matched_text_end_index = matched_text_start_index + len(matched_text)
                    text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                    matched_texts.append(matched_text)
                    matched_indexes.append(matched_text_start_index)

                    print('matched text:', matched_text)  # test

                else:
                    break

            print(f'c1 經過duckling之後 text = "{text}"')

            ''''''

            # 全部字串處理完畢
            print('@@@@@@@@@@@@@@@字串處理完畢@@@@@@@@@@@@@@@')
            print(f'{ori_msg} -> {pro_msg}')
            sim_msg = text  # test
            print(f'sim msg: {text}')

            sorted_pairs = sorted(zip(matched_indexes, matched_texts))
            # sorted_indexes  = [pair[0] for pair in sorted_pairs]
            matched_texts = [pair[1] for pair in sorted_pairs]

            sorted_pairs = sorted(zip(matched_indexes, time_tags))
            # sorted_indexes  = [pair[0] for pair in sorted_pairs]
            time_tags = [pair[1] for pair in sorted_pairs]

            sorted_pairs = sorted(zip(matched_indexes, matched_time_lines))
            matched_indexes = [pair[0] for pair in sorted_pairs]
            matched_time_lines = [pair[1] for pair in sorted_pairs]

            print('time tags:', time_tags)
            print('matched texts:', matched_texts)
            print('matched texts indexes:', matched_indexes)
            print('matched time lines:', matched_time_lines)

            ''''''

            # 一個接著一個時間段做處理
            while re.findall(r'year|month|week|day|hour|minute|second|range', text):
                matches = re.findall(
                    r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                    text)

                # tag1到tag2
                for match in matches:
                    print('***************處理字串***************')
                    print(f'準備處理字串: "{match}" ({sim_msg})')
                    tag1, tag2 = get_until_tags(match)
                    print(f'until {tag1}, {tag2}')
                    # tag1 的開頭都會是 matched_time_lines[0][0]
                    start_time = matched_time_lines[0][0]
                    start_time_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    # tag2 都取[1][0]
                    end_time = matched_time_lines[1][0]
                    if tag2[0] == 'range':
                        # 但如果是range 就取[1][1]
                        end_time = matched_time_lines[1][1]
                    if tag2[0] == 'year':
                        print('1year')
                        next_year = int(end_time.split('-')[0]) + 1
                        end_time = end_time.replace(end_time.split('-')[0], str(next_year))
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)
                    elif tag2[0] == 'month':
                        print('1month')
                        next_month = int(end_time.split('-')[1]) + 1
                        end_time = end_time.replace(end_time.split('-')[1], str(next_month))
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)
                    elif tag2[0] == 'week':
                        print('1week')
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=7) - timedelta(
                            seconds=1)
                    elif tag2[0] == 'day':
                        print('1day')
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1) - timedelta(
                            seconds=1)
                    else:
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

                    print(f'124 {end_time_obj}')  # test
                    if start_time_obj > end_time_obj:
                        print('你輸入的日期好像怪怪的 你可以再重新輸入一次嗎')
                    else:
                        print(f'篩選 {start_time_obj} <= something <= {end_time_obj}')

                    text = text[text.index(match) + len(match):]
                    print(f'剩餘字串 "{text}"')  # test
                    print('***************處理完成***************')

                    ''' 檢查下一個標籤 '''
                    # 下一個標籤為tag到tag嗎
                    if re.findall(
                            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                            text):
                        next_match = re.findall(
                            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                            text)
                        print('aqa')  # test
                        print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        print(f'>> !1 檢查 "{text[:text.index(next_match[0])]}"')  # test

                        text = text.replace(text[:text.index(next_match[0])], '')
                        # do
                        # 檢查以下這個字串有沒有城市
                        # text[text.index(match) + len(match):text.index(next_match[0])]

                        # print('!1 bef', text)  # test
                        # print('!1 aft', text)  # test
                    # 那是單獨一個tag嗎
                    elif re.findall(r'year|month|week|day|hour|minute|second|range', text):
                        next_match = re.findall(r'year|month|week|day|hour|minute|second|range', text)
                        print('awa')  # test
                        print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        print(f'>> !2 檢查 "{text[:text.index(next_match[0])]}"')  # test

                        text = text.replace(text[:text.index(next_match[0])], '')
                        # do
                        # 檢查以下這個字串有沒有城市
                        # text[text.index(match) + len(match):text.index(next_match[0])]

                        # print('!2 bef', text)  # test
                        # print('!2 aft', text)  # test
                    # 後面沒有tag了
                    else:
                        print(f'match後面的字串，已經沒有標籤了: "{text}"')  # test
                        print(f'>> !3 檢查 "{text}"')
                        # do
                        # 檢查以下字串有沒有城市
                        # text[text.index(match) + len(match):]

                        # print('!3 bef', text)  # test
                        # text = text[text.index(match) + len(match):]
                        # print('!3 aft', text)  # test

                    # text = text.replace(match, '')
                    # print(f'a12 {text}')

                    for i in range(2):
                        del time_tags[0]
                        del matched_texts[0]
                        del matched_indexes[0]
                        del matched_time_lines[0]

                ''''''

                matches = re.findall(r'year|month|week|day|hour|minute|second|range', text)
                # 單獨
                for match in matches:
                    print('***************處理單獨***************')
                    print(f'準備處理字串: "{match}" / {matched_time_lines[0]} / ({sim_msg})')

                    if match == 'range':
                        print('處理range')
                        print(datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S"))
                        print(datetime.strptime(matched_time_lines[0][1], "%Y-%m-%d %H:%M:%S"))
                    elif match == 'year':
                        print('處理year')
                        print(f'year = {datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").year}')
                    elif match == 'month':
                        print('處理month')
                        print(f'month = {datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").month}')
                    elif match == 'week':
                        print('處理week')
                        # print('z1', datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S"))
                        start_time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S")
                        end_time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S") + timedelta(
                            days=7) - timedelta(seconds=1)
                        print('z1')
                        print(start_time_obj)
                        print(end_time_obj)
                    elif match == 'day':
                        print('處理day')
                        print(datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S"))
                    elif match == 'hour' or match == 'minute':
                        print('處理hour or minute')
                        print(datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S"))

                    text = text[text.index(match) + len(match):]
                    print(f'剩餘字串 "{text}"')  # test
                    print('***************處理完成***************')

                    ''' 檢查下一個標籤 '''
                    # 下一個標籤為tag到tag嗎
                    if re.findall(
                            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                            text):
                        next_match = re.findall(
                            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                            text)
                        print('qwe')  # test
                        print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        print(f'>> !3 檢查 "{text[:text.index(next_match[0])]}"')  # test
                        text = text.replace(text[:text.index(next_match[0])], '')
                        print('下一輪的字串', text)

                        # do
                        # 檢查以下這個字串有沒有城市
                        # text[text.index(match) + len(match):text.index(next_match[0])]

                        # print('!4 bef', text)  # test
                        # print('!4 aft', text)  # test
                    # 那是單獨一個tag嗎
                    elif re.findall(r'year|month|week|day|hour|minute|second|range', text):
                        next_match = re.findall(r'year|month|week|day|hour|minute|second|range', text)
                        print('bab')  # test
                        print(next_match)
                        print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        print(f'>> !4 檢查 "{text[:text.index(next_match[0])]}"')  # test

                        text = text.replace(text[:text.index(next_match[0])], '')
                        print('下一輪的字串', text)
                        # do
                        # 檢查以下這個字串有沒有城市
                        # text[text.index(match) + len(match):text.index(next_match[0])]

                        # print('!5 bef', text)  # test
                        # print('!5 aft', text)  # test
                    # 後面沒有tag了
                    else:
                        print(f'match後面的字串，已經沒有標籤了: "{text}"')  # test
                        print(f'>> !6 檢查 "{text}"')
                        # do
                        # 檢查以下字串有沒有城市
                        # text[text.index(match) + len(match):]

                        # print('!3 bef', text)  # test
                        # text = text[text.index(match) + len(match):]
                        # print('!3 aft', text)  # test

                    # text = text[text.index(match):]
                    # if '前' in text and '後' in text:
                    #
                    # print('aza', text)

                    # 起床看一下 接下來要做的是判斷match text後面緊隨其後的是 "前" 還是 "後"

                    # text = text.replace(match, '')

                    del time_tags[0]
                    del matched_texts[0]
                    del matched_indexes[0]
                    del matched_time_lines[0]

            print(
                '------------------------------------------------------------------------------------------------------------------------------------------------')
        except Exception as e:
            print('!!!')
            print(f'{text} have error: {e}')
            print(
                '------------------------------------------------------------------------------------------------------------------------------------------------')
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


conversation()
