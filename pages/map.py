import streamlit as st


if "candidate_point" in st.session_state:
    df = st.session_state["candidate_point"]
    st.write(df)

if "destination_object" in st.session_state:
    dob = st.session_state["destination_object"]
    st.write(dob)

if "origin_object" in st.session_state:
    oob = st.session_state["origin_object"]
    st.write(oob)
