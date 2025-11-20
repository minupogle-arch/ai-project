import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

st.set_page_config(page_title="Weather Analysis")

st.title("🌡️ 기상청 데이터 상세 분석")

# -------------------------------
# 🔥 한글 폰트 자동 다운로드 + 등록
# -------------------------------

FONT_PATH = "/tmp/NanumGothic.ttf"

# 폰트 없으면 자동 다운로드
if not os.path.exists(FONT_PATH):
    import urllib.request
    url = "https://github.com/naver/nanumfont/releases/download/v1.0/NanumGothic.ttf"
    urllib.request.urlretrieve(url, FONT_PATH)

# matplotlib 폰트 설정
fm.fontManager.addfont(FONT_PATH)
plt.rc('font', family='NanumGothic')

# -------------------------------

# CSV 로드
try:
    df = pd.read_csv("kma_weather.csv", encoding="cp949")
except:
    st.error("CSV 파일 로드 실패. 루트 폴더에 kma_weather.csv 가 필요합니다.")
    st.stop()

st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 수치형 컬럼 찾기
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(numeric_cols) == 0:
    st.error("그래프를 그릴 수 있는 숫자형 칼럼이 없습니다.")
else:
    target_col = numeric_cols[0]

    st.subheader(f"📊 막대그래프: {target_col} 기준 상위 10개")

    top10 = df.sort_values(by=target_col, ascending=False).head(10)

    fig, ax = plt.subplots()
    ax.bar(top10.index.astype(str), top10[target_col])
    ax.set_xlabel("인덱스")
    ax.set_ylabel(target_col)
    ax.set_title(f"{target_col} 기준 상위 10개")

    st.pyplot(fig)

