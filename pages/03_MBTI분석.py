import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 페이지 설정
st.set_page_config(page_title="🌍 MBTI 세계 분석", layout="wide")

st.title("🌍 MBTI 16유형 세계 분포 분석 대시보드")

# CSV 경로 (상위 폴더)
csv_path = os.path.join(os.path.dirname(__file__), "..", "countriesMBTI_16types.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("❌ 상위 폴더에 'countriesMBTI_16types.csv' 파일이 없어요!")
    st.stop()

# 탭 구성
tab1, tab2 = st.tabs(["🌎 국가별 MBTI 분포", "📈 MBTI 유형별 상위 국가"])

# ✅ 탭 1 — 국가별 MBTI 분포
with tab1:
    st.subheader("국가별 MBTI 유형 비율 비교")

    country = st.selectbox("국가를 선택하세요", df["Country"].unique(), key="country_tab1")

    selected = df[df["Country"] == country].iloc[0, 1:]
    mbti_df = pd.DataFrame({
        "MBTI": selected.index,
        "비율": selected.values
    }).sort_values("비율", ascending=False)

    # 🔵 색상: 파란색 그라데이션 (반대 방향) + 1등은 빨강
    num_colors = len(mbti_df)
    blue_grad = [px.colors.sample_colorscale("Blues", i / (num_colors - 1)) for i in range(num_colors - 1)]
    colors = ["#FF4B4B"] + blue_grad  # 1등 빨강 + 아래쪽으로 밝아지는 파랑

    # Plotly 그래프
    fig1 = px.bar(
        mbti_df,
        x="MBTI",
        y="비율",
        text=mbti_df["비율"].map(lambda x: f"{x*100:.1f}%"),
        color=mbti_df["MBTI"],
        color_discrete_sequence=colors
    )

    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        title=f"🇺🇳 {country}의 MBTI 분포",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig1, use_container_width=True)

# ✅ 탭 2 — MBTI 유형별 상위 10개국
with tab2:
    st.subheader("MBTI 유형별 전 세계 상위 10개 국가")

    mbti_type = st.selectbox("MBTI 유형을 선택하세요", df.columns[1:], key="mbti_tab2")

    # 선택한 MBTI 기준으로 내림차순 정렬
    sorted_df = df.sort_values(by=mbti_type, ascending=False)

    # 상위 10개 + 한국 포함 여부 확인
    top10 = sorted_df.head(10)
    if "South Korea" not in top10["Country"].values and "South Korea" in df["Country"].values:
        korea_row = df[df["Country"] == "South Korea"]
        top10 = pd.concat([top10, korea_row])

    # 색상: 한국은 빨강, 나머지는 파랑
    colors = ["#FF4B4B" if c == "South Korea" else "#4B8BFF" for c in top10["Country"]]

    fig2 = px.bar(
        top10,
        x="Country",
        y=mbti_type,
        text=top10[mbti_type].map(lambda x: f"{x*100:.1f}%"),
        color=top10["Country"],
        color_discrete_sequence=colors
    )

    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        title=f"🌏 {mbti_type} 유형이 가장 많은 국가 TOP 10",
        xaxis_title="국가",
        yaxis_title=f"{mbti_type} 비율",
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig2, use_container_width=True)

