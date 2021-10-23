import csv

from plotly.graph_objs import Bar
from plotly import offline

from globe import Globe

from operator import itemgetter

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

def get_draws_integer_sorted(draws):
    
    draws_integer = []
    for draw in draws:
        draw_list = []
        for ball in draw:
            draw_list.append(int(ball))
        draw_list.sort()
        draws_integer.append(draw_list)
    
    return draws_integer

def create_neighbors_dict(balls):
    
    ball_dict = {}
    for ball in balls[:-1]:
        ball_dict[ball] = {}
        for ball_pair in balls[ball:]:
            ball_dict[ball][ball_pair] = 0
            
    return ball_dict

def create_ball_dict(draws_sorted, balls):
    # Create ball dictionary
    ball_dict = create_neighbors_dict(balls)
    # Populate ball dictionary
    for draw in draws_sorted:
        for ball_1 in draw.copy():
            draw.remove(ball_1)
            for ball_2 in draw:
                ball_dict[ball_1][ball_2] += 1
    
    return ball_dict

def get_qty_sequential_numbers(draws_sorted, balls_drawn):
    """Function that returns a dictionary the quantity of sequential 
    numbers of all draws.
    
    Args:
        draws_sorted (Nested List): Sorted nested list with integer 
                                    numbers
        balls_drawn (integer): How many balls will be drawn.

    Returns:
        Dictionary: Dictionary - {sequential: quantity}
    """    
    qty_sequential = {sequence: 0 for sequence in range(1, balls_drawn+1)}
    sequential_draws_dict = {}
    
    for index_draw, draw in enumerate(draws_sorted):
        
        count = 1
        
        sequential_draw = {sequence: 0 for sequence in range(1, balls_drawn+1)}
        
        for index, number in enumerate(draw):
            if index != 0: 
                if draw[index-1] == number-1:
                    count += 1
                else:
                    qty_sequential[count] += 1
                    sequential_draw[count] += 1
                    count = 1
        
        qty_sequential[count] += 1
        sequential_draw[count] += 1
        
        sequential_draws_dict[index_draw] = sequential_draw
        
    return qty_sequential, sequential_draws_dict

def get_numbers_to_bet(ball_frequency_sorted_dict, qty_numbers_bet):
    
    balls_sorted = list(ball_frequency_sorted_dict.keys())
    balls_bet = balls_sorted[:qty_numbers_bet]
    balls_bet.sort()
    
    filename = 'numbers_to_bet.txt'
    with open(filename, 'w') as f:
        f.write(f"{balls_bet}")

    return balls_bet
    
def main():
    # Get real data from csv file
    filename = 'data/loto_facil_compiled_draws_2354.csv'
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
    ball_frequency_dict = {ball: frequency for ball, frequency in 
                           zip(balls, real_frequencies)}
    # make_plot(list(ball_frequency_dict.keys()), 
    #           list(ball_frequency_dict.values()), 
    #           "real_balls_draw", "Real Balls Draw")
    
    # Sort low to high frequencies of balls
    ball_frequency_sorted_dict = dict(sorted(ball_frequency_dict.items(), 
                                        key=itemgetter(1)))
    balls_sorted = [f'{ball}' for ball in 
                    list(ball_frequency_sorted_dict.keys())]
    # make_plot(balls_sorted, list(ball_frequency_sorted_dict.values()), 
    #           "real_balls_sorted", "Real Balls Sorted")

    # Simulate 1,000,000 of draws, total frequency of ball draw and plot 
    # # the simulated frequencies
    # number_draws = 1_000_000
    # simulated_draws = get_simulated_data(number_draws, lower_ball, 
    #                                      higher_ball, balls_drawn)
    # simulated_frequencies = get_frequencies(simulated_draws, balls)
    # make_plot(balls, simulated_frequencies, "simulated_balls_draw", 
    #         "Simulated 1,000,000 Draws")

    # Verify the ocurrence of sequential numbers, total and per draw.
    draws_sorted = get_draws_integer_sorted(draws)
    qty_sequential, sequential_draws_dict = \
        get_qty_sequential_numbers(draws_sorted, balls_drawn)
    # make_plot(list(qty_sequential.keys()), list(qty_sequential.values()), 
    #           "sequential_numbers", "Quantity of sequential numbers")
    
    for key, value in sequential_draws_dict.items():
        print(key, value)

    # # Choose numbers to bet
    # qty_numbers_bet = 15
    # print(get_numbers_to_bet(ball_frequency_sorted_dict, qty_numbers_bet))
    
if __name__ == "__main__":
    main()