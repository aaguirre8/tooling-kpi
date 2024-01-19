import streamlit as st

from src.database.main import main as api_setup_database

# Subheader
st.markdown("""
<style>
    .setup-database-subheader {
        color: #153D64;
        font-size: 36px;
        font-family: font-family: 'Roboto', sans-serif;; 
    }
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="setup-database-subheader">Setup Database</div>', unsafe_allow_html=True)


with st.container():
    # Spacing
    st.markdown("""
    <style>
        .custom-spacing {
            margin-bottom: 20px; /* Adjust the margin as needed for spacing */
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="custom-spacing"></div>', unsafe_allow_html=True)

    start_button = st.button("Get started")
    if start_button:
        api_setup_database()
        st.write("Database setup complete!")