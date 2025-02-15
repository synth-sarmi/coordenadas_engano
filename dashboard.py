'''
se corre local con "streamlit run dashboard.py"
está deployado en el streamlit cloud a través de un repositorio en github
para actualizarlo hay que stage - commit - push los cambios y se deben ver en prod
'''

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def text_to_coordinates(text):
    coordinates = []
    for char in text:
        x = np.random.uniform(-10, 10)
        y = np.random.uniform(-10, 10)
        coordinates.append({
            'character': char,
            'x': x,
            'y': y
        })
    return pd.DataFrame(coordinates)

def main():
    st.title("Convertidor de coordenadas El Engaño")

    # Input text box
    user_text = st.text_area("Texto a convertir:", "Ejemplo de un texto que no tiene mucho que decir.")

    if st.button("Generar coordenadas"):
        # Llamar a la función
        df = text_to_coordinates(user_text)

        # imprimit la tablita de coordenadas
        st.subheader("Coordenadas")
        st.dataframe(df)

        # Create a scatter plot
        fig = px.scatter(df, x='x', y='y', text='character',
                    title='Character Coordinates',
                    labels={'x': 'X Coordinate', 'y': 'Y Coordinate'},
                    width=800, height=600)

        # Show the plot
        st.plotly_chart(fig)

        # bajar en CSV las  coordenadas
        csv = df.to_csv(index=False)
        st.download_button(
            label="Bajar como CSV",
            data=csv,
            file_name="coordenadas.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()


