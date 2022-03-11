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
from retrying import retry

import math
info = StreamInfo('Vector', 'Markers', 1, 0, 'string', 'myuidw43536')
outlet = StreamOutlet(info)

wake_word_heard = False
wake_word_heard2 = False
wake_word_heard3 = False
wake_word_heard4 = False
wake_word_heard5 = False
wake_word_heard6 = False
wake_word_heard7 = False
wake_word_heard8 = False

wake_word_heard_sk = False
Face = False

#동 : 0  서 : -180 북 : 90 남 :-90

def location(cur_degree, target_degree, robot):
    #다리에서 벗어나지 않게 하기 위한 function
    print("cur_degree: ",cur_degree)
    if target_degree==0:
        if cur_degree>target_degree:
            cur_degree= int(cur_degree)
            robot.behavior.turn_in_place(degrees(-cur_degree))
        else:
            cur_degree = int(cur_degree)
            robot.behavior.turn_in_place(degrees(cur_degree))
    elif target_degree==90: #90?
        if cur_degree>target_degree:
            target = cur_degree-90
            target = int(target)
            robot.behavior.turn_in_place(degrees(-target))
        else:
            target = 90-cur_degree
            target = int(target)
            robot.behavior.turn_in_place(degrees(target))

    elif target_degree==-90:
        if abs(cur_degree)>abs(target_degree):
            target = abs(cur_degree)-90
            target = int(target)
            robot.behavior.turn_in_place(degrees(target))
        else:
            target = 90-abs(cur_degree)
            target = int(target)
            robot.behavior.turn_in_place(degrees(-target))
    print("cur_degree: ", robot.pose.rotation.angle_z.degrees)




def first_bhvr():
    time.sleep(1)
    #말 기다리기
    time.sleep(3)
    print("sending markers...")
    outlet.push_sample(['Vector_Turned1'])
    robot.anim.play_animation('anim_eyepose_happy')
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.behavior.say_text("hi i'm vector" )
    # robot.anim.play_animation('anim_onboarding_reacttoface_happy_01_head_angle_40')
    robot.behavior.say_text("nice to meet you")


def second_bhvr():
    time.sleep(3)

    print("sending markers...")
    outlet.push_sample(['Vector_Turned2'])


    robot.behavior.say_text("of course!")  # 오른쪽에 있는 참가자를 바라보고 있는 상황
    # # Positive values turn to the left, negative values to the right.
    # robot.behavior.turn_in_place(degrees(90))  # or this can be placed with remote control
    # robot.behavior.drive_straight(distance_mm(200), speed_mmps(100))  # arrive on the spot
    # robot.behavior.turn_in_place(degrees(-90))  # 참가자를 바라보는 것으로 끝맺음

    # 앞으로 나온 로봇 다시 뒤로
    # robot.behavior.drive_straight()


def third_bhvr():
    time.sleep(5)

    print("sending markers...")
    outlet.push_sample(['Vector_Turned3'])

    robot.behavior.turn_in_place(degrees(94)) # 90 보다 더 돌려야 함
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    # robot.behavior.turn_in_place(degrees(-90))
    robot.anim.play_animation('anim_eyepose_sad_up')
    robot.behavior.say_text("it seems scary..")

def fourth_bhvr():
    time.sleep(3)

    print("sending markers...")
    outlet.push_sample(['Vector_Turned4'])
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_eyepose_sad_instronspect')
    robot.behavior.say_text("okay... i will try...")

    # robot.behavior.turn_in_place(degrees(90))
    robot.behavior.set_head_angle(degrees(45.0))
    robot.behavior.drive_straight(distance_mm(30), speed_mmps(20))
    location(robot.pose.rotation.angle_z.degrees,90,robot)

    robot.behavior.drive_straight(distance_mm(40), speed_mmps(20))
    location(robot.pose.rotation.angle_z.degrees,90, robot)

    # robot.behavior.turn_in_place(degrees(180))
    robot.behavior.drive_straight(distance_mm(-30), speed_mmps(100))
    # robot.behavior.turn_in_place(degrees(90))
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_eyepose_sad_down')
    robot.behavior.say_text("i cant' do this...")
def fifth_bhvr():
    time.sleep(5)

    print("sending markers...")
    outlet.push_sample(['Vector_Turned5'])
    robot.anim.play_animation('anim_eyepose_sad_up')
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.behavior.say_text("okay....")
    robot.behavior.drive_straight(distance_mm(15), speed_mmps(10))
    # robot.behavior.turn_in_place(degrees(90))
    # 여기에 뭔가 더 필요
    robot.behavior.drive_straight(distance_mm(-15), speed_mmps(50))
    location(robot.pose.rotation.angle_z.degrees,90, robot)


    print("sending markers...")
    outlet.push_sample(['Vector_Turned5_2'])
    robot.anim.play_animation('anim_eyepose_sad_instronspect')
    robot.behavior.turn_in_place(degrees(-90))
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_eyepose_worried')
    robot.behavior.say_text("sorry... i can't do this...")

def sixth_bhvr():
    time.sleep(6)
    print("sending markers...")
    outlet.push_sample(['Vector_Turned6'])

    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_eyepose_sad_instronspect')
    time.sleep(1)
    robot.behavior.say_text("but it is too scary..")

def seventh_bhvr():
    time.sleep(6)
    print("sending markers...")
    outlet.push_sample(['Vector_Turned7'])

    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_eyepose_determined')
    robot.behavior.say_text("Okay I will try!")
    time.sleep(0.5)
    robot.behavior.turn_in_place(degrees(90))
    robot.behavior.drive_straight(distance_mm(100), speed_mmps(50))
    location(robot.pose.rotation.angle_z.degrees,90, robot)
    robot.behavior.drive_straight(distance_mm(130), speed_mmps(100))
    location(robot.pose.rotation.angle_z.degrees,90, robot)
    # encounter

    outlet.push_sample(['Vector_Turned7_2'])

    robot.anim.play_animation('anim_reacttocliff_faceplantroll_armup_02', ignore_body_track=True)

    outlet.push_sample(['Vector_Turned7_3'])
    robot.anim.play_animation('anim_eyepose_sad_down')
    robot.behavior.drive_straight(distance_mm(-200), speed_mmps(300))  # run away
    location(robot.pose.rotation.angle_z.degrees,90, robot)
    # robot.behavior.turn_in_place(degrees(-90))
    robot.anim.play_animation('anim_eyepose_sad_up')
    robot.behavior.say_text("i was almost dead")


def eighth_bhvr():
    time.sleep(5)
    print("sending markers...")
    outlet.push_sample(['Vector_Turned8'])

    robot.behavior.say_text("okay! i will try again!")
    robot.behavior.turn_in_place(degrees(2))
    robot.behavior.drive_straight(distance_mm(150), speed_mmps(50))
    location(robot.pose.rotation.angle_z.degrees,90,robot)
    robot.behavior.drive_straight(distance_mm(150), speed_mmps(50))
    location(robot.pose.rotation.angle_z.degrees,93, robot)
    robot.behavior.drive_straight(distance_mm(300), speed_mmps(150))
    # location(robot.pose.rotation.angle_z.degrees,93, robot)
    # robot.behavior.drive_straight(distance_mm(150), speed_mmps(150))
    robot.behavior.turn_in_place(degrees(180))
    robot.behavior.set_head_angle(MAX_HEAD_ANGLE)
    robot.anim.play_animation('anim_onboarding_reacttoface_happy_01_head_angle_40')
    robot.behavior.say_text("i did it!!")

    print("sending markers...")
    outlet.push_sample(['end'])

def first():
    time.sleep(5)
    r = sr.Recognizer()
    print(robot.pose.rotation.angle_z)
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    try:
        speech = r.recognize_google(audio)
        if len(speech)>0:
            print("You said: " + r.recognize_google(audio))
            first_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    second()


def second():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print("여기서 막혔나")
        print("audio   : ",audio)

    # Speech recognition using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            second_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    third()

def third():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            third_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    fourth()


def fourth():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            fourth_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    fifth()


def fifth():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            fifth_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    sixth()

def sixth():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            sixth_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    seventh()

def seventh():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            seventh_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    robot.conn.request_control()
    eighth()


def eighth():
    time.sleep(1.5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        speech = r.recognize_google(audio)
        if len(speech) > 0:
            print("You said: " + r.recognize_google(audio))
            eighth_bhvr()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    robot.conn.request_control()

if __name__ == '__main__':

    with anki_vector.Robot(config={"cert": "C:/Users/Hyunseung/.anki_vector/Vector-C1G1-00a10bb4.cert", "name": "Vector-C1G1" },behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY , cache_animation_lists=True) as robot:
        time.sleep(5)
        print("sending markers...")
        outlet.push_sample(['start'])
        first()