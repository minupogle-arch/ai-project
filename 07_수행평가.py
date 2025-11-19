import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# 1) 기본 설정
# -------------------------------
st.set_page_config(
    page_title="디저트 추천 시스템",
    page_icon="🍰",
    layout="wide"
)

st.title("🍰 나만의 디저트 추천 시스템")
st.write("당도, 식감, 온도 취향을 선택하면 가장 잘 맞는 디저트를 추천해줘!")

# -------------------------------
# 2) 디저트 데이터셋
# -------------------------------
data = {
    "dessert": [
        "마카롱", "다쿠아즈", "티라미수", "바스크 치즈케이크", "크렘브륄레",
        "와플", "허니브레드", "말차 파운드", "딸기 아이스크림", "흑임자 푸딩",
        "슈크림", "휘낭시에", "푸딩", "브라우니", "휘핑라떼 케이크"
    ],
    "sweet": [9, 7, 6, 5, 8, 5, 7, 4, 6, 3, 5, 4, 5, 8, 6],
    "soft": [3, 5, 9, 6, 8, 4, 5, 3, 7, 9, 9, 4, 9, 5, 6],
    "chewy": [8, 6, 2, 1, 1, 3, 2, 4, 1, 6, 3, 7, 2, 4, 2],
    "temp": [1,1,0,0,0,1,1,1,0,0,1,1,0,1,1]   # 1=따뜻함, 0=차가움
}

df = pd.DataFrame(data)

# -------------------------------
# 3) 사용자 입력 (취향 선택)
# -------------------------------
st.sidebar.header("✨ 나의 디저트 취향 선택하기")

sweet_pref = st.sidebar.slider("당도 선호도", 1, 10, 5)
soft_pref = st.sidebar.slider("부드러움 선호도", 1, 10, 5)
chewy_pref = st.sidebar.slider("쫀득함 선호도", 1, 10, 5)
temp_pref = st.sidebar.radio("좋아하는 온도", ["차가움", "따뜻함"])

temp_pref_val = 1 if temp_pref == "따뜻함" else 0

user_pref = np.array([sweet_pref, soft_pref, chewy_pref, temp_pref_val])

# -------------------------------
# 4) 추천 알고리즘 (유클리드 거리)
# -------------------------------
def get_recommendations(df, user_pref):
    scores = []
    for _, row in df.iterrows():
        dessert_vec = np.array([row["sweet"], row["soft"], row["chewy"], row["temp"]])
        dist = np.linalg.norm(user_pref - dessert_vec)
        scores.append(dist)

    df["score"] = scores
    return df.sort_values("score").head(3)

rec = get_recommendations(df.copy(), user_pref)

# -------------------------------
# 5) 추천 결과
# -------------------------------
st.subheader("🍮 추천 결과 Top 3")

for i, row in rec.iterrows():
    st.markdown(f"### ⭐ {row['dessert']}")
    st.write(f"- 당도: {row['sweet']}")
    st.write(f"- 부드러움: {row['soft']}")
    st.write(f"- 쫀득함: {row['chewy']}")
    st.write(f"- 온도: {'따뜻함' if row['temp']==1 else '차가움'}")
    st.write("---")

# -------------------------------
# 6) 레이더 차트 시각화
# -------------------------------
st.subheader("📊 추천 디저트 맛 프로필 비교")

labels = ["당도", "부드러움", "쫀득함", "온도(따뜻함)"]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

for _, row in rec.iterrows():
    values = [row["sweet"], row["soft"], row["chewy"], row["temp"]]
    values += values[:1]  # 닫기
    ax.plot(angles + angles[:1], values)
    ax.fill(angles + angles[:1], values, alpha=0.1, label=row["dessert"])

ax.set_xticks(angles)
ax.set_xticklabels(labels)
ax.set_title("추천 디저트 맛 레이더 차트")
ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

st.pyplot(fig)

# -------------------------------
# 끝
# -------------------------------
