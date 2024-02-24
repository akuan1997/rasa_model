from duckling import *
import re
from datetime import datetime, timedelta
import calendar
from z_test4 import kuannn
import json

zh_cities = ['雲林', '連江', '台南', '花蓮', '屏東', '高雄',
          '彰化', '新竹', '台中', '桃園', '金門', '宜蘭',
          '澎湖', '新北', '苗栗', '南投', '基隆', '台東',
          '嘉義', '台北']

with open('concert.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

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
        ori_msg = text  # 原始字串

        try:
            text = text_replacement(text)

            pro_msg = text  # 經過處理之後的字串

            time_tags = []
            matched_texts = []
            matched_indexes = []
            matched_time_lines = []

            # 下下周一、下下周二 ...
            matches = re.findall(r'(下{2,})周(一|二|三|四|五|六|日)', text)
            for match in matches:
                grain = 'day'
                match_text = f'{match[0]}周{match[1]}'

                duckling_result = d.parse_time(f'下周{match[1]}')
                time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00', '')
                time_line = str(
                    datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7 * (len(match[0]) - 1)))
                if match[1] == '六' or match[1] == '日':
                    time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7))

                matched_text_start_index = text.index(match_text)
                matched_text_end_index = matched_text_start_index + len(match_text)

                time_tags.append(grain)
                matched_time_lines.append([time_line])
                text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                matched_texts.append(match_text)
                matched_indexes.append(matched_text_start_index)

            ''''''

            # 下下周、下下下周 ...
            matches = re.findall(r'(下{2,})周', text)
            for match in matches:
                grain = 'week'
                match_text = f'{match}周'

                duckling_result = d.parse_time(f'下周')
                time_line = str(duckling_result[0]['value']['value']).replace('T', ' ').replace('.000+08:00', '')
                time_line = str(
                    datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7 * (len(match) - 1)))

                matched_text_start_index = text.index(match_text)
                matched_text_end_index = matched_text_start_index + len(match_text)

                time_tags.append(grain)
                matched_time_lines.append([time_line])
                text = text.replace(text[matched_text_start_index:matched_text_end_index], grain)
                matched_texts.append(match_text)
                matched_indexes.append(matched_text_start_index)

            ''''''

            # duckling可判斷的範圍 / 處理完畢之後會變成簡化的字串
            # range到range有哪些演唱會、請問day有什麼演唱會 ...
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
                        elif grain == 'day' and re.findall(r'下周(?:六|日)', matched_text):
                            time_line = str(datetime.strptime(time_line, "%Y-%m-%d %H:%M:%S") + timedelta(days=7))
                            matched_time_lines.append([time_line])
                        else:
                            matched_time_lines.append([time_line])

                        time_tags.append(grain)

                        # if grain != 'range':  # test
                        #     print(f"{matched_text} / {time_line} / {grain}")


                    except Exception as e:
                        grain = 'range'
                        matched_text = str(duckling_result[0]['text'])
                        time_tags.append(grain)

                        # print('from', str(duckling_result[0]['value']['value']['from']).replace('T', ' ').replace(
                        #     ':000+08:00', ''), 'to',
                        #       str(duckling_result[0]['value']['value']['to']).replace('T', ' ').replace('.000+08:00',
                        #                                                                                 ''))  # test
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

                    # print('matched text:', matched_text)  # test

                else:
                    break

            ''''''

            # 字串處理完畢 / 把日期按照字串的順序排列
            print(f'原始字串 {ori_msg}')
            print(f'經過處理後 -> {pro_msg}')
            print(f'字串簡化完成 - {text}')

            sorted_pairs = sorted(zip(matched_indexes, matched_texts))
            # sorted_indexes  = [pair[0] for pair in sorted_pairs]
            matched_texts = [pair[1] for pair in sorted_pairs]

            sorted_pairs = sorted(zip(matched_indexes, time_tags))
            # sorted_indexes  = [pair[0] for pair in sorted_pairs]
            time_tags = [pair[1] for pair in sorted_pairs]

            sorted_pairs = sorted(zip(matched_indexes, matched_time_lines))
            matched_indexes = [pair[0] for pair in sorted_pairs]
            matched_time_lines = [pair[1] for pair in sorted_pairs]

            print(f'---\ntime tags: {time_tags}')
            print(f'matched texts: {matched_texts}')
            print(f'matched texts indexes: {matched_indexes}')
            print(f'matched time lines: {matched_time_lines}\n---')

            ''''''
            show_info_indexes = []
            # tag by tag 處理
            while re.findall(r'year|month|week|day|hour|minute|second|range', text):
                matches = re.findall(
                    r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                    text)
                concert_indexes = []

                # tag1到tag2
                for match in matches:
                    print(f'>> 處理期間 {match}')
                    # 鼠標往後移動到tag結束
                    text = text[text.index(match) + len(match):]
                    # 取得要檢查城市的字串 並把數標移動到下一個標籤之前
                    check_text, text = next_tag(text)

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
                        next_year = int(end_time.split('-')[0]) + 1
                        end_time = end_time.replace(end_time.split('-')[0], str(next_year))
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)
                    elif tag2[0] == 'month':
                        next_month = int(end_time.split('-')[1]) + 1
                        end_time = end_time.replace(end_time.split('-')[1], str(next_month))
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=1)
                    elif tag2[0] == 'week':
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=7) - timedelta(
                            seconds=1)
                    elif tag2[0] == 'day':
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") + timedelta(days=1) - timedelta(
                            seconds=1)
                    else:
                        end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

                    if start_time_obj > end_time_obj:
                        print('你輸入的日期好像怪怪的 你可以再重新輸入一次嗎')
                    else:
                        print(f'篩選 {start_time_obj} <= something <= {end_time_obj}')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                if start_time_obj <= pdt_obj <= end_time_obj:
                                    # print(f'發現! {pdt_obj}')
                                    concert_indexes.append(i)
                            # else:
                            #     print('有~ 後面再處理')

                    # # 期間的tag處理完成 鼠標往後移動到tag結束
                    # text = text[text.index(match) + len(match):]

                    if concert_indexes:
                        print(f'符合時間段: {concert_indexes}')
                        print(f'>> 檢查"{check_text}"有無城市')
                        city_indexes = get_city_indexes(check_text)
                        if not city_indexes:
                            for concert_index in concert_indexes:
                                show_info_indexes.append(concert_index)
                        else:
                            for concert_index in concert_indexes:
                                for city_index in city_indexes:
                                    if city_index == concert_index:
                                        show_info_indexes.append(city_index)
                        print(list(set(show_info_indexes)))
                        print(f'---\n剩餘字串 "{text}"\n---')
                        # check_text, text = next_tag(text)
                        # for index in concert_indexes
                        # 得到 "標籤~下一個標籤之前" 的字串
                        # 檢查有沒有城市
                        # if data[index]['cit'] == '某個city' or data[index]['cit'] == '某個city'
                        #   show_info_indexes.append(index)
                        # ''' 檢查下一個標籤 '''
                        # # 下一個標籤為tag到tag嗎
                        # if re.findall(
                        #         r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                        #         text):
                        #     next_match = re.findall(
                        #         r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
                        #         text)
                        #     print('aqa')  # test
                        #     print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        #     check_text = text[:text.index(next_match[0])]
                        #     print(f'>> 檢查"{check_text}"有無城市')
                        #     # do
                        #     text = text.replace(text[:text.index(next_match[0])], '')
                        #     print(f'---\n下一輪的字串 "{text}"')
                        #     # print(f'>> !1 檢查 "{check_text}" 有無城市')  # test
                        #     # do
                        #     # 檢查以下這個字串有沒有城市
                        #     # text[text.index(match) + len(match):text.index(next_match[0])]
                        #
                        #     # print('!1 bef', text)  # test
                        #     # print('!1 aft', text)  # test
                        # # 那是單獨一個tag嗎
                        # elif re.findall(r'year|month|week|day|hour|minute|second|range', text):
                        #     next_match = re.findall(r'year|month|week|day|hour|minute|second|range', text)
                        #     print('awa')  # test
                        #     print(f'{next_match[0]}, start at index {text.index(next_match[0])}')  # test
                        #     check_text = text[:text.index(next_match[0])]
                        #     print(f'>> 檢查"{check_text}"有無城市')
                        #     # do
                        #     text = text.replace(text[:text.index(next_match[0])], '')
                        #     print(f'---\n下一輪的字串 "{text}"')
                        #     # print(f'---\n下一輪的字串 {text}')
                        #     # print(f'>> !2 檢查 "{check_text}" 有無城市')  # test
                        #     # do
                        #     # 檢查以下這個字串有沒有城市
                        #     # text[text.index(match) + len(match):text.index(next_match[0])]
                        #
                        #     # print('!2 bef', text)  # test
                        #     # print('!2 aft', text)  # test
                        # # 後面沒有tag了
                        # else:
                        #     print(f'range to range 3')  # test
                        #     print(f'>> 檢查 {text} 有無城市')
                        #     # do
                    else:
                        print('沒有符合的時間段')

                    for i in range(2):
                        del time_tags[0]
                        del matched_texts[0]
                        del matched_indexes[0]
                        del matched_time_lines[0]

                ''''''

                matches = re.findall(r'year|month|week|day|hour|minute|second|range', text)
                # 單獨
                for match in matches:
                    print(f'>> 開始處理單獨標籤: {match}')
                    # print(f'準備處理字串: "{match}" / {matched_time_lines[0]} / ({sim_msg})')
                    text = text[text.index(match) + len(match):]
                    check_text, text = next_tag(text)
                    concert_indexes = []
                    if match == 'range':
                        print('function range')
                        start_time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S")
                        end_time_obj = datetime.strptime(matched_time_lines[0][1], "%Y-%m-%d %H:%M:%S")

                        if start_time_obj > end_time_obj:
                            print('你輸入的日期好像怪怪的 如果有錯誤的話麻煩再輸入一次')
                        else:
                            print(f'篩選 {start_time_obj} <= something <= {end_time_obj}')
                            for i in range(len(data)):
                                if '~' not in data[i]['pdt'][0]:
                                    pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                    if start_time_obj <= pdt_obj <= end_time_obj:
                                        # print(f'發現! {pdt_obj}')
                                        concert_indexes.append(i)
                                    # else:
                                    #     print('有~ 後面再處理')
                            if concert_indexes:
                                print(f'符合時間段: {concert_indexes}')
                                print(f'>> 檢查"{check_text}" 有無城市')
                                city_indexes = get_city_indexes(check_text)
                                if not city_indexes:
                                    for concert_index in concert_indexes:
                                        show_info_indexes.append(concert_index)
                                else:
                                    for concert_index in concert_indexes:
                                        for city_index in city_indexes:
                                            if city_index == concert_index:
                                                show_info_indexes.append(city_index)
                                print(list(set(show_info_indexes)))

                    elif match == 'year':
                        single_year = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").year
                        print('function year')
                        print(f'year = {single_year}')

                        print(f'>> 檢查 "{check_text}" 有無城市以及前後')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                if '前' in check_text and '後' in check_text:
                                    print('不好意思，請問你想要搜尋是前、後還是一整年')
                                elif '前' in check_text:
                                    if pdt_obj.year < single_year:
                                        concert_indexes.append(i)
                                elif '後' in check_text:
                                    if pdt_obj.year > single_year:
                                        concert_indexes.append(i)
                                else:
                                    if pdt_obj.year == single_year:
                                        concert_indexes.append(i)
                            # else:
                            #     print('有~ 稍後我再處理')

                        if concert_indexes:
                            print('single tag - year', concert_indexes)
                            city_indexes = get_city_indexes(check_text)
                            if not city_indexes:
                                for concert_index in concert_indexes:
                                    show_info_indexes.append(concert_index)
                            else:
                                for concert_index in concert_indexes:
                                    for city_index in city_indexes:
                                        if city_index == concert_index:
                                            show_info_indexes.append(city_index)
                            print(list(set(show_info_indexes)))
                        else:
                            print('沒有找到匹配的資料')

                    elif match == 'month':
                        single_month = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").month
                        print('function month')
                        print(f'month = {single_month}')

                        print(f'>> 檢查 "{check_text}" 有無城市或前後')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                if '前' in check_text and '後' in check_text:
                                    print('不好意思，請問你想要搜尋是前、後還是一整個月')
                                elif '前' in check_text:
                                    if pdt_obj.month < single_month:
                                        concert_indexes.append(i)
                                elif '後' in check_text:
                                    if pdt_obj.month > single_month:
                                        concert_indexes.append(i)
                                else:
                                    if pdt_obj.month == single_month:
                                        concert_indexes.append(i)
                            # else:
                            #     print('有~ 稍後我再處理')

                        if concert_indexes:
                            print('single tag - month', concert_indexes)
                            city_indexes = get_city_indexes(check_text)
                            if not city_indexes:
                                for concert_index in concert_indexes:
                                    show_info_indexes.append(concert_index)
                            else:
                                for concert_index in concert_indexes:
                                    for city_index in city_indexes:
                                        if city_index == concert_index:
                                            show_info_indexes.append(city_index)
                            print(list(set(show_info_indexes)))
                        else:
                            print('沒有找到匹配的資料')

                    elif match == 'week':
                        single_week = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").isocalendar()[1]
                        print('function week')
                        # print(f'week = {single_week}')

                        print(f'>> 檢查 "{check_text}" 有無城市或前後')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                pdt_week = pdt_obj.isocalendar()[1]
                                # print(f'pdt week = {pdt_week}')
                                if '前' in check_text and '後' in check_text:
                                    print('不好意思，請問你想要搜尋是前、後還是一整周')
                                elif '前' in check_text:
                                    if pdt_week < single_week:
                                        concert_indexes.append(i)
                                elif '後' in check_text:
                                    if pdt_week > single_week:
                                        concert_indexes.append(i)
                                else:
                                    if pdt_week == single_week:
                                        concert_indexes.append(i)
                            # else:
                            #     print('有~ 稍後我再處理')

                        if concert_indexes:
                            print('single tag - week', concert_indexes)
                            city_indexes = get_city_indexes(check_text)
                            if not city_indexes:
                                for concert_index in concert_indexes:
                                    show_info_indexes.append(concert_index)
                            else:
                                for concert_index in concert_indexes:
                                    for city_index in city_indexes:
                                        if city_index == concert_index:
                                            show_info_indexes.append(city_index)
                            print(list(set(show_info_indexes)))
                        else:
                            print('沒有找到匹配的資料')

                        # # print('z1', datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S"))
                        # start_time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S")
                        # end_time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S") + timedelta(
                        #     days=7) - timedelta(seconds=1)
                        # print('z1')
                        # print(start_time_obj)
                        # print(end_time_obj)

                    elif match == 'day':
                        single_day = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S").day
                        print('function day')
                        print(f'day = {single_day}')

                        print(f'>> 檢查 "{check_text}" 有無城市或前後')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                if '前' in check_text and '後' in check_text:
                                    print('不好意思，請問你想要搜尋是前、後還是一整天')
                                elif '前' in check_text:
                                    if pdt_obj.day < single_day:
                                        concert_indexes.append(i)
                                elif '後' in check_text:
                                    if pdt_obj.day > single_day:
                                        concert_indexes.append(i)
                                else:
                                    if pdt_obj.day == single_day:
                                        concert_indexes.append(i)
                            # else:
                            #     print('有~ 稍後我再處理')

                        if concert_indexes:
                            print('single tag - day', concert_indexes)
                            city_indexes = get_city_indexes(check_text)
                            if not city_indexes:
                                for concert_index in concert_indexes:
                                    show_info_indexes.append(concert_index)
                            else:
                                for concert_index in concert_indexes:
                                    for city_index in city_indexes:
                                        if city_index == concert_index:
                                            show_info_indexes.append(city_index)
                            print(list(set(show_info_indexes)))
                        else:
                            print('沒有找到匹配的資料')

                    elif match == 'hour' or match == 'minute':
                        time_obj = datetime.strptime(matched_time_lines[0][0], "%Y-%m-%d %H:%M:%S")
                        print('function hour or function minute')
                        print(f'hour or minute = {time_obj}')

                        print(f'>> 檢查 "{check_text}" 有無城市或前後')
                        for i in range(len(data)):
                            if '~' not in data[i]['pdt'][0]:
                                pdt_obj = datetime.strptime(data[i]['pdt'][0], "%Y/%m/%d %H:%M")
                                if '前' in check_text and '後' in check_text:
                                    print('不好意思，請問你想要搜尋是前還是後')
                                elif '前' in check_text:
                                    if pdt_obj < time_obj:
                                        concert_indexes.append(i)
                                elif '後' in check_text:
                                    if pdt_obj > time_obj:
                                        concert_indexes.append(i)
                                else:
                                    if pdt_obj == time_obj:
                                        concert_indexes.append(i)
                            # else:
                            #     print('有~ 稍後我再處理')

                        if concert_indexes:
                            print('single tag - hour | minute', concert_indexes)
                            city_indexes = get_city_indexes(check_text)
                            if not city_indexes:
                                for concert_index in concert_indexes:
                                    show_info_indexes.append(concert_index)
                            else:
                                for concert_index in concert_indexes:
                                    for city_index in city_indexes:
                                        if city_index == concert_index:
                                            show_info_indexes.append(city_index)
                            print(list(set(show_info_indexes)))
                        else:
                            print('沒有找到匹配的資料')

                    print(f'---\n剩餘字串 "{text}"\n---')

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


def month_arabic_to_zh(match):
    num_map = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
               '10': '十', '11': '十一', '12': '十二'}
    num = match.group(1)

    return num_map[num] + '月'


def day_arabic_to_zh(match):
    num_map = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
               '10': '十', '11': '十一', '12': '十二', '13': '十三', '14': '十四', '15': '十五', '16': '十六',
               '17': '十七', '18': '十八', '19': '十九', '20': '二十', '21': '二十一', '22': '二十二', '23': '二十三',
               '24': '二十四', '25': '二十五', '26': '二十六', '27': '二十七', '28': '二十八', '29': '二十九',
               '30': '三十', '31': '三十一'}
    num = match.group(1)

    return num_map[num] + '號'


def text_replacement(text):
    text = replace_week(text)  # 統一為周一、周二 ... 周日

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

    # 補上年分 / 和 / A年B月和C月 -> A年B月和A年C月
    text = re.sub(r'明年([十]?[一二三四五六七八九十])月\s*和\s*([十]?[一二三四五六七八九十])月',
                  r'明年\1月和明年\2月', text)
    # 補上年分 / 到 / A年B月到C月 -> A年B月到A年C月
    text = re.sub(r'明年([十]?[一二三四五六七八九十])月\s*到\s*([十]?[一二三四五六七八九十])月',
                  r'明年\1月到明年\2月', text)

    # 阿拉伯 -> 中文 / 幾月
    text = re.sub(r'(\d{1,2})月', month_arabic_to_zh, text)
    # 阿拉伯 N日 -> N號
    text = re.sub(r"(\d{1,2})日", r"\1號", text)
    # 阿拉伯 -> 中文 / 幾號
    text = re.sub(r'(\d{1,2})號', day_arabic_to_zh, text)

    # 補上月份 / 和 / A月B號和C號 -> A月B號和A月C號
    text = re.sub(
        r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*和\s*([一二三]?[十]?[一二三四五六七八九十])號',
        r'\1月\2號到\1月\3號', text)
    # 補上月份 / 到 / A月B號到C號 -> A月B號到A月C號
    text = re.sub(
        r'([十]?[一二三四五六七八九十])月\s*([一二三]?[十]?[一二三四五六七八九十])號\s*到\s*([一二三]?[十]?[一二三四五六七八九十])號',
        r'\1月\2號到\1月\3號', text)

    text = text.replace('臺', '台')

    return text


def get_until_tags(text):
    tag1 = re.findall(
        r'(year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
        text)
    tag2 = re.findall(
        r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(year|month|week|day|hour|minute|second|range)',
        text)
    return tag1, tag2


def next_tag(text):
    ''' 檢查下一個標籤 '''
    # 下一個標籤為tag到tag嗎
    if re.findall(
            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
            text):
        next_match = re.findall(
            r'(?:year|month|week|day|hour|minute|second|range).*?到.*?(?:year|month|week|day|hour|minute|second|range)',
            text)
        print('aqa')  # test
        print(f'下一個標籤是{next_match[0]}，在第{text.index(next_match[0])}個位置')  # test
        check_text = text[:text.index(next_match[0])]
        text = text.replace(text[:text.index(next_match[0])], '')
        # do
        # print(f'>> 檢查"{check_text}"有無城市')
        # print(f'---\n下一輪的字串 "{text}"')
        # print(f'>> !1 檢查 "{check_text}" 有無城市')  # test
        # do
        # 檢查以下這個字串有沒有城市
        # text[text.index(match) + len(match):text.index(next_match[0])]

        # print('!1 bef', text)  # test
        # print('!1 aft', text)  # test
    # 那是單獨一個tag嗎
    elif re.findall(r'year|month|week|day|hour|minute|second|range', text):
        next_match = re.findall(r'year|month|week|day|hour|minute|second|range', text)
        print('awa')  # test
        print(f'下一個標籤是{next_match[0]}，在第{text.index(next_match[0])}個位置')  # test
        check_text = text[:text.index(next_match[0])]
        text = text.replace(text[:text.index(next_match[0])], '')
        # do
        # print(f'>> 檢查"{check_text}"有無城市')
        # print(f'---\n下一輪的字串 "{text}"')
        # print(f'---\n下一輪的字串 {text}')
        # print(f'>> !2 檢查 "{check_text}" 有無城市')  # test
        # do
        # 檢查以下這個字串有沒有城市
        # text[text.index(match) + len(match):text.index(next_match[0])]

        # print('!2 bef', text)  # test
        # print('!2 aft', text)  # test
    # 後面沒有tag了
    else:
        # print(f'range to range 3')  # test
        check_text = text
        # print(f'>> 檢查 {text} 有無城市')

        # do
    return check_text, text


def get_city_indexes(text):
    cities = re.findall(
        r"(台北|雲林|連江|台南|花蓮|屏東|高雄|彰化|新竹|台中|桃園|金門|宜蘭|澎湖|新北|苗栗|南投|基隆|台東|嘉義)", text)
    # print(cities)

    city_indexes = []
    for city in cities:
        for i in range(len(data)):
            if data[i]['cit'] == city:
                city_indexes.append(i)
    # print(city_indexes)

    return city_indexes


conversation()
