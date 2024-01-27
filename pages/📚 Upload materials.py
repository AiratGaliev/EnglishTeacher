import streamlit as st

st.set_page_config(
    page_title="Upload materials",
    page_icon="📚",
)
st.header("📚 Upload materials")
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

st.text("Give unique name to link with your materials:")
material_name = st.text_input("Material name", key="material_name")

if st.button('Upload'):
    st.write(f'Materials linked with name "{material_name}" uploaded successfully!')
