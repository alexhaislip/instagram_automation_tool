from util import needToUnfollow, unfollow, actionWait, follow

def preformAction(driver):
        
    if(needToUnfollow()):
        unfollow(driver)
        actionWait(driver, False)
    else:
        follow(driver)
        actionWait(driver, False)
