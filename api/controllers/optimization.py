'''
    Optimization Controller
'''
import pandas as pd
import osmnx as ox
import networkx as nx
from schemas.optimization import DataMapResponse, RouteResponse
from services.database import engine
from services.ml_optimization import distance_between_points, fiter_order_df
from services.ml_optimization import optimal_route, GeoAnalyzer

async def preparing_data(route_id: int, day: int) -> pd.DataFrame:
    '''
        Preparing data from database to ML models
    '''
    try:
        dtf = database_to_df(route_id, day)

        data = draw_map(dtf)

        data_model = df_to_pydantic(data, DataMapResponse)

        return data_model
    except TypeError as error:
        print(f'Error Creating Dataframe from Database: {error}')
        return None

async def data_ordered(route_id: int, day: int) -> pd.DataFrame:
    '''
        Ordering data and calculating distances
    '''
    try:
        dtf = database_to_df(route_id, day)

        dtf_distances = distances(dtf)

        dtf_order = fiter_order_df(dtf_distances['origin'] == int(dtf_distances['origin'].iloc[0]),
                                'distance', dtf_distances)

        dtf_final = final_data(dtf_order, dtf_distances)

        return dtf_final
    except TypeError as error:
        print(f'Error Creating Dataframe from Database: {error}')
        return None

async def optimization_algorithm(route_id: int, day: int, dist: int) -> pd.DataFrame:
    '''
        Route optimization algorithm
    '''
    try:
        dtf_final = await data_ordered(route_id, day)

        dtf_route = final_route(dtf_final, dist)

        dtf_route_model = df_to_pydantic(dtf_route, RouteResponse)

        return dtf_route_model
    except TypeError as error:
        print(f'Error Optimization Algoritm: {error}')
        return None

async def simulation_algorithm(route_id: int, day: int) -> pd.DataFrame:
    '''
        Route optimization algorithm
    '''
    try:
        dtf = database_to_df(route_id, day)
        data = draw_map(dtf)

        distance_matrix = data[data['day'] == day][ ['client_id', 'y', 'x']].reset_index(drop=True)
        distance_matrix = distance_matrix.rename(columns = {'y': 'latitude', 'x': 'longitude'})
        distance_matrix = distance_matrix.set_index('client_id')

        geo_analyzer = GeoAnalyzer()
        geo_analyzer.add_locations(distance_matrix)

        df_distances = geo_analyzer.get_distance_matrix()

        return df_distances
    except TypeError as error:
        print(f'Error Creating Dataframe from Database: {error}')
        return None

def database_to_df(route_id: int, day: int) -> pd.DataFrame:
    '''
        Read data from table and convert to pandas dataframe
    '''
    try:
        query = f'SELECT * FROM routes WHERE route_id = {route_id} and day = {day}'
        dtf = pd.read_sql(query, engine)
        dtf = dtf[['day', 'client_id', 'latitude', 'longitude']].reset_index(drop = True)
        dtf = dtf.rename(columns = {'latitude': 'y', 'longitude': 'x'})

        return dtf
    except IOError as error:
        print(f'Error extracting data from database: {error}')
        return None

def draw_map(dtf: pd.DataFrame) -> tuple:
    '''
        Creating a dataframe to draw map
    '''
    data = dtf.copy()
    size, _ = data.shape
    data_order = data.sort_values(by = 'client_id', ascending = True)
    data = data_order.reset_index(drop = True)
    data.loc[0, 'color'] = 'red'
    mask = (data.index >= 1) & (data.index < len(data) - 1)
    data.loc[mask, 'color'] = 'black'
    data.loc[size - 1, 'color'] = 'green'
    # start = data[data.index == 0][['y', 'x']].values[0]

    return data

def distances(dtf: pd.DataFrame) -> pd.DataFrame:
    '''
        Creating the dataframe with linear distance calculations
    '''
    dtf_distances = pd.DataFrame({'origin': dtf.at[0, 'client_id'],
                                'target': dtf.at[0, 'client_id'],
                                'x': dtf.at[0, 'x'],
                                'y': dtf.at[0, 'y'],
                                'distance': 0},
                                index = [0])
    # Iterar sobre las filas y calcular las diferencias
    for i in range(len(dtf)):
        #Para evitar calcular la diferencia de una fila consigo misma
        for j in range(i + 1, len(dtf)):
            node_1 = (dtf.at[i, 'x'], dtf.at[i, 'y'])
            node_2 = (dtf.at[j, 'x'], dtf.at[j, 'y'])
            distance = distance_between_points(node_1, node_2)
            new_row = pd.DataFrame({'origin': dtf.at[i, 'client_id'],
                                    'target': dtf.at[j, 'client_id'],
                                    'x': dtf.at[j, 'x'],
                                    'y': dtf.at[j, 'y'],
                                    'distance': distance},
                                    index = [i * j])
            dtf_distances = pd.concat([dtf_distances, new_row], ignore_index = True)

    dtf_distances = dtf_distances.reset_index(drop = True)

    return dtf_distances

def final_data(dtf: pd.DataFrame, dtf_distances: pd.DataFrame) -> pd.DataFrame:
    '''
        Creating the dataframe with the optimized and organized route
    '''
    dtf_final = pd.DataFrame({'origin': dtf.at[0, 'target'],
                            'target': dtf.at[1, 'target'],
                            'distance': dtf.at[1, 'distance'],
                            'x': dtf.at[0, 'x'],
                            'y': dtf.at[0, 'y']},
                            index = [0])

    origin = dtf.at[0, 'target']
    target = dtf.at[1, 'target']
    dtf_final = optimal_route(len(dtf), origin, target, dtf_distances, dtf_final)

    dtf_final = pd.merge(dtf_final, dtf, left_on = 'origin',
                         right_on = 'target', how = 'left')

    dtf_final.drop(columns = ['x_x', 'y_x', 'origin_y', 'target_y', 'distance_y'],
                   axis = 1, inplace = True)

    dtf_final = dtf_final.rename(columns = {'origin_x': 'origin',
        'distance_x': 'distance', 'y_y': 'y', 'x_y': 'x',
        'target_x': 'target'})

    return dtf_final

def final_route(dtf: pd.DataFrame, dist) -> pd.DataFrame:
    '''
        Creating the dataframe with the final route data
    '''
    start = dtf[dtf.index == 0][['y', 'x']].values[0]

    df_route = dtf.copy()
    df_route.index.name = 'visit_order'
    df_route.drop(columns = ['target'], axis = 1, inplace = True)

    df_route_segments = df_route.join(
        df_route.shift(-1),  # map each stop to its next stop
        rsuffix = '_next'
    ).dropna()  # last stop has no 'next one', so drop it
    df_route_segments.drop(columns = ['distance_next'], axis = 1, inplace = True)
    df_route_segments = df_route_segments.rename(columns = {'origin_next': 'target'})

    df_route_segments['time_seg'] = df_route_segments.apply(
        lambda stop: distance_between_points(
            (stop.y, stop.x),
            (stop.y_next, stop.x_next)),
        axis = 1
    )

    graph = ox.graph_from_point(start, dist = dist, network_type = 'drive')
    df_route_segments.loc[:,'origin_node'] = df_route_segments[['y', 'x']].apply(
        lambda x: ox.distance.nearest_nodes(graph, x.iloc[1], x.iloc[0]), axis = 1)
    df_route_segments.loc[:,'destination_node'] = df_route_segments[['y_next', 'x_next']].apply(
        lambda x: ox.distance.nearest_nodes(graph, x.iloc[1], x.iloc[0]), axis = 1)
    df_route_segments.loc[:,'route'] = df_route_segments[['origin_node', 'destination_node']].apply(
        lambda x: nx.shortest_path(graph, x.iloc[0], x.iloc[1], weight = 'length'), axis = 1)

    return df_route_segments

def df_to_pydantic(df: pd.DataFrame, model) -> list:
    '''
        Transforming a dataframe in pydantic class
    '''
    data = df.to_dict(orient = 'records')
    return [model(**item) for item in data]
