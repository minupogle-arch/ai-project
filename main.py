import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력해주세요')
st.selectbox('좋아하는 음식을 선택해세요!',['한식','중식','일식','양식','디저트'])
if st.button('인사말 생성'):
  st.write(a+'님, 안녕하세요! 반갑습니다!')
