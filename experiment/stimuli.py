import numpy as np
from psychopy.visual import TextStim, Line, RadialStim


class FixationLines(object):

    def __init__(self, win, circle_radius, color, line_width, *args, **kwargs):
        self.color = color
        self.line_width = line_width
        self.line1 = Line(win, start=(-circle_radius, -circle_radius),
                          end=(circle_radius, circle_radius), lineColor=self.color, lineWidth=self.line_width, *args, **kwargs)
        self.line2 = Line(win, start=(-circle_radius, circle_radius),
                          end=(circle_radius, -circle_radius), lineColor=self.color, lineWidth=self.line_width, *args, **kwargs)

    def draw(self):
        self.line1.draw()
        self.line2.draw()

    def setColor(self, color):
        self.line1.color = color
        self.line2.color = color
        self.color = color

        
