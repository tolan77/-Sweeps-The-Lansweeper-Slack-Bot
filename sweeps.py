import time
from slackclient import SlackClient
from selenium import webdriver

# Token and ID

SLACK_BOT_TOKEN = ''  # Put Token Here
BOT_ID = ''  # Put Bot ID here


# constants
AT_BOT = "<@" + BOT_ID + ">"
HELP_COMMAND = "help"
STATUS_COMMAND = "status"
CHECKIN_COMMAND = "checkin"
CHECKOUT_COMMAND = "checkout"

# instantiate Slack clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Open chromedriver and navigate to lansweeper for later use
browser = webdriver.Chrome()
browser.get('http://lansweeper/')


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = ("Not sure what you mean.Type @sweeps *" + HELP_COMMAND + "* to"
                " see what I can do")
    if command.startswith(HELP_COMMAND):
        response = help_command(command[len(HELP_COMMAND):].strip())
    if command.startswith(STATUS_COMMAND):
        response = status_command(command[len(STATUS_COMMAND):].strip())
    if command.startswith(CHECKIN_COMMAND):
        response = checkin_command(command[len(CHECKIN_COMMAND):].strip())
    if command.startswith(CHECKOUT_COMMAND):
        response = checkout_command(command[len(CHECKOUT_COMMAND):].strip())
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def help_command(query_as_str):

    if query_as_str == 'status':
        resp = ("The *" + STATUS_COMMAND + "* command returns the status of an"
                " asset in lansweeper. Use it by typing @sweeps *" +
                STATUS_COMMAND + "* <gbxtag>")
    if query_as_str == 'checkin':
        resp = ("The *" + CHECKIN_COMMAND + "* command checks the given tag "
                "into the 5TH FLOOR IT WORKROOM in lansweeper and removing all"
                " previous associations. Use it by typing @sweeps *" +
                CHECKIN_COMMAND + "* <gbxtag>")
    if query_as_str == 'checkout':
        resp = ("The *" + CHECKOUT_COMMAND + "* command checks the given tag "
                "out to the contact and location provided. Use it by typing "
                "@sweeps *" + CHECKIN_COMMAND + "* <gbxtag>,<contact>,"
                "<location> The contact will be saved as both a contact and "
                "tagged as a user relation. Must have both a contact and "
                "location or the bot will fail")
    else:
        resp = ("The current commands I can do are *" + STATUS_COMMAND +
                "*, *" + CHECKIN_COMMAND + "*, *" + CHECKOUT_COMMAND +
                "*. Type @sweeps *help* <command> to find out more about a "
                "particular command")
    return resp


def status_command(gbxtag_as_str):
    """
        This command will navigate to the edit asset page on lansweeper
        and return the asset name,serial num, and contact/location
    """
    thepowerofchristcompelsyou = 1
    gbxtag = gbxtag_as_str
    # This next step navigates to the searchform at the top of the lansweeper
    # page. Clears it and searches for the gbxtag provided.
    searchform = browser.find_element_by_xpath(".//*[@id='q']")
    searchform.clear
    searchform.send_keys(gbxtag)
    searchform.submit()

    try:
        # This part clicks the "edit asset" link on the top left if the gbxtag
        # returned a result
        editassetclick = browser.find_element_by_xpath(
            ".//*[@id='assetMenuLeft']/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a")
        editassetclick.click()
    except:
        # This is an exemption if the gbxtag does not return a specific item
        thepowerofchristcompelsyou = 2

    # This following if statement will only run the following if the previous
    # try statement succeeded
    if thepowerofchristcompelsyou != 2:
        # This part stores the info about the item for a status check.
        assetname = browser.find_element_by_xpath(".//*[@id='assetname']")
        assetnamebyte = assetname.get_attribute('value').encode('utf-8')
        assetnamestr = assetnamebyte.decode('utf-8')
        serialnum = browser.find_element_by_xpath(".//*[@id='serial']")
        serialnumbyte = serialnum.get_attribute('value').encode('utf-8')
        serialnumstr = serialnumbyte.decode('utf-8')
        locationname = browser.find_element_by_xpath(".//*[@id='location']")
        locationnamebyte = locationname.get_attribute('value').encode('utf-8')
        locationnamestr = locationnamebyte.decode('utf-8')
        contactname = browser.find_element_by_xpath(".//*[@id='contact']")
        contactnamebyte = contactname.get_attribute('value').encode('utf-8')
        contactnamestr = contactnamebyte.decode('utf-8')

        resp = ("Tag : " + gbxtag + " is an " + assetnamestr + "Serial : " +
                serialnumstr + " is registered to " + locationnamestr +
                " contact " + contactnamestr + " for more info.")

        # This part clicks the "save asset" link on the top left
        saveassetclick = browser.find_element_by_xpath(
            ".//*[@id='asaveasset']")
        saveassetclick.click()

    # This final else catches if an item was not found
    else:
        thepowerofchristcompelsyou = 1
        resp = "Maybe you made a typo, could not find an item tied to " + \
            gbxtag + " There may be a tag mismatch"

    return resp


def checkin_command(gbxtag_as_str):
    """
        This command will navigate to the edit asset page on lansweeper
        ,change the contact and location to "5TH FLOOR IT STORAGE ROOM
        and remove any associated user relations
    """
    gbxtag = gbxtag_as_str
    theteachingsofbuddha = 1
    # This step navigates to the searchform at the top of the lansweeper
    # page. Clears it and searches for the gbxtag provided.
    searchform = browser.find_element_by_xpath(".//*[@id='q']")
    searchform.clear
    searchform.send_keys(gbxtag)
    searchform.submit()

    try:
        # This part clicks the "edit asset" link on the top left if the gbxtag
        # returned a result
        editassetclick = browser.find_element_by_xpath(
            ".//*[@id='assetMenuLeft']/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a")
        editassetclick.click()
    except:
        # This is an exemption if the gbxtag does not return a specific item
        theteachingsofbuddha = 2

    # This following if statement will only run the following if the previous
    # try statement succeeded
    if theteachingsofbuddha != 2:
        # This part navigates to the contact form on the edit page, clears
        # anything that was in it, and then types in
        # "5th Floor IT Storage room"
        contactform = browser.find_element_by_xpath(".//*[@id='contact']")
        contactform.clear()
        contactform.send_keys('5th Floor IT Storage Room')

        # This part navigates to the location form on the edit page, clears
        # anything that was in it, and then types in
        # "5th Floor IT Storage room"
        locationform = browser.find_element_by_xpath(".//*[@id='location']")
        locationform.clear()
        locationform.send_keys('5th Floor IT Storage Room')

        # This part tries to remove an associated user in "User Relations"
        # and if there isn't one continues to the next step
        try:
            removeuser = browser.find_element_by_xpath(
                ".//*[@id='userRelationsTable']/tbody/tr/td[7]/a/img")
            removeuser.click()

        except:
            pass

        # This part stores the information about the item being inventoried
        # to double check there isn't a tag mismatch
        assetname = browser.find_element_by_xpath(".//*[@id='assetname']")
        assetnamebyte = assetname.get_attribute('value').encode('utf-8')
        assetnamestr = assetnamebyte.decode('utf-8')
        serialnum = browser.find_element_by_xpath(".//*[@id='serial']")
        serialnumbyte = serialnum.get_attribute('value').encode('utf-8')
        serialnumstr = serialnumbyte.decode('utf-8')

        # This part clicks the "save asset" link on the top left
        saveassetclick = browser.find_element_by_xpath(
            ".//*[@id='asaveasset']")
        saveassetclick.click()

        resp = ("Tag: " + gbxtag + " a " + assetnamestr + " with serial " +
                serialnumstr + " has been checked in to the workroom")
    # This else catches if the item was not found in lansweeper.
    else:
        theteachingsofbuddha = 1
        resp = ("Maybe you made a typo, could not find an item tied to " +
                gbxtag + " There may be a tag mismatch")
    return resp


def checkout_command(commandstr):
    gbxtag, user, locat = commandstr.split(",")
    thegloriousleadersays = 1

    # This step navigates to the searchform at the top of the lansweeper page.
    # Clears it and searches for the gbxtag provided.
    searchform = browser.find_element_by_xpath(".//*[@id='q']")
    searchform.clear
    searchform.send_keys(gbxtag)
    searchform.submit()

    try:
        # This part clicks the "edit asset" link on the top left if the gbxtag
        # returned a result
        editassetclick = browser.find_element_by_xpath(
            ".//*[@id='assetMenuLeft']/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a")
        editassetclick.click()
    except:
        # This is an exemption if the gbxtag does not return a specific item
        thegloriousleadersays = 2

    # This following if statement will only run the following if the previous
    # try statement succeeded
    if thegloriousleadersays != 2:
        # This part navigates to the contact form on the edit page, clears
        # anything that was in it, and then types in the users name given above
        contactform = browser.find_element_by_xpath(".//*[@id='contact']")
        contactform.clear()
        contactform.send_keys(user)

        # This part navigates to the location form on the edit page,and clears
        # anything that was in it
        locationform = browser.find_element_by_xpath(".//*[@id='location']")
        locationform.clear()
        locationform.send_keys(locat)
        # This part tries to remove an associated user in "User Relations" and
        # if there isn't one continues to the next step
        try:
            removeuser = browser.find_element_by_xpath(
                ".//*[@id='userRelationsTable']/tbody/tr/td[7]/a/img")
            removeuser.click()

        except:
            pass

        # This part tries to add the user given above as an associated user in
        # "User Relations"
        usedby = browser.find_element_by_xpath(
            ".//*[@id='addUserRelationTypeSelect']/option[11]")
        usedby.click()

        selectuser = browser.find_element_by_xpath(
            ".//*[@id='addUserRelationParentSelect']/option[2]")
        selectuser.click()

        time.sleep(1)
        adduser = browser.find_element_by_xpath(".//*[@id='usertxt']")
        adduser.send_keys(user)

        time.sleep(2)
        clickuser = browser.find_element_by_xpath(
            ".//*[@id='userSelect']/option")
        clickuser.click()

        saveclickeduser = browser.find_element_by_xpath(
            "html/body/div[7]/div[3]/div/button[1]")
        saveclickeduser.click()

        adduserrelation = browser.find_element_by_xpath(
            ".//*[@id='addUserRelationButton']")
        adduserrelation.click()

        # This part stores the information about the item being inventoried to
        # double check there isn't a tag mismatch
        assetname = browser.find_element_by_xpath(".//*[@id='assetname']")
        assetnamebyte = assetname.get_attribute('value').encode('utf-8')
        assetnamestr = assetnamebyte.decode('utf-8')
        serialnum = browser.find_element_by_xpath(".//*[@id='serial']")
        serialnumbyte = serialnum.get_attribute('value').encode('utf-8')
        serialnumstr = serialnumbyte.decode('utf-8')

        # This part clicks the "save asset" link on the top left
        saveassetclick = browser.find_element_by_xpath(
            ".//*[@id='asaveasset']")
        saveassetclick.click()

        resp = ("Tag: " + gbxtag + " a " + assetnamestr + " with serial " +
                serialnumstr + " has been registered to " + user +
                "in location " + locat)
    # This else catches if the item was not found in lansweeper.
    else:
        thegloriousleadersays = 1
        resp = ("Maybe you made a typo, could not find an item tied to " +
                gbxtag + " There may be a tag mismatch")

    return resp


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Sweeps ready for action!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
