import sort_distance, get_time
import subprocess


if __name__ =="__main__":

    # # INPUTS - sort_distance.py
    # latitude = 37.571006515132865
    # longitude = 126.99251768504305
    # radius = 0.5 # km

    # # INPUTS - get_time.py
    # search_date = ['2024','07','06'] # 원하는 날짜
    # search_time = '01:00' # 궁금한 시간

    # # PATHS
    # data_path = '/Users/okchang/mainbiz/project/p1_final/data'
    # save_filename = 'cafe_jongro'
    # result_path = '/Users/okchang/mainbiz/project/p1_final/result'
    
    # date = ''.join(search_date)
    # time = ''.join(search_time.split(':'))
    # result_filename = f'카페리스트검색결과_{date}_{time}.csv'


    # subprocess.run(['python', 'data_load.py'])
    # subprocess.run(['python', 'crawl.py'])
    # subprocess.run(['python', 'sort_distance.py'])#, str(latitude), str(longitude), str(radius)])
    subprocess.run(['python', 'get_time.py'])
                    



    pass