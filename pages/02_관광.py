import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지도", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인이 좋아하는 서울 주요 관광지 Top 10")
st.write("서울을 대표하는 인기 관광지를 지도 위에 표시했습니다!")

# 서울 중심 좌표
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 관광지 리스트 (좌표 포함)
tourist_spots = [
    {"name": "경복궁 (Gyeongbokgung Palace)", "lat": 37.579617, "lon": 126.977041},
    {"name": "명동 (Myeongdong Shopping Street)", "lat": 37.563757, "lon": 126.982682},
    {"name": "남산타워 (Namsan Seoul Tower)", "lat": 37.551169, "lon": 126.988227},
    {"name": "홍대 (Hongdae)", "lat": 37.556327, "lon": 126.922965},
    {"name": "인사동 (Insadong)", "lat": 37.574012, "lon": 126.984919},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.566479, "lon": 127.009135},
    {"name": "이태원 (Itaewon)", "lat": 37.534531, "lon": 126.994153},
    {"name": "북촌한옥마을 (Bukchon Hanok Village)", "lat": 37.582604, "lon": 126.983998},
    {"name": "롯데월드타워 (Lotte World Tower)", "lat": 37.513068, "lon": 127.102493},
    {"name": "청계천 (Cheonggyecheon Stream)", "lat": 37.569713, "lon": 126.989317},
]

# 마커 추가
for spot in tourist_spots:
    folium.Marker(
        [spot["lat"], spot["lon"]],
        popup=spot["name"],
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=1000, height=600)
