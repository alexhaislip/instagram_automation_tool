from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from util import check_exists_by_xpath,navigateToProfile,searchUser,alreadyGathered,alreadyFollowing,alreadyFollowed,validUser
from selenium.webdriver.common.keys import Keys
import time
import settings

instagramHomePath = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a'
suggestionsPath = '//*[@id="react-root"]/section/main/section/div[3]/div[3]/div[1]/a'

def gatherSuggestions(driver):
    # if(check_exists_by_xpath(driver,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span',2)):
    #     userFollowersLink = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
    #     userFollowersLink.click()
    # # scroll down until suggestions link
    # while True:
    #     try:
    #         if(check_exists_by_xpath(driver, '/html/body/div[3]/div/div[2]/div[4]/a',2)):
    #             suggestionLink = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[4]/a')
    #             suggestionLink.click()
    #             break;
    #     except StaleElementReferenceException:
    #         try:
    #             driver.execute_script(
    #                 "arguments[0].scrollTop = arguments[0].scrollHeight", suggestionLink
    #             )
    #             time.sleep(1)
    #         except StaleElementReferenceException:
    #             continue

    if (check_exists_by_xpath(driver, instagramHomePath, 2)):
        homePage = driver.find_element_by_xpath(instagramHomePath)
        homePage.click()

    if (check_exists_by_xpath(driver, suggestionsPath, 2)):
        homePage = driver.find_element_by_xpath(suggestionsPath)
        homePage.click()

    #driver.refresh()
    while(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/div[2]/div/div/div[100]',2) == False):
        t_end = time.time() + 9
        while (time.time() < t_end):
            driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)

    usernames = []
    x = 1;
    while x < 80:
        currentSuggestion = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/div/div/div[' + str(x) + ']')
        currentText = (currentSuggestion.text).split()
        usernames.append(currentText[0])
        x += 1

    return usernames

def gatherFromUsernameList(driver, list):
    navigateToProfile(driver)

    for user in list:
        if((len(settings.allGathered)) >= settings.gatherCount):
            break
        
        print(str(user) + "--------------------------------------------------")

        layerAllowance = settings.layerDepth

        userLink = searchUser(driver, user)
        if(userLink == 1):
            continue
        while True:
            try:
                userLink.click()
                break
            except StaleElementReferenceException:
                continue
        # This refresh handles an unknown error with finding the followers link element
        driver.refresh()
        
        if((len(settings.allGathered)) < settings.gatherCount and alreadyGathered(user)==False and alreadyFollowing(user)==False and validUser(driver)==True):
            #print(user + " already following us")
            print(str(user) + " is valid")
            settings.allGathered.append(user)
            print("currently gathered: ", settings.allGathered)

        else:
            print(str(user) + " NOT VALID")
        # if follower link is clickable(account is not private), click it, otherwise continue
        if(check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a',1)):
            userFollowersLink = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
            userFollowersLink.click()
        else:
            continue

        users = []
        if(check_exists_by_xpath(driver, '/html/body/div[3]/div/div[2]/ul', 2) == False):
            continue
        try:
            followerlistElement = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
        except NoSuchElementException:
            continue
        followerElements = followerlistElement.find_elements_by_tag_name('li')
        for i in range(min(settings.recursiveDepth, len(followerElements))):
            currentUserText = (followerElements[i].text).split()
            if(currentUserText[-1] == "Follow"):
                users.append(currentUserText[0])


        # Here starts the recursive gather
        recursiveGather(driver, users, settings.recursiveDepth, layerAllowance)

def recursiveGather(driver, list, recursiveDepth, layerAllowance):

    for user in list:
        
        if (layerAllowance <= 0 or len(settings.allGathered) >= settings.gatherCount):
            break
        print(str(user) + "--------------------------------------------------")

        userLink = searchUser(driver, user)
        if (userLink == 1):
            continue
        while True:
            try:
                userLink.click()
                break
            except StaleElementReferenceException:
                continue
        # This refresh handles an unknown error with finding the followers link element
        driver.refresh()
        
        if((len(settings.allGathered)) < settings.gatherCount and alreadyGathered(user)==False and alreadyFollowing(user)==False and validUser(driver)==True):
            #print(user + " already following us")
            print(str(user) + " is valid")
            settings.allGathered.append(user)
            print("currently gathered: " + settings.allGathered)
        else:
            print(str(user) + " NOT VALID")

        # if follower link is clickable(account is not private), click it, otherwise continue
        if (check_exists_by_xpath(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a', 1)):
            userFollowersLink = driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
            userFollowersLink.click()
        else:
            continue

        users = []
        if (check_exists_by_xpath(driver, '/html/body/div[3]/div/div[2]/ul', 2) == False):
            continue
        try:
            followerlistElement = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
        except NoSuchElementException:
            continue
        followerElements = followerlistElement.find_elements_by_tag_name('li')
        for i in range(min(settings.recursiveDepth, len(followerElements))):
            currentUserText = (followerElements[i].text).split()
            print(currentUserText)
            if(currentUserText[-1] == "Follow"):
                users.append(currentUserText[0])

        recursiveGather(driver, users, recursiveDepth, layerAllowance-1)
