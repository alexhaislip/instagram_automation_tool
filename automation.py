from selenium import webdriver
import time
from datetime import timedelta, datetime
import os
import PySimpleGUI as ag
from PySimpleGUI import SetOptions
from util import login, closeSearchPopup, navigateToProfile, needToUnfollow, unfollow
from files import appendListToFile
from gather import gatherSuggestions, gatherFromUsernameList
from action import preformAction
import settings 

def main():
    settings.init()
    
    print(os.path.getsize(os.getcwd() + "/unfollow_pending.txt"))
    print(os.path.getsize(os.getcwd() + "/pending.txt"))


    layout = [[ag.Text("Username",pad=(0,5)),
              ag.InputText(size=(20,1), default_text="")],
              [ag.Text("Password", pad=(0,5)),
              ag.InputText(size=(20,1), default_text="")],
              [ag.Text("Recursive Depth", pad=((0,0),(8,0))),
              ag.Slider(range=(2,10), orientation='h', size=(18,15), default_value=4, pad=(0,0), border_width=0)],
              [ag.Text("Recursive Layer", pad=(0,5)),
              ag.Slider(range=(3,20), orientation='h', size=(18,15), default_value=5, pad=(0,0), border_width=0)],
              [ag.Text("Gather Count",pad=(0,5)),
              ag.InputText(size=(10,1), pad=(0,5), default_text="40")],
              [ag.Text("Runtime( hours )", pad=(0, 5)),
              ag.Slider(range=(1, 300), orientation='h', size=(18, 15), default_value=50, pad=(0, 0), border_width=0)],
              [ag.Text("Actions each day", pad=(0, 5)),
               ag.Slider(range=(10, 500), orientation='h', size=(18, 15), default_value=5, pad=(0, 0), border_width=0)],
              [ag.Text("hours to unfollow", pad=(0, 5)),
               ag.Slider(range=(1, 120), orientation='h', size=(18, 15), default_value=50, pad=(0, 0), border_width=0)],
              [ag.Button("OK", size=(8,3), pad=(0,5))]]

    window = ag.Window('App Settings').Layout(layout)

    SetOptions(background_color='#9FB8AD')

    buttontext, values = window.Read()
    settings.username = values[0]
    settings.password = values[1]
    settings.recursiveDepth = int(values[2])
    settings.layerDepth = int(values[3])
    settings.gatherCount = int(values[4])
    settings.runTime = int(values[5])
    settings.actionsPerDay = int(values[6])
    settings.timeTillUnfollow = int(values[7])
    window.Close()

    driver = webdriver.Chrome(os.getcwd() + "/chromedriver");
    driver.implicitly_wait(2.5)
    # login into users account
    login(driver)
    driver.implicitly_wait(1)

    masterTime = datetime.now() + timedelta(minutes=settings.runTime)
    while(datetime.now() < masterTime):
        if(os.stat("pending.txt").st_size == 0):
            print("Gathering more users")
            gatherStartTime = datetime.now()
            closeSearchPopup(driver)
            navigateToProfile(driver)
            suggestionsNameList = gatherSuggestions(driver)
            gatherFromUsernameList(driver, suggestionsNameList)
            appendListToFile("pending.txt", settings.allGathered)
            settings.allGathered.clear()
            gatherFinishTime = datetime.now()
            masterTime += (gatherFinishTime - gatherStartTime)
            closeSearchPopup(driver)
            navigateToProfile(driver)
        else:
            preformAction(driver)

    time.sleep(10)
    driver.close()

if __name__== "__main__":
    main()
        