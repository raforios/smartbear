'''
    Main function for SamartBear frontend APP
'''
import streamlit as st
from layout.menu import menu

st.set_page_config(
    page_title = 'SmartBear Dashboard',
    page_icon = '🌐',
    layout = 'wide',
    initial_sidebar_state = 'collapsed',
    menu_items={
        'Get Help': 'mailto:raforios@gmail.com',
        'Report a bug': "mailto:raforios@gmail.com",
        'About': "# SmartBear APP. This is an *BETA* version!"
    }    
)
def main():
    '''
        Main function Frontend SmartBear
    '''

    st.title('SmartBear')
    st.header('BI - APP')
    menu()


if __name__ == '__main__':
    main()
