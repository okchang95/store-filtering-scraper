import pandas as pd
from haversine import haversine

def distance(data, latitude, longitude, radius):
    '''
    args
        data: str, data.csv 경로 (위도 경도 포함된)
        latitude: float, 기준점 위도
        longitude: float, 기준점 경도
        radius: float, 기준점으로부터의 거리 km 
    
    return
        : 기준점으로부터의 거리 정보가 포함된 dataframe
    '''
    df = pd.read_csv(data)
    # check
    df.info()

    cafe_ls = []
    dist_ls = []
    # 기준점과 데이터상 카페와의 거리 구하기
    for i in range(len(df)):
        # x, y: 카페의 위도, 경도
        x = df['위도'][i]
        y = df['경도'][i]
        # haversine() : 두 지점의 거리 반환
        dist = haversine((latitude, longitude), (x, y), unit = 'km')
        # 입력된 반경 이내의 카페를 리스트에 담고 df로 만듦
        if dist < radius:  
            cafe_ls.append(df.iloc[i]) # 전체 행이 담긴 리스트
            dist_ls.append(dist) # 기준점과의 거리만 담긴 리스트

    dist_df = pd.DataFrame(cafe_ls)

    # dist_df에 dist컬럼 추가
    dist_df['dist'] = dist_ls
    dist_df['dist'] = dist_df['dist'].round(4)

    # dist컬럼 오름차순 정렬
    sorted_df = dist_df.sort_values(by='dist', ascending=True)

    # 인덱스 초기화
    reidx_df = sorted_df.reset_index(drop=True, inplace=False)

    return reidx_df

# TEST
def test(reidx_df, latitude, longitude, print_n):
    '''
    distance에서 반환한 dataframe 출력 test
    '''
    # 거리순 매장 리스트 출력
    out_ls = []
    for i in range(len(reidx_df)):
        out_ls.append(f"{i+1}. {reidx_df['상호명'][i]} ({reidx_df['dist'][i]}km)")

    print("기준좌표: ----------------------------------")
    print(f"- 위도: {latitude}\n- 경도: {longitude}")
    print("------------------------------------------")

    for i, o in enumerate(out_ls):
        print(o)
        if i == print_n:
            break