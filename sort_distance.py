# 3. 거리별 필터링, 정리
# -------------------------------------------------------------------------
# 입력값 받음!!!!!!!!!!!
# 여기서 저장된 dataframe가지고 ~ 운영시간 정리 + 해당 시간에 열려있는 카페 최종 결과 출력

import pandas as pd
import os
from py import distance
import sys

## INPUTS (sample: kg아이티뱅크) =========================================
latitude = 37.571006515132865
longitude = 126.99251768504305
radius = 0.5 # km

# latitude = float(sys.argv[1])
# longitude = float(sys.argv[2])
# radius = float(sys.argv[3])
## =====================================================================

data_dir = '/Users/okchang/mainbiz/project/p1_final/data'
filename = 'cafe_jongro'

crawled_df_path = os.path.join(data_dir, f'{filename}_crawled.csv')
sorted_df = distance.distance(crawled_df_path, latitude, longitude, radius)
# sorted_df.info()

sorted_df.to_csv(os.path.join(data_dir, f'{filename}_sorted.csv'), index=False, encoding='utf-8-sig')
print('done!')
