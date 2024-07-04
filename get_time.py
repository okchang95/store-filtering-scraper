# 4. 운영시간 정리, result.csv

from py import filter
import pandas as pd
import os
from ast import literal_eval

## INPUTS ==========================================
search_date = ['2024','07','06'] # 원하는 날짜
search_time = '01:00' # 궁금한 시간
## INPUTS ==========================================

data_dir = '/Users/okchang/mainbiz/project/p1_final/data'
filename = 'cafe_jongro'

# csv 불러와서 편집
crawled_df = pd.read_csv(os.path.join(data_dir, f'{filename}_sorted.csv'),
                            converters={"운영시간":literal_eval, "운영시간":literal_eval})

# 최종 결과 저장
result_path = os.path.join(data_dir.replace('/data', ''), "result")

result_df = filter.checked_cafe_df(crawled_df, result_path, search_date, search_time)

# 확인
print(result_df)
