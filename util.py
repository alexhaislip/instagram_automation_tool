from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from files import fileContains, removeAndReturn, appendToFile
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import PySimpleGUI as ag
import settings
from datetime import datetime

profileButtonPath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a'
notificationsButtonPath = "/html/body/div[4]/div/div/div[3]/button[2]"
exitFollowersPopupPath = '/html/body/div[4]/div/div[1]/div/div[2]/button'

def login(driver):
    # navigate to instagram login
    driver.get("https://www.instagram.com/accounts/login/");
    # locate username and password boxes
    usernameBox = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/'
        'div/label/input')
    passwordBox = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]'
        '/div/label/input')
    # type in and submit
    time.sleep(1)
    usernameBox.send_keys(settings.username)
    passwordBox.send_keys(settings.password)
    loginSubmit = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]'
        '/button')
    loginSubmit.click()
    # handle suspicious login
    if (check_exists_by_xpath(driver, '//*[@id="react-root"]/section/div/div/div[3]/form/div/div[2]/label', 4) == True):
        phoneNumberSelect = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/div/div[2]/'
                                                         'label')
        phoneNumberSelect.click()
        sendCodeButton = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[3]/form/span/button')
        sendCodeButton.click()
        securityLayout = [[ag.Text('Security Code')],
                          [ag.InputText()],
                          [ag.Button('Submit')]]

        securityWindow = ag.Window('Suspicious Login Handler: Instagram noticed a suspicious '
                                   'login with the account. A security code was sent to the '
                                   'Phone number associated with the account').Layout(securityLayout)
        buttonText, code = securityWindow.Read()
        securityWindow.Close()
        securityCodeInput = driver.find_element_by_xpath('//*[@id="security_code"]')
        securityCodeInput.send_keys(code)
        codeSubmit = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div/div[2]/form/span/button')
        codeSubmit.click()
    # navigate to account profile
    if (check_exists_by_xpath(driver, notificationsButtonPath, 3) == True):
        notificationspopup = driver.find_element_by_xpath(notificationsButtonPath)
        notificationspopup.click()

    navigateToProfile(driver)

def navigateToProfile(driver):
    driver.refresh()
    time.sleep(1)
    if(check_exists_by_xpath(driver, profileButtonPath, 2) == True):
        profilePage = driver.find_element_by_xpath(profileButtonPath)
        profilePage.click()
    else:
        print("profile element not found")

def check_exists_by_xpath(driver, xpath, waitTime):
    wait = WebDriverWait(driver, waitTime)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        return False
    return True

def searchUser(driver, user):

    if(check_exists_by_xpath(driver,exitFollowersPopupPath,3)):
        exitPopup = driver.find_element_by_xpath(exitFollowersPopupPath)
        exitPopup.click()

    searchBar = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    searchBar.clear()
    for letter in user:
        while(True):
            try:
                searchBar.send_keys(letter)
                break
            except StaleElementReferenceException:
                continue
    time.sleep(1.2)
    # ///////////////////////////////////////pause////////////////////get rid of this eventuallyxs
    if (check_exists_by_xpath(driver, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div', 2)):
        dropDown = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div')
        dropDownElements = dropDown.find_elements_by_tag_name('a')
        result = 1
        # handle exception of username not matching topmost selection of drop down
        for userLink in dropDownElements:
            while(True):
                try:
                    dropDownText = (userLink.text).split()
                    break
                except StaleElementReferenceException:
                    continue
            if (dropDownText[0] == user):
                result = userLink
                break
    else:
        #print(user + " does not exist")
        return 1
    return result

def alreadyGathered(user):
    if user in settings.allGathered:
        return True
    else:
        return False

def alreadyFollowing(user):
    if(fileContains('followers.txt', user)):
        return True
    else:
        return False

# must be on profile page of user for this to work
def alreadyFollowed(driver):
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button', 2)):
        return False
    else:
        return True

def closeSearchPopup(driver):
    if (check_exists_by_xpath(driver, '/html/body/div[3]/div/div[1]/div/div[2]/button/span', 1)):
        exitPopup = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[2]/button/span')
        exitPopup.click()

def needToUnfollow():
    with open("unfollow_pending.txt") as file:
        line = file.readline()
        if(len(line) < 3):
            return False
        parts = line.split()
        user, year, month, day, hour, minute, second = [parts[i] for i in (0,1,2,3,4,5,6)]
        userDate = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        if(datetime.now() > userDate):
            return True
        else:
            return False

def unfollow(driver):

    with open('unfollow_pending.txt', 'r') as fin:
        data = (fin.readlines())
        user = ((data[0]).split())[0]
    with open('unfollow_pending.txt', 'w') as fout:
        fout.writelines(data[1:])

    if(user.endswith('\n')):
        user = user[:-1]
    userLink = searchUser(driver, user)
    if (userLink == 1):
        return 1
    while True:
        try:
            userLink.click()
            break
        except StaleElementReferenceException:
            continue

    # Here we press unfollow and then unfollow on the are you sure page
    time.sleep(2)
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button',2)):
        unfollowElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
        text = unfollowElement.text
    elif(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button',2)):
        unfollowElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        text = unfollowElement.text
    else:
        print("unfollow error")
        return 1
    
    if(text == "Following" or text == "Requested"):
        unfollowElement.click()
        areYouSureElement = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
        areYouSureElement.click()
        print("unfollowed " + str(user))
    else:
        print(str(user) + " Action Button does not read 'Following' or 'Requested'")
        return 1
    return 0

def follow(driver):
    user = removeAndReturn("pending.txt")

    userLink = searchUser(driver, user)
    if (userLink == 1):
        print("append error")
        return 1
    while True:
        try:
            userLink.click()
            break
        except StaleElementReferenceException:
            continue
        
    # This refresh handles an unknown error with finding the followers link element
    #######################driver.refresh()
    ######################time.sleep(0.5)
    
    time.sleep(2)
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button',2)):
        followElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
        text = followElement.text
    elif(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button',2)):
        followElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        text = followElement.text
    else:
        print("Follow Error")
        return 1
    
    if(text == "Follow"):
        followElement.click()
        print('following ' + str(user))
        appendToFile("unfollow_pending.txt", user, True)
    else:
        print(str(user) + " Action Button does not read 'Follow'")
        return 1
    return 0
    
def actionWait(driver, isTest):
    if(isTest == False):
        i = 0
        while (i < 100):
            if((i % 2) == 0 ):
                driver.refresh()
            time.sleep(((24 * 60 * 60) / settings.actionsPerDay) / 100)
            i += 10
    else:
        time.sleep(1)
        
# Use only when on somebodys profile page
def validUser(driver):
    
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/button',2)):
        followElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
        text = followElement.text
    elif(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button',2)):
        followElement = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        text = followElement.text
    
    print("text is... " + text)
    if(text != "Follow"):
        return False
    
    numFollowers = str(1)
    numFollowed = str(1)
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a',2)):
        followersLink = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        numFollowers = ((followersLink.text).split())[0]
    if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a',2)):
        followedLink = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        numFollowed = ((followedLink.text).split())[0]
        
    numFollowers = numFollowers.replace(',','')
    numFollowed = numFollowed.replace(',','')
    
    if(numFollowers.endswith('k') or numFollowers.endswith('m')):
        return True
    elif(int(numFollowers) == 0 or int(numFollowed) == 0):
        print("no followers or followings")
        return False
    elif((int(numFollowers)*0.15) > int(numFollowed)):
        print("bad ratio")
        return False
    
    return True
