import time

import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees
from anki_vector import lights as lght
from anki_vector import color


with anki_vector.Robot() as robot:
    robot.screen.set_screen_to_color(anki_vector.color.Color(rgb=[255, 128, 0]), duration_sec=10000)