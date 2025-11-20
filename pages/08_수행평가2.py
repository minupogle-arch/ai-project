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
    # matplotlib 폰트 및 스타일 설정
    # -------------------------------
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    matplotlib.rcParams['axes.labelsize'] = 12
    matplotlib.rcParams['xtick.labelsize'] = 10
    matplotlib.rcParams['ytick.labelsize'] = 10
    matplotlib.rcParams['axes.facecolor'] = '#f5f5f5'  # 배경색
    matplotlib.rcParams['axes.grid'] = True
    matplotlib.rcParams['grid.color'] = 'white'

    # -------------------------------
    # 색상 설정: 최고값 빨강, 나머지 파랑 그라데이션
    # -------------------------------
    max_index = top10[target_col].idxmax()
    colors = []
    for idx in top10.index:
        if idx == max_index:
            colors.append('red')
        else:
            colors.append(cm.Blues_r(top10.index.get_loc(idx)/10))

    # -------------------------------
    # 막대그래프 그리기
    # -------------------------------
    fig, ax = plt.subplots(figsize=(10,6))
    bars = ax.bar(top10.index.astype(str), top10[target_col], color=colors)

    # x축, y축 라벨
    ax.set_xlabel("Index")
    ax.set_ylabel("target_col")

    # x축 글씨 회전
    ax.tick_params(axis='x', rotation=45)

    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0,3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)


