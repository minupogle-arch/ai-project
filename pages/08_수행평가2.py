# pages/Weather_Analysis.py
import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(page_title="Weather Analysis", layout="wide")
st.title("Weather Data — 분석 도구 (CSV: PLAVEPLBBUU.csv)")

@st.cache_data(show_spinner=False)
def load_data(path: str):
    encodings = ["utf-8", "cp949", "euc-kr", "latin1"]
    last_err = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, low_memory=False)
            return df, enc
        except Exception as e:
            last_err = e
            continue
    raise ValueError(f"CSV 파일을 읽을 수 없습니다. 마지막 에러: {last_err}")

CSV_FILENAME = "PLAVEPLBBUU.csv"
csv_path = Path(CSV_FILENAME)

if not csv_path.exists():
    st.error(f"루트 폴더에 `{CSV_FILENAME}` 파일이 없습니다. 업로드했는지 확인하세요.")
    st.stop()

# Load
with st.spinner("CSV 로드 중..."):
    df, used_encoding = load_data(str(csv_path))

# Sidebar controls
st.sidebar.markdown("## 옵션")
view = st.sidebar.radio("보여줄 내용 선택", ("데이터 미리보기", "기본 통계", "결측치 요약", "막대그래프 (탑값)", "컬럼 설명"))

if view == "데이터 미리보기":
    n = st.sidebar.slider("행 개수", min_value=5, max_value=200, value=10)
    st.markdown(f"**인코딩(자동탐지)**: `{used_encoding}`")
    st.dataframe(df.head(n))

elif view == "기본 통계":
    st.write("### 기본 통계 (수치형 + 범주형)")
    try:
        st.write(df.describe(include='all'))
    except Exception as e:
        st.error(f"통계 요약 생성 중 오류: {e}")

elif view == "결측치 요약":
    st.write("### 컬럼별 결측치 수")
    missing = df.isna().sum().sort_values(ascending=False)
    st.write(missing[missing > 0])

elif view == "컬럼 설명":
    st.write("### 컬럼 목록 및 타입")
    info = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str),
        "non_null_count": df.notna().sum().values
    })
    st.dataframe(info)

else:
    # Bar chart view
    st.write("### 막대그래프 — 컬럼 선택 후 Top N 표시")
    # Determine categorical cols
    cat_cols = df.select_dtypes(include=['object','category']).columns.tolist()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()

    if cat_cols:
        col = st.selectbox("범주형 컬럼 선택", cat_cols, index=0)
        topn = st.number_input("Top N", min_value=3, max_value=50, value=10)
        vc = df[col].fillna("N/A").value_counts().nlargest(topn)
        st.write(f"**컬럼**: {col} — 상위 {topn} 값")
        fig, ax = plt.subplots(figsize=(10,5))
        vc.plot(kind='bar', ax=ax)
        ax.set_xlabel(col)
        ax.set_ylabel("count")
        ax.set_title(f"Top {topn} value counts of '{col}'")
        plt.tight_layout()
        st.pyplot(fig)
    elif num_cols:
        col = st.selectbox("숫자형 컬럼 선택 (binned 분포)", num_cols, index=0)
        bins = st.slider("Binning 구간 수", min_value=5, max_value=50, value=10)
        binned = pd.cut(df[col].dropna(), bins=bins).value_counts().sort_index()
        st.write(f"**컬럼**: {col} — {bins}구간 분포")
        fig, ax = plt.subplots(figsize=(10,5))
        binned.plot(kind='bar', ax=ax)
        ax.set_xlabel(col)
        ax.set_ylabel("count")
        ax.set_title(f"Binned distribution of '{col}'")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("그래프를 그릴 수 있는 적절한 컬럼이 없습니다.")

st.markdown("---")
st.write("앱: 자동 생성된 분석 도구. 추가 기능이나 특정 시각화 원하면 알려줘.")
