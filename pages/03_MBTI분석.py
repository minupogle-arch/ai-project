import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.set_page_config(page_title="🌍 국가별 MBTI 분포", layout="centered")

st.title("🌍 국가별 MBTI 16유형 분포 시각화")
st.markdown("국가를 선택하면 각 MBTI 유형 비율을 확인할 수 있어요!")

# CSV 파일 업로드 또는 기본 경로 설정
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (countriesMBTI_16types.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 국가 선택
    country = st.selectbox("국가를 선택하세요", df["Country"].unique())

    # 선택한 국가 데이터만 추출
    selected = df[df["Country"] == country].iloc[0, 1:]  # Country 열 제외
    mbti_df = pd.DataFrame({
        "MBTI": selected.index,
        "비율": selected.values
    }).sort_values("비율", ascending=False)

    # 색상 지정: 1등은 빨강, 나머지는 파랑 그라데이션
    colors = ["#FF4B4B"] + [px.colors.sequential.Blues[i] for i in range(1, len(mbti_df))]

    # Plotly 막대 그래프
    fig = px.bar(
        mbti_df,
        x="MBTI",
        y="비율",
        text=mbti_df["비율"].map(lambda x: f"{x*100:.1f}%"),
        color=mbti_df["비율"],
        color_continuous_scale=["#FF4B4B"] + px.colors.sequential.Blues[::-1],
    )

    # 그래프 꾸미기
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

else:
    st.info("⬆️ CSV 파일을 업로드하면 그래프가 표시됩니다.")
