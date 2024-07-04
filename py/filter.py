import pandas as pd
import datetime
import requests
import json
from pandas import json_normalize
from ast import literal_eval
import numpy as np
import re
import os


week = ['월','화','수','목','금','토','일']
week_obj = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4, '토': 5, '일': 6}
basic_sche_ls = [False, False, False, False, False, False, False]


# 공휴일 리스트 불러오는 함수
# search_year : '2024'
# return : [20240101 20240209 20240210 20240211 20240212 20240301 20240410 20240505 ... 20241225] 
def get_holiday_ls(search_year):
    key = 'bReGIChBOFicao2yKs6dK1omF0UQTdG3DATnNWQ1r%2BCH%2Bfz6UpvcYYW6w0MtmnbhRZURyRyOEWCsBnbqtXiGnw%3D%3D'
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50&solYear=' + str(search_year) + '&ServiceKey=' + str(key)
    response = requests.get(url)
    if response.status_code == 200:
        json_ob = json.loads(response.text)
        holidays_data = json_ob['response']['body']['items']['item']
        dataframe = json_normalize(holidays_data)
        holiday_list = dataframe['locdate'].values
        return holiday_list
    else:
        print("공휴일 리스트를 불러오지 못했습니다.")

# 공휴일인지 확인하는 함수
# holiday_list : [20240101 20240209 20240210 20240211 20240212 20240301 20240410 20240505 ... 20241225] 
# search_date(검색 날짜) : ['2024','07','04']
# return : True 또는 False
def is_holiday(holiday_list, search_date):
    if len(np.where(holiday_list == (''.join(search_date)))[0]) == 1:
        '''
        # 경고메세지나옴
        /Users/okchang/mainbiz/project/p1_final/py/filter.py:38: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
        if len(np.where(holiday_list == (''.join(search_date)))[0]) == 1:
        '''
        return True
    else: 
        return False    

########################################################################

# 영업정보 dictionary 리턴하는 함수 
# op_info_list : ['월,화', '07:00 ~ 22:00', '목~금', '07:00 ~ 22:00', '일', '09:00 ~ 23:00', '휴무일', '', '공휴일', '09:00 ~ 22:00']
# return : {'영업일': ['매일', '07:00 ~ 22:00', '일', '09:00 ~ 23:00'], '휴무일': [''], '공휴일': ['09:00 ~ 22:00']}
def get_operating_time_dict(op_info_list):
    if '휴무일' in op_info_list and '공휴일' in op_info_list:
        cday = op_info_list.index('휴무일')
        hday = op_info_list.index('공휴일')
        if len(op_info_list) == hday+1:
            obj = {'영업일': op_info_list[:cday], '휴무일': op_info_list[cday+1 :hday], '공휴일':['휴무일'] }
            return obj
        else:
            if cday < hday: 
                obj = {'영업일': op_info_list[:cday], '휴무일': op_info_list[cday+1 :hday], '공휴일': op_info_list[hday+1:] }
                return obj
            if hday < cday:
                obj = {'영업일': op_info_list[:hday], '공휴일': op_info_list[hday+1 :cday], '휴무일': op_info_list[cday+1:] }
                return obj
    elif '휴무일' in op_info_list:
        cday = op_info_list.index('휴무일')
        obj = {'영업일': op_info_list[:cday], '휴무일': op_info_list[cday+1 :]}
        return obj
    elif '공휴일' in op_info_list:
        hday = op_info_list.index('공휴일')
        if len(op_info_list) == hday+1:
            obj = {'영업일': op_info_list[:hday], '공휴일':'휴무일' }
            return obj
        else: 
            obj = {'영업일': op_info_list[:hday], '공휴일': op_info_list[hday+1 :]}
            return obj
    else:
        obj = {'영업일': op_info_list}
        return obj


# 영업스케줄 list 리턴하는 함수
# op_ls: ['월~목', '07:00 ~ 22:00', '일', '09:00 ~ 23:00']
# return: ['07:00 ~ 22:00', '07:00 ~ 22:00', '07:00 ~ 22:00', '07:00 ~ 22:00', False, False, '09:00 ~ 23:00']
def get_sche_ls(op_ls):
    result = basic_sche_ls.copy()
    com=re.compile('[^월화수목금토일~,]')
    
    for idx in range(len(op_ls)):
        if idx % 2 == 0 :
            if '매일' == op_ls[idx]:
                for i in range(6):
                    result[i] = op_ls[idx+1]
                        
            elif len(com.findall(op_ls[idx])) == 0:
                if'~' in op_ls[idx]:
                    sd = op_ls[idx].split('~')[0]
                    fd = op_ls[idx].split('~')[1]
                
                    for i in range(week_obj[fd]+1):
                        if i >= week_obj[sd]: 
                            result[i] = op_ls[idx+1]
                
                elif ',' in op_ls[idx] : 
                    day_ls = op_ls[idx].split(',')
                    for day in day_ls:
                        result[week_obj[day]] = op_ls[idx+1]

    return result 


# 영업시간 범위 확인하는 함수
# operating_hours(운영 시간) : '09:00 ~ 22:30'
# search_time(검색 시간) : '12:30'
# return : True 또는 False
def check_cafe_sche(operating_hours, search_time):
    r = re.compile("..:..")
    if operating_hours == '휴무일':
        return False
    elif not r.search(operating_hours):
        return False
    else: 
        time_ls = operating_hours.split('~')
        time_ls[0] = time_ls[0].strip().split(':')
        time_ls[1] = time_ls[1].strip().split(':')
        check_time_ls = search_time.split(':')
        
        open_time = int(time_ls[0][0])+int(time_ls[0][1])/60
        close_time = int(time_ls[1][0])+int(time_ls[1][1])/60
        check_time = int(check_time_ls[0])+int(check_time_ls[1])/60

        if close_time < open_time: 
            if check_time >= open_time and check_time <= close_time+24:
                return True
            else:
                return False
        else: 
            if check_time >= open_time and check_time <= close_time:
                return True
            else:
                return False

###############################################################

# 카페이용 가능한지 확인하는 함수
# op_info_list(확인 대상) : csv의 운영시간 값
# search_date
# search_time
# retur : True 또는 False
def cafe_go(op_info_list, search_date, search_time):
    if is_holiday(get_holiday_ls(search_date[0]), search_date):                                          ##### 수정 ##### holiday_list -> get_holiday_ls(search_date[0])
        if '공휴일' in op_info_list:
            return check_cafe_sche(get_operating_time_dict(op_info_list)['공휴일'][0], search_time)
    else: 
        cafe_schedule = get_sche_ls(get_operating_time_dict(op_info_list)['영업일'])
        day = datetime.date(int(search_date[0]), int(search_date[1]), int(search_date[2])).weekday()     ##### 수정 ##### date -> datetime.date
        if cafe_schedule[day]:
            return check_cafe_sche(cafe_schedule[day], search_time)
        else: return False


# 데이터에서 이용가능한 카페리스트 반환하는 함수
# dataframe : 카페csv파일 불러온 것 -> cafe_jongro_crawled.csv
def checked_cafe_df(dataframe, result_path, search_date, search_time):        ##### 추가 ##### + result_path
    result = []
    result1 = []
    result2 = []

    ## search_time이 전날의 closetime 전일 수 있으므로 확인하기 위한 코드 
    # 예시 : 
    # search_time : 7/6 02:00 --> 7/5 26:00
    # 운영시간 : 7/5 12:00 ~ 03:00(27:00), 7/6 12:00 ~ 03:00(27:00)
    date2 = datetime.datetime.strftime(datetime.datetime.strptime(''.join(search_date), '%Y%m%d') + datetime.timedelta(days=-1), '%Y%m%d')
    search_date2 = [date2[:4], date2[4:6], date2[6:]]
    search_time2 = f"{int(search_time.split(':')[0])+24}:{search_time.split(':')[1]}"
    
    for op_info_list in dataframe['운영시간'].values.tolist():
        value = cafe_go(op_info_list, search_date, search_time) or cafe_go(op_info_list, search_date2, search_time2)
        result.append(value)
        result1.append(cafe_go(op_info_list, search_date, search_time))
        result2.append(cafe_go(op_info_list, search_date2, search_time2))
   
    dataframe['운영확인'] = result
    dataframe['운영확인1'] = result1
    dataframe['운영확인2'] = result2
    
    new_df = dataframe.loc[dataframe['운영확인'], ['상호명', 'dist', '도로명주소', 'url', '운영시간']] #, '운영확인1', '운영확인2', '운영확인']]
    date = ''.join(search_date)
    time = ''.join(search_time.split(':'))
    
    # 저장경로 추가                                                              ##### 추가 #####
    filename = f'카페리스트검색결과_{date}_{time}.csv'
    save_path = os.path.join(result_path, filename)

    pd.DataFrame(new_df).to_csv(save_path, index=False, encoding='utf-8-sig') ##### 수정 #####
    
    # 확인을 위한 return추가
    return new_df

# # ## 입력할 값
# search_date = ['2024','07','06']
# search_time = '01:00'


# holiday_list = get_holiday_ls(search_date[0])


# # # csv 불러와서 편집
# df = pd.read_csv('drop_nulls.csv', converters={"운영시간":literal_eval, "운영시간":literal_eval})
# checked_cafe_df(df, search_date, search_time)