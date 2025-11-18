# pages/04_지하철분석.py
# Streamlit page: 2025년 10월 하루 & 호선별 역 순위(Plotly)
# CSV 파일은 루트 폴더에 `BBUU109커하.csv`로 놓아주세요.

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from pathlib import Path

st.set_page_config(page_title="역별 승하차 합계 랭킹 (10월)", layout="wide")

st.title("📊 2025년 10월 — 호선별 역별 승·하차 합계 랭킹 (Plotly)")
st.markdown("CSV는 루트 폴더의 `BBUU109커하.csv`를 사용합니다.")

DATA_PATH = Path("BBUU109커하.csv")
if not DATA_PATH.exists():
    st.error(f"CSV 파일을 루트 폴더에 '{DATA_PATH.name}' 이름으로 올려주세요.")
    st.stop()

# --- 데이터 로드 ---
@st.cache_data
def load_data(path: Path):
    df = pd.read_csv(path)
    # 사용일자: YYYYMMDD (숫자형) -> datetime
    df['사용일자'] = df['사용일자'].astype(str)
    df['date'] = pd.to_datetime(df['사용일자'], format='%Y%m%d', errors='coerce').dt.date
    # 안전형: 승/하차는 숫자형
    df['승차총승객수'] = pd.to_numeric(df['승차총승객수'], errors='coerce').fillna(0).astype(int)
    df['하차총승객수'] = pd.to_numeric(df['하차총승객수'], errors='coerce').fillna(0).astype(int)
    return df

df = load_data(DATA_PATH)

# 2025-10-01 ~ 2025-10-30 필터
valid_start = date(2025, 10, 1)
valid_end = date(2025, 10, 30)

# 사이드바: 날짜, 호선, top N
st.sidebar.header("필터")
selected_date = st.sidebar.date_input("날짜 선택 (2025년 10월)", value=valid_start, min_value=valid_start, max_value=valid_end)

# 노선 목록은 해당 월 데이터 기준으로 제공
df_oct = df[(df['date'] >= valid_start) & (df['date'] <= valid_end)].copy()
if df_oct.empty:
    st.warning("데이터에 2025년 10월 범위의 행이 없습니다.")
    st.stop()

lines = sorted(df_oct['노선명'].dropna().unique().tolist())
lines.insert(0, '전체')
selected_line = st.sidebar.selectbox("호선 선택", options=lines, index=0)

max_rows = st.sidebar.slider("막대 개수 (Top N)", min_value=5, max_value=200, value=30, step=1)

# --- 데이터 필터링 및 집계 ---
mask = (df['date'] == selected_date)
if selected_line != '전체':
    mask &= (df['노선명'] == selected_line)

df_sel = df[mask].copy()
if df_sel.empty:
    st.info("선택한 날짜/호선에 해당하는 데이터가 없습니다. 다른 날짜나 '전체'를 선택해 보세요.")
    st.stop()

# 역별로 승차+하차 합
df_sel['total'] = df_sel['승차총승객수'] + df_sel['하차총승객수']
agg = df_sel.groupby('역명', dropna=True)['total'].sum().reset_index()
agg = agg.sort_values('total', ascending=False).reset_index(drop=True)
agg['rank'] = agg.index + 1

# limit top N
top_n = agg.head(max_rows).copy()

# --- 색상 생성: 1등은 빨간색(#ff0000), 나머지는 파란색 계열 그라데이션 ---
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def interp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i]) * t) for i in range(3))

red = '#ff0000'
blue_start = '#cfe8ff'  # 연한 파랑
blue_end = '#08306b'    # 진한 파랑

colors = []
if len(top_n) > 0:
    colors.append(red)
    n = len(top_n) - 1
    if n > 0:
        a = hex_to_rgb(blue_start)
        b = hex_to_rgb(blue_end)
        for i in range(n):
            t = i / max(1, n-1)  # 0..1
            colors.append(rgb_to_hex(interp(a, b, t)))

# --- Plotly 막대그래프 ---
fig = go.Figure(go.Bar(
    x=top_n['total'][::-1],
    y=top_n['역명'][::-1],
    orientation='h',
    marker=dict(color=colors[::-1]),
    hovertemplate='<b>%{y}</b><br>합계: %{x:,}<extra></extra>'
))

fig.update_layout(
    title=f"{selected_date.isoformat()}  —  {selected_line}  역별 승차+하차 합계 (Top {len(top_n)})",
    xaxis_title='승차총승객수 + 하차총승객수',
    yaxis_title='역명',
    margin=dict(l=240, r=20, t=70, b=40),
    height=60 * max(6, len(top_n))
)

st.plotly_chart(fig, use_container_width=True)

# 하단 테이블
with st.expander("상세표 보기 (역명, 합계, 순위)"):
    st.dataframe(agg[['rank','역명','total']].head(500).style.format({'total':'{:,}'}))

st.markdown("---")
st.caption("코드: pages/04_지하철분석.py  |  CSV: 루트/BBUU109커하.csv")


