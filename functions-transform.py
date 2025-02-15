import pandas as pd
import matplotlib.pyplot as plt
import random
random.seed(666)

def preproc(str_input, dc):
    '''
    Generating random values if input not in dictionary
    '''
    str_output = set(list(str_input))
    for ch in set(list(str_input)): 
        if ch not in dc: 
            ax = random.choice(['x', 'y'])
            if ax == 'x': 
                dc[ch] = {'x': random.choice([-1, 1]), 'y': 0}
            else: 
                dc[ch] = {'x': 0, 'y':  random.choice([-1, 1])}
    return dc 

    
def load_dic():
    '''
    Load csv with initial values for characters
    '''
    # leemos el csv
    df = pd.read_csv('./diccionario_letras.csv')

    # conversión a dict usando la función de pandas
    rows = df.to_dict(orient='records')

    # re acomodamos el diccionario para el formato correcto
    d = {row['letra']: {'x': row['move_x'], 'y': row['move_y']} for row in rows}
    return(d)

def disturb_dic(d): 
    '''
    Shift values in dictionary by 1 row. 
    '''
    k = list(d.keys())
    v = list(d.values())
    vpop = v.pop(0)
    v.append(vpop)
    new_d = dict(zip(k, v))
    return(new_d)

def walk_path(text, d): 
    '''
    For each dictionary of values, walk the path of the string.  
    Return paths. 
    '''
    transf_ch = [d[chr] for chr in text]

    # Load dictionary 
    path_x = [0]
    path_y = [0]

    for letter in transf_ch: 
        # Transform each 
        #l = transform_ch(dc, letter)
        current_x = letter['x']
        current_y = letter['y']
        # Path
        path_x = path_x + [path_x[-1]+current_x]
        path_y = path_y + [path_y[-1]+current_y] 

    #path_x = path_x + [path_x[0]] 
    #path_y = path_y + [path_y[0]]
    
    return(path_x, path_y)

def transform_text(text):
    '''
    Transform text
    Input: text
    Output: instructions set
    '''
    dc = load_dic()
    dc = preproc(text, dc)
    chrctrs = list(text)
    
    walks={}
    x, y = walk_path(chrctrs, dc)
    walks['main walk'] = {'pathx' : x, 'pathy' : y}
    
    # Alternative walk 1
    d1 = disturb_dic(dc) 
    x1, y1 = walk_path(chrctrs, d1)  
    walks['walk alt 1'] = {'pathx' : x1, 'pathy' : y1}
 
    # Alternative walk 2
    d2 = disturb_dic(d1) 
    x2, y2 = walk_path(chrctrs, d2) 
    walks['walk alt 2'] = {'pathx' : x2, 'pathy' : y2}
    
    # Alternative walk 3
    d3 = disturb_dic(d2) 
    x3, y3 = walk_path(chrctrs, d3) 
    walks['walk alt 3'] = {'pathx' : x3, 'pathy' : y3}
    return(walks)

def export_paths(paths_walked_d, alt):
    '''
    Export chose alternative walk 
    '''
    d_to_exp = paths_walked_d[alt]
    pdf = pd.DataFrame(d_to_exp)
    return pdf  

def fnplot(path_x, path_y, title): 
    '''
    Plot 
    '''
    plt.plot(path_x, path_y)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title(title)
    plt.show()

def visualize(dwalks, alt, t):
    '''
    Define alternative walk to visualize 
    '''
    fnplot(dwalks[alt]['pathx'], dwalks[alt]['pathy'], t)
