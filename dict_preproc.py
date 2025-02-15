import pandas as pd

# leemos el csv
df = pd.read_csv('diccionario_letras.csv')

# conversión a dict usando la función de pandas
rows = df.to_dict(orient='records')

# re acomodamos el diccionario para el formato correcto
letter_dict = {row['letra']: {'x': row['move_x'], 'y': row['move_y']}
               for row in rows}