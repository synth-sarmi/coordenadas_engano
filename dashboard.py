import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def text_to_coordinates(text):
    coordinates = []
    for char in text:
        if not char.isspace():  # Skip spaces
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
        # Convert text to coordinates
        df = text_to_coordinates(user_text)

        # Display the coordinates in a table
        st.subheader("Coordenadas")
        st.dataframe(df)

        # Create a scatter plot
        fig = px.scatter(df, x='x', y='y', text='character',
                    title='Character Coordinates',
                    labels={'x': 'X Coordinate', 'y': 'Y Coordinate'},
                    width=800, height=600)

        # Update layout to make it square and centered at (0,0)
        fig.update_layout(
        xaxis=dict(range=[-11, 11], zeroline=True),
        yaxis=dict(range=[-11, 11], zeroline=True),
        showlegend=False
        )

        # Add grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        # Show the plot
        st.plotly_chart(fig)

        # Add download button for CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Bajar como CSV",
            data=csv,
            file_name="coordenadas.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()


# se corre con "streamlit run dashboard.py"