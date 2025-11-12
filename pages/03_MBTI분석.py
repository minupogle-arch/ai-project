import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 페이지 설정
st.set_page_config(page_title="🌍 국가별 MBTI 분포", layout="centered")

st.title("🌍 국가별 MBTI 16유형 분포 시각화")
st.markdown("국가를 선택하면 각 MBTI 유형 비율을 확인할 수 있어요!")

# CSV 파일 경로 설정 (상위 폴더)
csv_path = os.path.join(os.path.dirname(__file__), "..", "countriesMBTI_16types.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("❌ 상위 폴더에 'countriesMBTI_16types.csv' 파일이 없어요!")
    st.stop()

# 국가 선택
country = st.selectbox("국가를 선택하세요", df["Country"].unique())

# 선택한 국가 데이터 추출
selected = df[df["Country"] == country].iloc[0, 1:]  # Country 제외
mbti_df = pd.DataFrame({
    "MBTI": selected.index,
    "비율": selected.values
}).sort_values("비율", ascending=False)

# 색상 설정: 1등 빨강, 나머지 파란 그라데이션
colors = ["#FF4B4B"] + [px.colors.sequential.Blues[i] for i in range(1, len(mbti_df))]

# Plotly 그래프 생성
fig = px.bar(
    mbti_df,
    x="MBTI",
    y="비율",
    text=mbti_df["비율"].map(lambda x: f"{x*100:.1f}%"),
    color=mbti_df["비율"],
    color_continuous_scale=["#FF4B4B"] + px.colors.sequential.Blues[::-1],
)

# 그래프 스타일 다듬기
fig.update_traces(textposition="outside")
fig.update_layout(
    title=f"🇺🇳 {country}의 MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    coloraxis_showscale=False,
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)
