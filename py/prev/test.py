from py import crawling, distance, filter
import pandas as pd
import os
from ast import literal_eval

if __name__ == '__main__':
    
    # 1. 크롤링 ############################################################################

    # data: cafe_jongro.csv 가져와서 아래 크롤링 실행 
    # data_path = 'data/cafe_jongro.csv' # 상대경로

    # 프로젝트 경로
    root = '/Users/okchang/mainbiz/project/p1_final'
    data_path = os.path.join(root, 'data/cafe_jongro.csv') # 정리만 된 data

    # 크롤링: url, time컬럼 추가 =====> 시간 오래걸림(에러나면 한줄씩 try해서 실패하면 다시하는걸로)
    # df_url = crawling.get_urls(data_path)
    # df_url.to_csv(os.path.join(root, 'data/cafe_jongro_url.csv'), index=False, encoding='utf-8-sig')
    
    # loaded_df_url = pd.read_csv(os.path.join(root, 'data/cafe_jongro_url.csv'))
    # loaded_df_url.info()

    # save_path = os.path.join(root, 'data/cafe_jongro_crawled.csv') # 크롤링 포함된 data 저장
    # crawling.get_time_n_dropna(loaded_df_url, save_path) # save csv

    # 2. 거리기준 검색(sample: kg아이티뱅크) ####################################################

    ## INPUTS ==========================================
    latitude = 37.571006515132865
    longitude = 126.99251768504305
    radius = 0.5 # km
    ## INPUTS ==========================================

    # crawled_df = pd.read_csv(os.path.join(root, 'data/cafe_jongro_crawled.csv'))
    # crawled_df.info() # -> distance가 df가 아니라 경로로 입력... 통일할 필요가 있나?
    crawled_df_path = os.path.join(root, 'data/cafe_jongro_crawled.csv')

    sorted_df = distance.distance(crawled_df_path, latitude, longitude, radius)
    print('sorted_df', sorted_df.head())
    sorted_df.info()

    sorted_df.to_csv(os.path.join(root, 'data/cafe_jongro_sorted.csv'), index=False, encoding='utf-8-sig')

    # ㄴ 여기서 저장된 dataframe가지고 ~ 운영시간 정리 + 해당 시간에 열려있는 카페 최종 결과 출력

    # 3. 운영시간 정리 #######################################################################

    ## INPUTS ==========================================
    search_date = ['2024','07','06'] # 원하는 날짜
    search_time = '01:00' # 궁금한 시간
    ## INPUTS ==========================================

    # csv 불러와서 편집
    crawled_df = pd.read_csv(os.path.join(root, 'data/cafe_jongro_sorted.csv'),
                             converters={"운영시간":literal_eval, "운영시간":literal_eval})
    # 확인
    print('crawled_df',crawled_df.head())
    print('DONE!!!!!!!!!!!')

    result_path = os.path.join(root, "result")

    # 최종 결과 저장
    result_df = filter.checked_cafe_df(crawled_df, result_path, search_date, search_time)
    # 확인
    print(result_df)
    pass