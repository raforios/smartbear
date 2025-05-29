'''
    Menu function
'''
import streamlit as st

def menu():
    '''
        App menu
    '''
    with st.sidebar:
    
        st.markdown('### Dashboards')
        st.page_link('main.py', label='Home', icon=':material/home:')
        st.page_link('pages/resume.py', label='Resume', icon=':material/person:')
        st.page_link('pages/optimization.py', label='Optimization Routes', icon=':material/local_shipping:')
        st.page_link('pages/content_generator.py', label='Content Generator', icon=':material/description:')
        st.page_link('pages/load_file.py', label='Load CSV Files', icon=':material/cloud_upload:')
        st.page_link('pages/dashboard.py', label='Dashboard', icon=':material/analytics:')
        st.page_link('pages/maps.py', label='Maps', icon=':material/map:')
        st.markdown('---')
