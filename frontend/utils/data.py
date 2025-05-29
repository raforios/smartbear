'''
    File library with common functions to process external files
'''
import streamlit as st
import random
import pandas as pd
import numpy as np
import sqlalchemy as sa
# from utils.environment import PARAMETERS

# engine = sa.create_engine(PARAMETERS.get('DATABASE_URL'))
engine = sa.create_engine(st.secrets['DATABASE_URL'])

# ----------------------------------------------------------------
# Generating a list of hexadecimal colors
# ----------------------------------------------------------------
def hexa_color_generator_list(quantity) -> list:
    '''
        Generates a list of unique hexadecimal colors.    
    '''
    colors = set()
    while len(colors) < quantity :
        # Generate a random color
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        hex_color = f'#{red:02x}{green:02x}{blue:02x}'
        colors.add(hex_color)

    return list(colors)

# ----------------------------------------------------------------
# Get data from a excel file
# ----------------------------------------------------------------
def get_excel_data(file_name: str) -> pd.DataFrame:
    ''' 
        Read data from excel file
    '''
    # data_df = pd.read_excel(f'{PARAMETERS.get('DATA_FOLDER')}/{file_name}')
    data_df = pd.read_excel(f'{st.secrets['DATA_FOLDER']}/{file_name}')
    return data_df

# ----------------------------------------------------------------
# Load data from excel file to database
# ----------------------------------------------------------------
def load_excel_data(model: dict, table: str, file_name: str) -> pd.DataFrame:
    '''
        Load data from excel file to database
    '''
    df_load = get_excel_data(file_name)

    df_load = df_load.reset_index(drop = True)

    df_load.index += 1

    df_load = df_load.reset_index().rename(columns = model)

    # Insertar los datos en la tabla
    df_load.to_sql(table, engine, if_exists = 'replace', index = False)

    print(f'total registers: {len(df_load)}')
    return df_load

# ----------------------------------------------------------------
# Load data from text file
# ----------------------------------------------------------------
def load_text_data(file_name: str, delimiter: str, until_col: int, skip_rows: int) -> tuple:
    '''
        Load data from text file
    '''
    data = np.loadtxt(file_name, delimiter = delimiter, skiprows = skip_rows)
    x_matrix = data[:,:until_col]
    y = data[:,until_col]
    return x_matrix, y

# ----------------------------------------------------------------
# Animation for mapping
# ----------------------------------------------------------------
def df_animation_multiple_path(graph, lst_routes, df) -> pd.DataFrame:#pylint: disable=R0914
    '''
        Create a dataframe with animation data for multiple paths
    '''
    for path in lst_routes :
        lst_start, lst_end = [], []
        start_x, start_y = [], []
        end_x, end_y = [], []
        lst_length, lst_time = [], []
        for a, b in zip (path[:-1], path[1:]) :
            # data_json = dict(graph.edges[(a, b, 0)])
            # print(data_json)
            lst_start.append(a)
            lst_end.append(b)
            lst_length.append(round(graph.edges[(a, b, 0)]['length']))
            lst_time.append(round(graph.edges[(a, b, 0)]['travel_time']))
            start_x.append(graph.nodes[a]['x'])
            start_y.append(graph.nodes[a]['y'])
            end_x.append(graph.nodes[b]['x'])
            end_y.append(graph.nodes[b]['y'])

        tmp = pd.DataFrame({
            'origin': str(lst_start),
            'target': str(lst_end),
            'x': start_x,
            'y': start_y,
            'x_next': end_x,
            'y_next': end_y,
            'distance': lst_length,
            'time_seg': lst_time
        })
        df = pd.concat([df, tmp], ignore_index = True)

    df = df.drop(index = 0)
    df = df.reset_index().rename(columns = {'index':'id'})
    return df
