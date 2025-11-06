# app.py
# Streamlit MBTI → 진로 추천 앱
# 저장: app.py
# 실행: streamlit run app.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="MBTI 진로 추천 🌟", page_icon="🎯", layout="centered")

st.title("🎯 MBTI로 골라보는 진로 추천")
st.caption("MBTI 하나 골라봐요 — 청소년 눈높이로 친절하게 설명해줄게요! 🙂")

mbti_types = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ"
]

# 데이터 구조: mbti -> list of two career dicts
DATA = {
    "ISTJ": [
        {
            "title": "회계사 / 재무 전문가",
            "emoji": "📊",
            "majors": "경영학과(회계), 세무·재무 관련 전공",
            "personality": "꼼꼼하고 책임감 강함. 규칙과 절차를 잘 지키는 타입에게 딱!",
            "books": ["『박정식 회계학 입문』 (또는 입문 회계서)", "『The Intelligent Investor』(벤저민 그레이엄)"],
            "movies": ["The Accountant (2016)", "Moneyball (2011)"]
        },
        {
            "title": "토목/건설 엔지니어",
            "emoji": "🏗️",
            "majors": "토목공학, 건축공학",
            "personality": "현실적이고 계획적임. 체계적으로 문제를 해결하는 걸 좋아함.",
            "books": ["『Structures: Or Why Things Don't Fall Down』 (J.E. Gordon)", "엔지니어링 개론서(국내 교재)"],
            "movies": ["Bridge of Spies (2015)", "The Martian (2015)"]
        }
    ],
    "ISFJ": [
        {
            "title": "간호사 / 보건의료 실무자",
            "emoji": "🩺",
            "majors": "간호학과, 보건학과",
            "personality": "봉사정신 있고 세심함. 남을 돕는 데서 보람을 느끼는 타입.",
            "books": ["『한 권으로 끝내는 간호학 기초(입문서)』", "『Being Mortal』 (Atul Gawande)"],
            "movies": ["Patch Adams (1998)", "The Intouchables (2011)"]
        },
        {
            "title": "초등교사 / 유아교육자",
            "emoji": "📚",
            "majors": "교육학과(유아교육·초등교육)",
            "personality": "인내심 많고 안정감 제공. 책임감 있고 학생 돌보는 걸 좋아함.",
            "books": ["『How Children Succeed』 (Paul Tough)", "교수법 입문서(국내 교육서)"],
            "movies": ["Dead Poets Society (1989)", "Freedom Writers (2007)"]
        }
    ],
    "INFJ": [
        {
            "title": "상담심리사 / 임상심리사",
            "emoji": "💬",
            "majors": "심리학과, 상담심리학과",
            "personality": "통찰력 있고 공감 능력 뛰어남. 깊은 대화와 의미를 중시함.",
            "books": ["『Man's Search for Meaning』 (Viktor Frankl)", "『The Gift of Therapy』 (Irvin Yalom)"],
            "movies": ["Good Will Hunting (1997)", "A Beautiful Mind (2001)"]
        },
        {
            "title": "작가 / 창작자(문학·시나리오)",
            "emoji": "✍️",
            "majors": "국어국문학, 창작학, 영상·시나리오 관련학과",
            "personality": "내면 세계가 풍부하고 깊이 있는 표현을 좋아함.",
            "books": ["『On Writing』 (Stephen King)", "국내 문학집/창작 입문서"],
            "movies": ["Amélie (2001)", "Her (2013)"]
        }
    ],
    "INTJ": [
        {
            "title": "연구원 / 데이터 사이언티스트",
            "emoji": "🔬",
            "majors": "통계학, 컴퓨터공학, 전공에 따라 수학·물리",
            "personality": "전략적이고 분석적. 복잡한 문제 풀기를 즐김.",
            "books": ["『Deep Work』 (Cal Newport)", "『Introduction to Statistical Learning』"],
            "movies": ["The Imitation Game (2014)", "Ex Machina (2014)"]
        },
        {
            "title": "전략 컨설턴트",
            "emoji": "📈",
            "majors": "경영학, 경제학, 산업공학",
            "personality": "장기적 계획 세우기 좋아함. 논리적 사고와 독립성 강함.",
            "books": ["『Good Strategy Bad Strategy』 (Richard Rumelt)", "케이스 스터디 모음집(경영)"],
            "movies": ["The Social Network (2010)", "Margin Call (2011)"]
        }
    ],
    "ISTP": [
        {
            "title": "항공정비∙기계정비 엔지니어",
            "emoji": "🔧",
            "majors": "기계공학, 항공정비 관련 학과/전문대",
            "personality": "실용적이고 손재주 좋음. 문제 현장에서 빠르게 해결함.",
            "books": ["기계공학 실습서(국내 교재)", "『The Design of Everyday Things』 (Don Norman)"],
            "movies": ["Ford v Ferrari (2019)", "Top Gun (1986)"]
        },
        {
            "title": "소프트웨어 개발자(실무형)",
            "emoji": "💻",
            "majors": "컴퓨터공학, 소프트웨어학과",
            "personality": "논리적이고 즉흥 대응 능력 우수. 혼자 집중해서 만드는 걸 좋아함.",
            "books": ["『Clean Code』 (Robert C. Martin)", "『The Pragmatic Programmer』"],
            "movies": ["The Matrix (1999)", "WarGames (1983)"]
        }
    ],
    "ISFP": [
        {
            "title": "그래픽 디자이너 / 일러스트레이터",
            "emoji": "🎨",
            "majors": "시각디자인, 미술·디자인 관련 학과",
            "personality": "감성적이고 창의적. 감각적 결과물 만드는 걸 즐김.",
            "books": ["『Steal Like an Artist』 (Austin Kleon)", "디자인 기초 교재"],
            "movies": ["Inside Out (2015)", "La La Land (2016)"]
        },
        {
            "title": "수의사 보조·동물 돌봄 관련 직업",
            "emoji": "🐾",
            "majors": "동물보건, 수의예과(진로 단계에 따라)",
            "personality": "온화하고 동물과 조용히 교감하기 좋음.",
            "books": ["동물행동학 입문서", "『Animals Make Us Human』 (Temple Grandin)"],
            "movies": ["Babe (1995)", "Hachi: A Dog's Tale (2009)"]
        }
    ],
    "INFP": [
        {
            "title": "창작 작가 / 시나리오 작가",
            "emoji": "📝",
            "majors": "문예창작, 국어국문, 영상·시나리오",
            "personality": "이상주의적이고 창의적. 자기만의 메시지를 표현하는 데 재능.",
            "books": ["『Bird by Bird』 (Anne Lamott)", "창작 입문서(국내)"],
            "movies": ["Eternal Sunshine of the Spotless Mind (2004)", "Big Fish (2003)"]
        },
        {
            "title": "인문·사회 연구자 / NGO 활동가",
            "emoji": "🌱",
            "majors": "사회학, 인류학, 국제관계",
            "personality": "가치 중심적이고 공감 능력 높음. 사회문제에 관심 많음.",
            "books": ["『The Alchemist』 (Paulo Coelho)", "사회운동 관련 도서(입문)"],
            "movies": ["The Pursuit of Happyness (2006)", "The Motorcycle Diaries (2004)"]
        }
    ],
    "INTP": [
        {
            "title": "소프트웨어 아키텍트 / 연구개발",
            "emoji": "🧠",
            "majors": "컴퓨터공학, 수학, 전산학",
            "personality": "논리적, 호기심 많음. 이론적 문제 풀기를 즐김.",
            "books": ["『Gödel, Escher, Bach』 (Douglas Hofstadter)", "『Introduction to Algorithms』"],
            "movies": ["Primer (2004)", "The Social Network (2010)"]
        },
        {
            "title": "학계(대학원 연구자)",
            "emoji": "📚",
            "majors": "전공 심화(수학·물리·컴퓨터 등)",
            "personality": "독립적 연구 선호. 긴 호흡의 프로젝트에 적응 잘함.",
            "books": ["전공 심화서(해당 분야 교재)", "『The Structure of Scientific Revolutions』 (Thomas Kuhn)"],
            "movies": ["A Beautiful Mind (2001)", "Good Will Hunting (1997)"]
        }
    ],
    "ESTP": [
        {
            "title": "영업·세일즈 전문가",
            "emoji": "🤝",
            "majors": "경영학, 마케팅, 상경 계열",
            "personality": "사교적이고 행동력 있음. 현장감각으로 성과 내기 좋음.",
            "books": ["『How to Win Friends and Influence People』 (Dale Carnegie)", "영업 실무서(국내)"],
            "movies": ["The Wolf of Wall Street (2013)", "Jerry Maguire (1996)"]
        },
        {
            "title": "응급구조사·소방관",
            "emoji": "🚨",
            "majors": "응급구조학, 소방안전 관련 교육과정",
            "personality": "위기 상황에서 빠르게 판단하고 행동함. 도전적임.",
            "books": ["응급의료·응급처치 입문서", "현장 사례집(국내)"],
            "movies": ["Backdraft (1991)", "Ladder 49 (2004)"]
        }
    ],
    "ESFP": [
        {
            "title": "공연·엔터테이너 (뮤지션·무대)",
            "emoji": "🎤",
            "majors": "실용음악, 공연예술, 연기학과",
            "personality": "무대 체질! 에너지 넘치고 사람들 앞에서 즐거움 줌.",
            "books": ["무대 연기·보컬 교재", "『Showmanship』 관련 서적"],
            "movies": ["La La Land (2016)", "Sing Street (2016)"]
        },
        {
            "title": "이벤트 플래너·호스피탈리티",
            "emoji": "🎉",
            "majors": "호텔경영, 관광·이벤트학과",
            "personality": "사교성 높고 즉흥 대처 잘함. 분위기 띄우는 역할에 강점.",
            "books": ["이벤트 기획 실무서", "서비스 매너 관련 서적"],
            "movies": ["The Grand Budapest Hotel (2014)", "Chef (2014)"]
        }
    ],
    "ENFP": [
        {
            "title": "스타트업 창업가 / 제품 기획",
            "emoji": "🚀",
            "majors": "경영학, 창업학, 컴퓨터·디자인 융합 전공",
            "personality": "아이디어 뿜뿜! 사람과 비전을 연결하는 데 강함.",
            "books": ["『Start with Why』 (Simon Sinek)", "『The Lean Startup』 (Eric Ries)"],
            "movies": ["The Social Network (2010)", "Joy (2015)"]
        },
        {
            "title": "콘텐츠 크리에이터 / 마케터",
            "emoji": "📣",
            "majors": "미디어커뮤니케이션, 광고·PR",
            "personality": "창의적이고 에너지 많음. 트렌드 감각이 뛰어남.",
            "books": ["콘텐츠 마케팅 입문서", "『Contagious』 (Jonah Berger)"],
            "movies": ["The Truman Show (1998)", "Chef (2014)"]
        }
    ],
    "ENTP": [
        {
            "title": "기업가·혁신 컨설턴트",
            "emoji": "💡",
            "majors": "경영학, 산업공학, 융합 전공",
            "personality": "토론 좋아하고 아이디어로 사람 설득함. 변화와 실험을 즐김.",
            "books": ["『Zero to One』 (Peter Thiel)", "『The Innovator's Dilemma』 (Clayton Christensen)"],
            "movies": ["The Social Network (2010)", "Steve Jobs (2015)"]
        },
        {
            "title": "변호사(특히 토론·논리 필요한 분야)",
            "emoji": "⚖️",
            "majors": "법학, 정치외교학",
            "personality": "말로 논쟁하고 전략 세우는 걸 좋아함.",
            "books": ["법학 입문서, 논리학 서적", "『Getting to Yes』 (Roger Fisher)"],
            "movies": ["A Few Good Men (1992)", "The Verdict (1982)"]
        }
    ],
    "ESTJ": [
        {
            "title": "공공행정·관리자 (공무원)",
            "emoji": "🏛️",
            "majors": "행정학, 정치학, 경영학",
            "personality": "조직 운영과 규칙을 중시. 리더십 있고 실무 지향적.",
            "books": ["행정학 총론(국내 교재)", "리더십 입문서"],
            "movies": ["Erin Brockovich (2000)", "The King's Speech (2010)"]
        },
        {
            "title": "프로젝트 매니저",
            "emoji": "🗂️",
            "majors": "경영학, 산업공학, IT 관련 전공",
            "personality": "조직화 능력 우수. 일정을 관리하고 팀을 이끄는 걸 잘함.",
            "books": ["『Scrum』 관련 입문서", "PMBOK 또는 프로젝트 관리 입문서"],
            "movies": ["Moneyball (2011)", "The Big Short (2015)"]
        }
    ],
    "ESFJ": [
        {
            "title": "HR·인사담당자",
            "emoji": "🤝",
            "majors": "경영학(인사), 심리학",
            "personality": "사람을 챙기고 조직의 분위기를 돌보는 데 강함.",
            "books": ["『Emotional Intelligence』 (Daniel Goleman)", "HR 실무서(국내)"],
            "movies": ["The Intern (2015)", "The Devil Wears Prada (2006)"]
        },
        {
            "title": "병원 행정·의료 코디네이터",
            "emoji": "🩺🗂️",
            "majors": "보건행정, 의료경영",
            "personality": "서비스 마인드 높고 세세한 관리 좋아함.",
            "books": ["의료경영 입문서", "서비스 매너/관리 서적"],
            "movies": ["Patch Adams (1998)", "The Intouchables (2011)"]
        }
    ],
    "ENFJ": [
        {
            "title": "교육 컨설턴트 / 커리어 코치",
            "emoji": "🎓",
            "majors": "교육학, 심리학, 상담",
            "personality": "사람 이끄는 능력 탁월. 동기부여와 지도에 능숙함.",
            "books": ["『Drive』 (Daniel Pink)", "교육상담 관련 서적"],
            "movies": ["Freedom Writers (2007)", "Dead Poets Society (1989)"]
        },
        {
            "title": "PR·커뮤니케이션 매니저",
            "emoji": "🗣️",
            "majors": "미디어커뮤니케이션, 광고·PR",
            "personality": "커뮤니케이션 능력 뛰어나고 사람을 연결함.",
            "books": ["『Influence』 (Robert Cialdini)", "PR·브랜딩 입문서"],
            "movies": ["The Social Network (2010)", "The King’s Speech (2010)"]
        }
    ],
    "ENTJ": [
        {
            "title": "경영자·임원(CEO)",
            "emoji": "🏆",
            "majors": "경영학, 국제경영, 경제학",
            "personality": "목표 지향적이고 리더십 강함. 전략적으로 조직 이끌기 좋음.",
            "books": ["『Good to Great』 (Jim Collins)", "경영전략 관련 서적"],
            "movies": ["The Founder (2016)", "Wall Street (1987)"]
        },
        {
            "title": "투자은행가 / 금융 트레이더",
            "emoji": "💼",
            "majors": "경제학, 금융학, 수학",
            "personality": "결단력 있고 경쟁심 강함. 빠른 판단과 리스크 관리 능력 필요.",
            "books": ["『Liar's Poker』 (Michael Lewis)", "『The Intelligent Investor』"],
            "movies": ["The Big Short (2015)", "Wall Street (1987)"]
        }
    ],
}

def render_career(card):
    st.markdown(f"### {card['emoji']} {card['title']}")
    st.write(f"**어울리는 학과 · 전공:** {card['majors']}")
    st.write(f"**어떤 성격이 잘 맞을까?** {card['personality']}")
    st.write("**추천 도서:**")
    for b in card["books"]:
        st.write(f"• {b}")
    st.write("**추천 영화:**")
    for m in card["movies"]:
        st.write(f"• {m}")

# UI
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("#### MBTI 선택")
    mbti = st.selectbox("", mbti_types, index=0)
    if st.button("추천 보여줘! ▶️"):
        st.session_state["show"] = True
with col2:
    st.markdown("#### 결과")
    if not st.session_state.get("show"):
        st.info("왼쪽에서 MBTI 골라서 '추천 보여줘! ▶️' 눌러봐요 ✨\n\n간단한 설명과 책/영화 추천까지 같이 알려줄게요.")
    else:
        careers = DATA.get(mbti, [])
        st.markdown(f"## {mbti} 유형 추천 진로 🔎")
        st.write("아래는 **두 가지** 진로 제안이야 — 각 항목마다 어울리는 학과, 성격, 관련 도서·영화까지 넣었어. 필요하면 더 자세히 파볼까?")
        for idx, c in enumerate(careers, start=1):
            st.markdown("---")
            render_career(c)

st.markdown("---")
st.caption(dedent("""
앱 사용 팁 💡
- 더 구체적(예: 관심과목, 성향)을 알려주면 진로 추천을 더 개인화할게.
- 도서/영화 추천은 입문·영감용으로 고른 거야. 관심 있으면 도서별 설명이나 영화 줄거리도 정리해줄게!
"""))

# 작은 저작권/출처 안내
st.markdown("**참고**: 책/영화 제목은 대중적으로 알려진 작품 위주로 예시를 넣었어. 실제 강의계획서/학과 안내는 각 대학·기관 사이트를 확인하면 좋아요.")
