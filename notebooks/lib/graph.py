'''
    Graphical Functions
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy.stats import norm
from lib.ml_functions import compute_cost_matrix

DLC = {'dlblue': '#0096ff', 'dlorange': '#FF9300', 'dldarkred': '#C00000', 'dlmagenta': '#FF40FF',
           'dlpurple': '#7030A0'}
DLCOLORS = ['#0096ff', '#FF9300', '#C00000', '#FF40FF', '#7030A0']

# ----------------------------------------------------------------
# GRAPH FUNCTIONS
# ----------------------------------------------------------------
def plot_cost_i_w(x_matrix, y, hist):

    ''' 
        Plots cost vs iteration for given parameters
    '''
    ws = np.array([p[0] for p in hist['params']])
    rng = max(abs(ws[:,0].min()), abs(ws[:,0].max()))
    wr = np.linspace(-rng+0.27, rng+0.27, 20)
    cst = [compute_cost_matrix(x_matrix, y, np.array([wr[i], -32, -67, -1.46]), 221)
        for i in range(len(wr))]

    _, ax = plt.subplots(1,2,figsize = (12,3))
    ax[0].plot(hist['iter'], (hist['cost']))
    ax[0].set_title('Cost vs Iteration')
    ax[0].set_xlabel('iteration')
    ax[0].set_ylabel('Cost')
    ax[1].plot(wr, cst)
    ax[1].set_title('Cost vs w[0]')
    ax[1].set_xlabel('w[0]')
    ax[1].set_ylabel('Cost')
    ax[1].plot(ws[:,0], hist['cost'])
    plt.show()

def norm_plot(ax, data):
    '''
        Plots a histogram and a normal distribution of a given data set.
    '''
    scale = (np.max(data) - np.min(data)) * 0.2
    x = np.linspace(np.min(data) - scale, np.max(data) + scale, 50)
    _, bins, _ = ax.hist(data, x, color = 'xkcd:azure')

    mu = np.mean(data)
    std = np.std(data)
    dist = norm.pdf(bins, loc = mu, scale = std)

    axr = ax.twinx()
    axr.plot(bins,dist, color = 'orangered', lw = 2)
    axr.set_ylim(bottom = 0)
    axr.axis('off')

def plot_data(x_matrix, y, ax, pos_label = 'y=1', neg_label = 'y=0', s = 40, loc = 'best'):#pylint: disable=R0917 disable=R0913
    ''' 
        plots logistic data with two axis 
    '''
    # Find Indices of Positive and Negative Examples
    pos = y == 1
    neg = y == 0
    pos = pos.reshape(-1,)  #work with 1D or 1D y vectors
    neg = neg.reshape(-1,)

    # Plot examples
    ax.scatter(x_matrix[pos, 0], x_matrix[pos, 1], marker = 'x', s = s, c = 'red',
               label = pos_label)
    ax.scatter(x_matrix[neg, 0], x_matrix[neg, 1], marker = 'o', s = s,
               label = neg_label, facecolors = 'none', edgecolors = DLC['dlblue'], lw = 2)
    ax.legend(loc = loc)

    ax.figure.canvas.toolbar_visible = False
    ax.figure.canvas.header_visible = False
    ax.figure.canvas.footer_visible = False

def draw_vthresh(ax, x):
    ''' 
        draws a threshold
    '''
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()
    ax.fill_between([xlim[0], x], [ylim[1], ylim[1]], alpha = 0.2, color = DLC['dlblue'])
    ax.fill_between([x, xlim[1]], [ylim[1], ylim[1]], alpha = 0.2, color = DLC['dldarkred'])
    ax.annotate('z >= 0', xy = [x, 0.5], xycoords = 'data',
                xytext = [30, 5], textcoords = 'offset points')
    draw = FancyArrowPatch(
        posA = (x, 0.5), posB = (x+3, 0.5), color = DLC['dldarkred'],
        arrowstyle = 'simple, head_width=5, head_length=10, tail_width=0.0',
    )
    ax.add_artist(draw)
    ax.annotate('z < 0', xy = [x, 0.5], xycoords = 'data',
                 xytext = [-50, 5], textcoords = 'offset points', ha = 'left')
    func = FancyArrowPatch(
        posA=(x, 0.5), posB = (x-3, 0.5), color = DLC['dlblue'],
        arrowstyle='simple, head_width=5, head_length=10, tail_width=0.0',
    )
    ax.add_artist(func)

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
            data_json = dict(graph.edges[(a, b, 0)])
            print(data_json)
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
