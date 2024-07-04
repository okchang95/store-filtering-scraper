# 1. 데이터 정리
# -------------------------------------------------------------------------
# 오리지날데이터(약 47만개)를 받아서 원하는 구역, 원하는 업종(일단은 카페만)으로 데이터 축소, 
# input: 원본 csv 파일, 행정동  (+ 법정동, 업종)
# output: 선택된 데이터 csv파일

import os
import pandas as pd

## INPUTS
data_dir = '/Users/okchang/mainbiz/project/p1_final/data' # 데이터가 저장된 경로
original_filename = 'original_data.csv'
original_data_path = os.path.join(data_dir, original_filename)
dong = '종로1.2.3.4가동' # 행정동명 (필요하면 법정동명도 포함시켜서 필터링)

df = pd.read_csv(original_data_path)

# 1) 불필요한 컬럼 제거
columns_to_keep = ['상호명', '지점명', '상권업종소분류명', '표준산업분류명', '행정동명', '법정동명', '지번주소', '도로명주소', '경도', '위도']
df_filtered = df[columns_to_keep]
print('1) 컬럼 정리')

# 2) 업종 필터링
cafe_df = df_filtered[(df_filtered['표준산업분류명'] == '커피 전문점') | (df_filtered['상권업종소분류명'] == '카페')]
print('2) 업종 필터링')

# 3) 결측치 제거
drop_df = cafe_df.dropna(subset=['표준산업분류명'], inplace=False)
print('3) 결측치 제거')

# 4) 행정동명으로 필터링 | 법정동 포함: dong_df = df[(df['행정동명'] == dong) | (df['법정동명'] == dong)]
dong_df = drop_df[drop_df['행정동명'] == dong]
print('4) 행정동 필터링')

# 인덱스 초기화
reidx_df = dong_df.reset_index(drop=True, inplace=False)
print('5) 인덱스 초기화')

# 저장
save_filename = 'cafe_jongro.csv'
reidx_df.to_csv(os.path.join(data_dir, save_filename), index=False, encoding='utf-8-sig')

print('6) 저장 완료 =================================================')


# X  정리된 데이터 저장
# X  save_filename = 'cafe_seoul.csv'
# X  drop_df.to_csv(f'{data_dir}/{save_filename}', index=False, encoding='utf-8-sig')