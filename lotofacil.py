import csv

from plotly.graph_objs import Bar
from plotly import offline

from globe import Globe

def get_frequencies(draws, balls):
    
    draw_balls = [int(ball) for row in draws for ball in row]
    
    frequencies = [draw_balls.count(ball) for ball in balls]
        
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

def get_data(filename):
    
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]
        
    return header, data

def get_simulated_data(number_draws, lower_ball, 
                       higher_ball, balls_drawn):
    
    globe_simulation = Globe(lower_ball=lower_ball, higher_ball=higher_ball, 
                            balls_drawn=balls_drawn)
    
    draws_simulation =[]
    for number_draw in range(number_draws):
        globe_simulation.run_drawn()
        draws_simulation.append(globe_simulation.draw)
        globe_simulation.refresh_balls()
        
    return draws_simulation
    
def main():
    # Get real data from csv file
    filename = 'data/loto_facil_compiled_draws_2345.csv'
    header, data = get_data(filename)

    # Defining the balls that can be draw and amount of balls to be 
    # draw.
    lower_ball = 1
    higher_ball = 25
    balls_drawn = 15
    balls = list(range(lower_ball, higher_ball+1))

    # Get all the balls drawn, total frequency of ball draw and plot 
    # the real frenquecies
    draws = [row[2:] for row in data]
    real_frequencies = get_frequencies(draws, balls)
    make_plot(balls, real_frequencies, "real_balls_draw", "Real Balls Draw")

    # Simulate 1,000,000 of draws, total frequency of ball draw and plot 
    # the simulated frequencies
    number_draws = 1_000_000
    simulated_draws = get_simulated_data(number_draws, lower_ball, 
                                         higher_ball, balls_drawn)
    simulated_frequencies = get_frequencies(simulated_draws, balls)
    make_plot(balls, simulated_frequencies, "simulated_balls_draw", 
            "Simulated 1,000,000 Draws")
    
    # TODO: Implement most common neighbors

if __name__ == "__main__":
    main()