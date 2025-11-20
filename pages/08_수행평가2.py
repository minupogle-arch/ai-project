import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

# -------------------------------
# Streamlit 페이지 설정
# -------------------------------
st.set_page_config(page_title="Weather Analysis", layout="wide")
st.title("🌡️ Weather Data Analysis")

# -------------------------------
# CSV 로드
# -------------------------------
try:
    df = pd.read_csv("kma_weather.csv", encoding="cp949")
except:
    st.error("CSV file load failed. kma_weather.csv is required in the root folder.")
    st.stop()

st.subheader("Data Preview")
st.dataframe(df.head())

# -------------------------------
# 수치형 컬럼 찾기
# -------------------------------
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(numeric_cols) == 0:
    st.error("No numeric columns available for plotting.")
else:
    target_col = numeric_cols[0]
    st.subheader(f"📊 Bar Chart: Top 10 by {target_col}")

    # 상위 10개 데이터
    top10 = df.sort_values(by=target_col, ascending=False).head(10)

    # -------------------------------
    # matplotlib 폰트 설정 (영어 글씨 깨짐 방지)
    # -------------------------------
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # 영어 기본 글꼴 명시
    matplotlib.rcParams['axes.labelsize'] = 12
    matplotlib.rcParams['xtick.labelsize'] = 10
    matplotlib.rcParams['ytick.labelsize'] = 10

    # -------------------------------
    # 막대그래프 그리기
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10,6))
    
    # 파란색 그라데이션
    colors = cm.Blues_r([i/10 for i in range(10)])
    ax.bar(top10.index.astype(str), top10[target_col], color=colors)
    
    # x축, y축 라벨
    ax.set_xlabel("Index")
    ax.set_ylabel(target_col)
    
    # x축 글씨 회전
    ax.tick_params(axis='x', rotation=45)

    # 제목 제거 (깨짐 방지)
    # ax.set_title(...) 삭제

    plt.tight_layout()
    st.pyplot(fig)

