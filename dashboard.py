# se corre local con "streamlit run dashboard.py"
# está deployado en el streamlit cloud a través de un repositorio en github
# para actualizarlo hay que stage - commit - push los cambios y se deben ver en prod

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# ------------- EN EL PRIMER BLOQUE DEFINIMOS LAS FUNCIONES QUE HACEN -------------
# 1. PREPROC
# 2. LOAD DICT
# 3. DISTURB_DIC
# 4. WALK PATH
# 5. TRANSFORM TEXT
# 6. EXPORT PATH
# 7 Y 8. FNPLOT Y VISUALIZE

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
    fig, ax = plt.subplots()
    ax.plot(path_x, path_y)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title(title)
    return fig

def visualize(dwalks, alt, t):
    '''
    Define alternative walk to visualize 
    '''
    return fnplot(dwalks[alt]['pathx'], dwalks[alt]['pathy'], t)


# ------------- AQUÍ EMPIEZA EL DASHBOARD - IMPLEMENTACIÓN CON STREAMLIT -------------

def main():
    st.title("Convertidor de texto a coordenadas El Engaño")

    # Initialize session state
    if 'walks' not in st.session_state:
        st.session_state.walks = None

    # Input text box
    user_text = st.text_area("Texto a convertir:", "Ejemplo de un texto que no tiene mucho que decir, pero que saca la chamba.")

    if st.button("Generar coordenadas"):
        # Set random seed before generating coordinates
        random.seed(666)
        # traerse todos los walks
        st.session_state.walks = transform_text(user_text)
        
    if st.session_state.walks is not None:
        walks = st.session_state.walks
        
        # First, create the tabs
        tab_main, tab_alt1, tab_alt2, tab_alt3 = st.tabs(["Main Walk", "Alternative 1", "Alternative 2", "Alternative 3"])

        # Store tabs in a list
        all_tabs = [tab_main, tab_alt1, tab_alt2, tab_alt3]

        # Get all walk information
        walk_items = list(walks.items())

        # Loop through each tab
        for index in range(4):
            # Get the current tab
            current_tab = all_tabs[index]

            # Get the current walk information
            current_walk_name = walk_items[index][0]
            current_walk_data = walk_items[index][1]

            # Use the tab
            with current_tab:
                # Create visualization using the visualize function
                fig = visualize(walks, current_walk_name, f'Path Coordinates - {current_walk_name}')
                st.pyplot(fig)
                plt.close(fig)  # Clean up the figure

        # Create a single DataFrame with all walks
        all_walks_data = []
        for walk_name, walk_data in walk_items:
            df = pd.DataFrame({
                'x': walk_data['pathx'],
                'y': walk_data['pathy']
            })
            df['walk_type'] = walk_name
            all_walks_data.append(df)
        
        combined_df = pd.concat(all_walks_data, ignore_index=True)
        csv = combined_df.to_csv(index=False)
        
        # Single download button for all walks
        st.download_button(
            label="Bajar todas las coordenadas como CSV",
            data=csv,
            file_name="todas_las_coordenadas.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
