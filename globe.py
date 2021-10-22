from random import choice

class Globe:
    """A class that represents a globe to draw balls.
    """    
    def __init__(self, lower_ball=1, higher_ball=25, balls_drawn=15):
        # Create all the balls as a list and decide how many balls to be 
        # drawn.
        self.lower_ball = lower_ball
        self.higher_ball = higher_ball
        self.balls = list(range(lower_ball, higher_ball+1))
        self.balls_drawn = balls_drawn
        self.draw = []
    
    # Method to run the draw.
    def run_drawn(self):
        balls = self.balls
        for ball in range(self.balls_drawn):
            ball_drawn = choice(balls)
            self.draw.append(ball_drawn)
            balls.remove(ball_drawn)
    
    # Refresh balls into the globe
    def refresh_balls(self):
        self.balls = list(range(self.lower_ball, self.higher_ball+1))
        self.draw = []