import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def distribution_plot(parking_x):
  lista_bicis = pd.read_csv("bicis1.csv", header = 0, sep = ';', encoding='latin-1')
  data = lista_bicis[9]
  mean = np.mean(data)
  # Crear el gráfico de distribución
  plt.style.use("seaborn-dark")
  plt.figure(figsize=(5,4))
  plt.hist(data,color='#5F93BA', edgecolor='None', alpha=0.5)

  # Agregar una línea vertical para marcar la media
  plt.axvline(x=mean, color='black', linestyle='--', label='Mean', alpha = 0.5)
  plt.axvline(x=parking_x, color='#86E0CE', linestyle='--')
  
  plt.text(parking_x*1.08, plt.ylim()[1]*0.5, f'{parking_x}',ha='right', va='top')
  plt.text(plt.xlim()[1]*0.99, plt.ylim()[1]*0.8, f'Mean = {mean:.2f}',ha='right', va='top',bbox = dict(facecolor='white', alpha=0.5))

  # Configuraciones adicionales
  plt.xlabel("Available slots")
  plt.ylabel("Frequency")
  plt.title("Available slots distribution")

  st.pyplot(plt.show())
