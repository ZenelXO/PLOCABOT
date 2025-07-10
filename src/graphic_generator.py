import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

matplotlib.use('Agg')
def generate_chart(dataDict, chartTitle):
    #Real values obtainer
    data = values_obtainer(dataDict)
    labels = labels_obtainer(dataDict)

    # Crear figura
    fig, ax = plt.subplots()
    
    # Título y etiquetas
    ax.set_title(chartTitle)
    ax.set_xlabel('Detections Type')
    ax.set_ylabel('Detections Counts')

    # Diagrama de barras
    ax.bar(range(len(data)), data, color='#7BAE7F')
    ax.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, rotation=20)

    # Guardar imagen en memoria como PNG
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)

    # Devuelve la imagen como base64
    return f"data:image/png;base64,{base64_img}"

def values_obtainer(dataDict):
    dataResult = []
    for i, j in dataDict.items():
        dataResult.append(j)
    return dataResult

def labels_obtainer(dataDict):
    labelsResult = []
    for label, value in dataDict.items():
        labelsResult.append(f"{label} ({value})")
    return labelsResult




# if __name__ == "__main__":
#     generate_chart( {'Industrial Ship': 10, 'Cruise Ship': 0, 'Sailboat': 0, 'Human Powered Boat': 0, 'Motorboat': 5} )