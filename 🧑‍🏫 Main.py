import streamlit as st

from utils.loaders import load_dolphin_dpo_laser


# @st.cache_data(show_spinner="Fetching data from LLM...")
def model_response(prompt):
    model = load_dolphin_dpo_laser()
    response = model.invoke(prompt)
    return response


if __name__ == '__main__':
    st.set_page_config(
        page_title="AI Tutor",
        page_icon="🧑‍🏫",
    )
    st.header("🧑‍🏫 Hello! I'm your tutor")
    if st.button('Get idea'):
        resp = model_response("What would be a good company name for a company that makes colorful socks?")
        st.write(resp)
