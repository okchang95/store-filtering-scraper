## 데이터 순서

1. (475236, 39) `original_data.csv`: 원본 데이터 
2. (21425, 10) `cafe_seoul.csv`: 컬럼제거하고 카페만 가져온 데이터 
3. (364, 10) `cafe_jongro.csv`: 종로1234가동으로 필터링 
4. (364, 11) `cafe_jongro_url.csv`: 3번에 url만 크롤링해온 데이터 
5. (301, 12) `cafe_jongro_crawled.csv`: 4번에 운영시간 크롤링 + 결측치 제거 
6. (104, 13)`cafe_jongro_sorted.csv`: 5번을 거리기준으로 필터링, 거리정보 컬럼추가, 가까운순으로 정렬 
7. () `result.csv` -> 크롤링한 운영시간 정리, 원하는 운영시간만 가져온 결과
