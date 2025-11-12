import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# 페이지 기본 설정
st.set_page_config(page_title="🌍 국가별 MBTI 분포", layout="centered")

st.title("🌍 국가별 MBTI 16유형 분포 시각화")
st.markdown("국가를 선택하면 각 MBTI 유형 비율을 확인할 수 있어요!")

# CSV 경로 (상위 폴더)
csv_path = os.path.join(os.path.dirname(__file__), "..", "countriesMBTI_16types.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("❌ 상위 폴더에 'countriesMBTI_16types.csv' 파일이 없어요!")
    st.stop()

# 국가 선택
country = st.selectbox("국가를 선택하세요", df["Country"].unique())

# 선택된 국가 데이터 정리
selected = df[df["Country"] == country].iloc[0, 1:]  # Country 제외
mbti_df = pd.DataFrame({
    "MBTI": selected.index,
    "비율": selected.values
}).sort_values("비율", ascending=False)

# 색상 설정
# 1등은 빨간색, 나머지는 파란색 계열 (16개 자동 보간)
num_colors = len(mbti_df)
blue_palette = px.colors.sequential.Blues
blue_grad = [px.colors.sample_colorscale("Blues", i / (num_colors - 1)) for i in range(num_colors - 1)]
colors = ["#FF4B4B"] + blue_grad[::-1]  # 빨강 + 파랑 그라데이션 반전

# Plotly 그래프
fig = px.bar(
    mbti_df,
    x="MBTI",
    y="비율",
    text=mbti_df["비율"].map(lambda x: f"{x*100:.1f}%"),
    color=mbti_df["MBTI"],  # MBTI별 색상 적용
    color_discrete_sequence=colors
)

# 그래프 꾸미기
fig.update_traces(textposition="outside")
fig.update_layout(
    title=f"🇺🇳 {country}의 MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)
