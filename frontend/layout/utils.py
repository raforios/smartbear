'''
    Utils for laout functions
'''
# import plotly.express as px
import os
import base64
from pathlib import Path
import streamlit as st

def remote_css(url):
    '''
        Loading remote CSS files
    '''
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html = True)

def local_file(file_name, sub_dir = 'img') -> str:
    '''
        Loading local files
    '''
    current_dir = os.getcwd()
    path = Path(current_dir)
    folder = st.secrets['STATIC_FOLDER']
    file_path = os.path.join(path, folder, sub_dir, file_name)

    if os.path.exists(file_path):
        if sub_dir == 'img':
            return file_path
        if sub_dir == 'docs':
            with open(file_path, 'rb') as file:
                file_contents = file.read()
                b64_file = base64.b64encode(file_contents).decode()
                return b64_file
        if sub_dir == 'css':
            with open(file_path, 'r', encoding = 'utf-8') as file:
                return f'<style>{file.read()}</style>'

    return None

def generate_icon_metric(fa_icon):
    '''
    Function
    '''
    return st.write(f'''<div class="iconMetric"
                    style="background-color:#5155c3;
                    height:70px;
                    width:70px;
                    text-align:center">
                    <i class="fa-solid {fa_icon} fa-2xl" style="line-height:50px;
                    margin:auto;color:white;">
                    </i></div>''', unsafe_allow_html=True)

def aplicar_formato_chart(fig,controls = False, legend = False, hover_template = None):
    '''
    Function
    '''
    fig.update_layout(paper_bgcolor = 'white')
    fig.update_layout(plot_bgcolor = 'white')
    fig.update_layout(showlegend = legend)
    fig.update_layout(title_pad_l = 20)
    fig.update_layout(
    #font_family="Open Sans",
    #font_color="#8dc73f",
    title_font_family = 'verdana',
    title_font_color = 'black',
    title_font_size = 20,
    font_size = 15,
    #legend_title_font_color="green"
    )

    if hover_template:
        if hover_template == '%':
            fig.update_traces(hovertemplate = '<b>%{x}</b> <br> %{y:,.2%}')
        elif hover_template == '$':
            fig.update_traces(hovertemplate = '<b>%{x}</b> <br> $ %{y:,.1f}')
        elif hover_template == '#':
            fig.update_traces(hovertemplate = '<b>%{x}</b> <br> %{y:,.0f}')
    if controls:
        fig.update_xaxes(
            rangeslider_visible=True
        )
    fig.update_layout(
            autosize=True,
            margin = {
                'l': 50,
                'r': 50,
                'b': 100,
                't': 100,
                'pad': 4                
            }
    )
    return fig

def generar_tabla(df):
    '''
    Function
    '''
    header = '</th><th>'.join(df.columns)
    header = f'<thead><tr><th>{header}</th><tr></thead>'
    items = ''
    for _, row in df.iterrows():
        # item='</td><td>'.join(map(str,row.tolist()))
        # item = f'<tr><td>{item}</td><tr>'
        item = [f'<td>{x}</td>' if isinstance(x, str) else
                f'<td style="text-align:right">{x:,.0f}</td>'
                for x in row.tolist()]
        item = ''.join(item)
        item = f'<tr>{item}<tr>'
        items = items+item
    table = f'<table class="dashboardTable">{header}<tbody>{items}</tbody></table>'
    # return table
    st.write(table,unsafe_allow_html=True)
