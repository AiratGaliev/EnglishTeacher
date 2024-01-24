import streamlit as st

st.set_page_config(
    page_title="Document analysis",
    page_icon="📚",
)
st.header("📚 Document analysis")
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

option = st.selectbox(
    'What is your purpose for studying this material?',
    ('Studying technical literature', 'Learning a foreign language', 'Studying technical documentation'))

if st.button('Analise document'):
    st.write('Analyzing document for:', option)
