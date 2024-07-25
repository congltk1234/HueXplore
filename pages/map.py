import streamlit as st


if "candidate_points" in st.session_state:
    res = st.session_state["candidate_points"]
    st.write(res)
