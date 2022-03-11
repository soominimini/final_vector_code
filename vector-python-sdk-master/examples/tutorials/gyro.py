from multiprocessing import Process
import threading
import time
import anki_vector
from anki_vector.events import Events
from anki_vector import util
from anki_vector import behavior
from anki_vector.util import *
from anki_vector.behavior import *
from anki_vector import connection

import asyncio

import speech_recognition as sr
import pyaudio
import wave

import sys; sys.path.append('..') # help python find pylsl relative to this example program
from pylsl import StreamInfo, StreamOutlet,StreamInlet, resolve_stream
import time
from anki_vector.connection import ControlPriorityLevel

def loca(cur_degree):
    print("cur_degree :",cur_degree)
#동 : 0  서 : -180 북 : 90 남 :-90
if __name__ == '__main__':
    with anki_vector.Robot(config={"cert": "C:/Users/Hyunseung/.anki_vector/Vector-C1G1-00a10bb4.cert", "name": "Vector-C1G1" },behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY , cache_animation_lists=True) as robot:
        time.sleep(1)
        print(robot.pose)
        robot.behavior.turn_in_place(degrees(90))
        print(robot.pose)
        robot.behavior.drive_straight(distance_mm(200), speed_mmps(150))
        print(robot.pose)
        robot.behavior.drive_straight(distance_mm(200), speed_mmps(150))
        print(robot.pose)

        if robot.pose.position.x >-90:
            print("오른쪽으로 넘어갔을 떄")
            target = abs(robot.pose.position.x) - 90
            robot.behavior.turn_in_place(degrees(target))
        else:
            target = 90-abs(robot.pose.position.x)
            robot.behavior.turn_in_place(degrees(-target))