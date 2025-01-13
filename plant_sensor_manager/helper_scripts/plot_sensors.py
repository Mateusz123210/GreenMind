import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Dane wejściowe - podmień na ścieżkę do swojego pliku JSON
file_path = 'sensor_data_2.json'

# Wczytaj dane
import ast
with open(file_path, 'r') as file:
    data_lines = [ast.literal_eval(line.strip()) for line in file]
data = pd.DataFrame(data_lines)

# Konwersja znaczników czasu na format czytelny
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

# Tworzenie wykresu z wieloma osiami Y
fig = go.Figure()

# Dodanie danych temperatury z pierwszą osią Y
fig.add_trace(go.Scatter(x=data['timestamp'], y=data['temperature'], mode='lines', name='Temperatura (°C)'))

# Dodanie danych naświetlenia z drugą osią Y
fig.add_trace(go.Scatter(
    x=data['timestamp'], 
    y=data['illuminance'], 
    mode='lines', 
    name='Naświetlenie (lx)',
    yaxis='y2'
))

# Dodanie danych wilgotności z trzecią osią Y
fig.add_trace(go.Scatter(
    x=data['timestamp'], 
    y=data['moisture'], 
    mode='lines', 
    name='Wilgotność (%)',
    yaxis='y3'
))

# Konfiguracja układu wykresu
fig.update_layout(
    title='Zmiany temperatury, naświetlenia i wilgotności w czasie',
    xaxis=dict(title='Czas'),
    yaxis=dict(title='Temperatura (°C)', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
    yaxis2=dict(
        title='Naświetlenie (lx)',
        titlefont=dict(color='orange'),
        tickfont=dict(color='orange'),
        anchor='x',
        overlaying='y',
        side='right'
    ),
    yaxis3=dict(
        title='Wilgotność (%)',
        titlefont=dict(color='green'),
        tickfont=dict(color='green'),
        anchor='x',
        overlaying='y',
        side='right'
    ),
    legend=dict(title='Parametry'),
    template='plotly_white'
)

# Save the plot as an image file
fig.show()