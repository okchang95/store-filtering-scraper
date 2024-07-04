from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import gc
import pandas as pd
import os

# 1. crawl_url(cafe): 키워드로 검색해서 해당 매장 정보페이지 url 반환
# 2. crawl_time(url): 받은 url에서 운영시간 정보 받아옴. 리스트로 반환
# 3. crawl_star(url): 받은 url에서 별점정보 문자열로 반환
# 4. case_test(case, ifprint=False): 출력 테스트

def crawl_url(cafe):
    '''
    input
        cafe: str, 도로명주소 + 상호명
    return
        new_tab_url: str, 카카오맵 매장 페이지 url
    '''
    # driver = webdriver.Chrome()

    # 백그라운드에서 실행
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    # get url
    time.sleep(1)
    url = 'https://map.kakao.com/'
    driver.get(url)

    # 받은 리스트에서 이름을 가져와 검색창에 넣는다
    time.sleep(1)
    box_path = '//*[@id="search.keyword.query"]' # 검색창 
    box = driver.find_element(By.XPATH, box_path)
    box.send_keys(cafe)
    box.send_keys(Keys.RETURN) # 검색 클릭

    # 상세보기 클릭 ~~ 검색결과 없을수도 있음
    more_path = '//*[@id="info.search.place.list"]/li/div[5]/div[4]/a[1]' # 검색결과 상세보기 버튼
    time.sleep(1)
    try:
        more = driver.find_element(By.XPATH, more_path)
        more.send_keys(Keys.RETURN)

    # 검색결과 없는 경우 -> url 대신 빈 문자열 리턴
    except:
        print('카페 검색결과 없음')
        return ''

    # 새로 열린 창으로 전환
    main_window = driver.current_window_handle
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    # 새 창에서 동작 수행: url반환 
    time.sleep(1)
    new_tab_url = driver.current_url

    # 새 창 닫기
    driver.close()

    # 메인 창으로 전환, 닫기
    driver.switch_to.window(main_window)
    driver.quit()

    print('crawl_url done')
    gc.collect()
    
    return new_tab_url


def crawl_time(url):
    '''
    input
        url: str, 카카오맵 매장 페이지 url
    return
        all_text: list, 운영시간 정보(text)를 담은 리스트 객체 반환
    '''
    # url 없는 경우(검색결과 없는 경우)
    if not url:
        print('url is None')
        all_text = []
        return all_text

    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # 운영시간 상세 클릭
    time.sleep(1)
    xp = '//*[@id="mArticle"]/div[1]/div[2]/div[2]/div/div[1]/div/ul/li/a/span' # 운영시간 확장 버튼

    # try로 운영시간 확장 되는지 확인
    try:
        more2 = driver.find_element(By.XPATH, xp)
        more2.click()
        # print('더보기 있음')
        res = driver.page_source # html source
        driver.close()

        soup = BeautifulSoup(res)
        inner_floor_div = soup.find('div', {'class': 'inner_floor'})
        all_text = inner_floor_div.get_text(separator='\n', strip=True)
        all_text = all_text.split('\n')[1:-1] # 리스트로 반환 [0]: '영업시간', [-1]: '닫기'

    # 운영시간 상세 버튼 없는 경우
    except:
        # print('더보기 없음')
        res = driver.page_source 
        driver.close()

        soup = BeautifulSoup(res)
        txt_operation_span = soup.find('span', {'class': 'txt_operation'}) # 영업시간 없는 경우 여기 Nontype 반환

        # 영업시간 정보 없는 경우
        if not txt_operation_span:
            all_text = [] #'영업시간 없음' 
        else:
            all_text = txt_operation_span.get_text(separator='\n', strip=True) 
            all_text = all_text.split('\n') # 리스트로 반환

    # print('crawl_time done')
    gc.collect()
    return all_text 

# 별점
def crawl_star(url):
    ''' 
    input: str, url
    return: str, 평점
    '''
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(1)
    
    # 별점 xpath
    star_path = '//*[@id="mArticle"]/div[1]/div[1]/div[2]/div/div[2]/a[1]/span[1]'
    star = driver.find_element(By.XPATH, star_path).text
    driver.close()
    print('crawl_star done')
    gc.collect()

    return star

# TEST
def case_test(case, ifprint=False):
    '''
    case1 = '서울 종로구 수표로28길 31' + '플리퍼스 익선점' # 영업시간 더보기 없는 경우
    case2 = '서울 종로구 계동길 5' + '어니언 안국' 
    case3 = '서울 종로구 북촌로 6-3' + '노티드 안국' 
    case4 = '서울 종로구 윤보선길 22' + '도트블랭킷' 
    case5 = '블루어니언소프트' # 운영시간 없는 경우
    case6 = '서울 마포구 포은로6길 11' + '딥블루레이크' # 매일 라스트오더 추가
    case7 = '서울 마포구 망원로6길' + '커피가게동경' # 휴무일 포함
    '''
    new_tab_url = crawl_url(case)
    case_txt = crawl_time(new_tab_url) # 더보기 없음
    if ifprint:
        print(f"[CASE: {case}]")
        print(f"별점: {crawl_star(new_tab_url)}")
        print('================================================================')
        print(case_txt)
        print('================================================================')
        print()
    
    gc.collect()
    return case_txt

################################################################
# main function

# 1. get_urls(data_path, getcsv=False): csv파일 정보로 url정보 가져옴
# 2. get_time_n_dropna(df, save_path): 가져온 url정보로 운영시간 정보 가져와서 csv저장

# get urls: csv의 행정동명 + 상호명으로 검색해서 컬럼 추가후 df 반환
def get_urls(data_path, getcsv=False): #, save_path):
    '''
    args
        data_path: csv 파일
        save_path: 저장 경로(확장자 포함)

    '''
    df = pd.read_csv(data_path)
    df_length = df.index[-1]+1

    url_ls = []
    for i in range(df_length):
    # for i in range(5):
        print(f'\n## get urls({i+1}/{df_length})...')
        url = crawl_url(df['행정동명'][i] + ' ' + df['상호명'][i])
        url_ls.append(url)
        print(f"{i} : {df['상호명'][i]}, {url}")
    print(len(url_ls))

    df['url'] = url_ls
    if getcsv:
       save_path = data_path.replace('.csv', '_withURL.csv')
       df.to_csv(save_path, index=False, encoding='utf-8-sig')
    return df
    

# get_time_n_dropna: get_urls로 반환시킨 df의 url 정보로 운영시간 크롤링
def get_time_n_dropna(df, save_path):
    '''
    args
        df: DataFrame,
            get_urls로 구한 df
            (또는 url컬럼이 포함된 csv 파일:data)
                #df = pd.read_csv(data)  

            -> save csv file
        save_path: str, csv file save path (with extension)
    '''
    
    # url 없으면 에러 -> 결측치 제거
    df.dropna(subset=['url'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # get time
    df_length = df.index[-1]+1
    time_ls = []
    for i in range(df_length):
        print(f'\n## get time({i+1}/{df_length})...')
        time = crawl_time(df['url'][i])
        time_ls.append(time)
        print(f"{i+1} : {df['상호명'][i]}, {time}")
        # TEST
        # if i == 3: break 
    # print(len(time_ls))
    # print(time_ls)

    # 운영시간 없는 경우 데이터 제거
    df['운영시간'] = time_ls
    df.dropna(subset=['운영시간'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # save csv file
    df.to_csv(save_path, index=False, encoding='utf-8-sig')



# # drop null: 크롤링해왔을 때 운영시간/url null값이면 drop
# def drop_null(df):
#     # url 컬럼 빈값 제거
#     drop_url = df.dropna(subset=['url'], inplace=False).reset_index(drop=True, inplace=False)
#     # 운영시간 빈 리스트 제거
#     drop_time = drop_url[drop_url['운영시간'] != '[]']

#     return drop_time