'''
Written by Liam Dwinnell
Last Updated: 7/12/2022
Planned Features:
 - get text of image for vetting non-englsih posts (higher quality following per like)
 - reserve time / make a bot for liking followers/following
    - unfollow accounts that do not like your posts after a certain period (most efficient follower feed)
 - detect device activity and avoid running during active times
'''

from cgi import test
from pynput.mouse import Button, Controller
mouse = Controller()

from pynput.keyboard import Key, Controller
keyboard = Controller()

import time
import random
import pyautogui

def move_and_click(x, y, clicks):
    mouse.position = (x, y)
    mouse.click(Button.left, clicks)

#starts a program given the name as a string
def start_program(name):
    time.sleep(2)
    if name == "chrome":
        move_and_click(230, 1100, 1)
    else:
        keyboard.press(Key.cmd_l)
        keyboard.release(Key.cmd_l)
        time.sleep(2)
        keyboard.type(name)
        time.sleep(1)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    time.sleep(2)
    
def goto_url(url):
    time.sleep(.5)
    mouse.position = (250, 70)
    mouse.click(Button.left, 2)
    keyboard.press(Key.ctrl.value)
    keyboard.press('a')
    keyboard.release(Key.ctrl.value)
    keyboard.release('a')
    keyboard.type(url)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

#searches webpage for text and scrolls to it
def cmd_f_string(search):
    keyboard.press(Key.ctrl.value)
    keyboard.press('f')
    keyboard.release(Key.ctrl.value)
    keyboard.release('f')
    time.sleep(1)
    keyboard.type(search)

def like_most_recent_from_hashtag(hashtag, like_count, testing=False):
    base_hashtag_url = "https://www.instagram.com/explore/tags/"
    goto_url(base_hashtag_url+hashtag+'/')
    time.sleep(12)
    cmd_f_string("most recent")
    time.sleep(1)
    move_and_click(295, 660, 1)
    time.sleep(2)
    mouse.position = (471, 414)
    for i in range(like_count):

        if testing==False:
            #like the post
            move_and_click(471, 414, 2)

        #wait for like action to register
        time.sleep(random.randint(1,2))

        #go to next post
        keyboard.press(Key.right)
        keyboard.release(Key.right)

        #wait for post to load
        time.sleep(random.randint(2,6))

        #before going to the next post make sure chrome is not in fullscreen
        if pyautogui.pixelMatchesColor(1200, 25, (43, 55, 61)) == False:
            keyboard.press(Key.f11)
            keyboard.release(Key.f11)
        
        time.sleep(1)
    
    #like the last post before finishing the thread session
    move_and_click(471, 414, 2)

    #make sure not fullscreen on video by going to next post before ending code
    keyboard.press(Key.right)
    keyboard.release(Key.right)

    #before going to the next post make sure chrome is not in fullscreen
    if pyautogui.pixelMatchesColor(1200, 25, (43, 55, 61)) == False:
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)

###ADJUSTABLE VARIABLES###

#Hashtags to like the 'most recent' posts (make these relevant to your insta page) 
todo_tags = [ "anime", "animelover", "animegirl", "animeart", "animefan", "animefans", "animecommunity", "animeworld", "animenation", "like4likes" ]
            #"anime", "animefans", "manga", "aiart", "painting", "instaart"

###NOTES###
#threads_per_session*likes_per_thread*17=maximum_daily_likes
#the above formula gives the hypothetical max likes at the current set rate. The internet says anywhere from 700 to 1000 will flag you
#try to keep it under 

#number of threads to explore per session
threads_per_session = 7 #2

#number of posts to like per thread
likes_per_thread = 10 #14

#number of minutes between cycles
minute_cycle_len = 90 #120

###DEV PARAMS###
#no liking
testing = False

#only like posts during the day
time_boundary = False

#allow for more frequent sessions for testing purposes
session_restraint = True

#do not start a session upon running the program (wait minute_cycle_len length of time)
safe_start = False

#do not include random extra time between sessions if false
cycle_variability = True

fluctuation_minutes = 20

###MAIN CODE###

hypo_daily_max = threads_per_session*likes_per_thread*17*(60/minute_cycle_len)
if hypo_daily_max < 3000 or session_restraint == False:

    print(hypo_daily_max, " is the daily max likes at current rate.")

    if safe_start == True:
        print("Running safe start: ", minute_cycle_len, " minutes long.")
        time.sleep(minute_cycle_len*60)

    while True:
        #get current hour in 24 hour time
        timestamp = int(time.strftime('%H'))
        deepstamp = time.strftime('%H:%M:%S')

        #if the time is between 6 AM and 11 PM 
        if timestamp >= 5 and timestamp <= 23 or time_boundary == False:
            
            print("Session Started at ", deepstamp, "...")

            #starts a blank chrome window
            start_program("chrome")

            #loops for the number of threads to do
            for i in range(threads_per_session):
                #go to a randomly selected thread and like some most recent posts
                temp_thread = todo_tags[random.randint(0,len(todo_tags)-1)]
                like_most_recent_from_hashtag(temp_thread, likes_per_thread, testing)
                print("Attempted: ", temp_thread, " for ", likes_per_thread, " likes.")
                time.sleep(3)
            print()

            #before going to the next post make sure chrome is not in fullscreen
            if pyautogui.pixelMatchesColor(1200, 25, (43, 55, 61)) == False:
                keyboard.press(Key.f11)
                keyboard.release(Key.f11)

            #exit chrome to clean things up
            move_and_click(1875, 10, 1)

            #reset mouse so it is not over x button of any other windows >:D
            mouse.position = (500,500)

            #sleep for the minute cycle length with slight deviation (maybe throws off bot detection???)
            time_to_next_session = minute_cycle_len*60
            if cycle_variability == True: time_to_next_session += random.randint(0,30*fluctuation_minutes)
            temptime = time.strftime('%H:%M:%S')
            print(time_to_next_session/60, " minutes until next session. Currently it is ", temptime)
            time.sleep(time_to_next_session)
        else:
            #check if it is the appropriate time every 15 minutes
            print(deepstamp, "is not an acceptable time to like posts... checking time again in 30 minutes.")
            time.sleep(30*60)
else:
    print("daily max is set too high at ", hypo_daily_max)