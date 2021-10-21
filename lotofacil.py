import csv

from plotly.graph_objs import Bar
from plotly import offline

filename = 'data/loto_facil_compiled_draws_2345.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)
    data = [row for row in reader]

# Defining the balls that can be draw.
lower_ball = 1
higher_ball = 25
balls = list(range(lower_ball, higher_ball+1))

# Getting all the balls drawn.
draws = [row[2:] for row in data]
draw_balls = [int(ball) for row in draws for ball in row]
    
# Total frequency of ball draw.
frequencies = []
for ball in balls:
    frequency = draw_balls.count(ball)
    frequencies.append(frequency)

# Plot the frequencies
data =[{
    'type': 'bar',
    'x': balls,
    'y': frequencies,
}]

my_layout = {
    'title': 'Frequency of Balls Drawn',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Balls',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
        'dtick': 1,
    },
    'yaxis': {
        'title': 'Frequency',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='ball_frequency.html')