import csv

from plotly.graph_objs import Bar
from plotly import offline

from globe import Globe

def get_frequencies(draws):
    draw_balls = [int(ball) for row in draws for ball in row]
    frequencies = []
    for ball in balls:
        frequency = draw_balls.count(ball)
        frequencies.append(frequency)
    return frequencies

def make_plot(balls, frequencies, file_name, title=None):
    data =[{
    'type': 'bar',
    'x': balls,
    'y': frequencies,
    }]
    
    my_layout = {
        'title': title,
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
    offline.plot(fig, filename=f'{file_name}.html')

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
# Total frequency of ball draw.
real_frequencies = get_frequencies(draws)

# Plot the real frequencies
make_plot(balls, real_frequencies, "real_balls_draw", "Real Balls Draw")

# 1,000,000 of draws
number_draws = 1_000_000
globe_simulation = Globe(lower_ball=lower_ball, higher_ball=higher_ball, 
                         balls_drawn=15)

draws_simulation =[]
for number_draw in range(number_draws):
    globe_simulation.run_drawn()
    draws_simulation.append(globe_simulation.draw)
    globe_simulation.refresh_balls()

simulated_frequencies = get_frequencies(draws_simulation)

make_plot(balls, simulated_frequencies, "simulated_balls_draw", 
          "Simulated 1,000,000 Draws")