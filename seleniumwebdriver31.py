#selenium python web bindings provides a convenient APIto access selenium web drivers like Firefox,chrome and remote etc.

#import tkinter module
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedAlertPresentException

import tkinter as tk
import tkinter.messagebox as mbox
import time
import re
import sys

#Create the GUI application main window.
root = tk.Tk()       #The root window is created,its a main application window created in our programs.This is a window with a title bar and other decoration provided by the window manager.
root.title("Conclusion of SAS Key Issues using selenium Webdriver") # Add a title to the root window
root.geometry("1020x1020+50+50")               # The geometry() method sets a size for the window and positions it on the screen.
                                             # First 2 parameters are width&height of the window,last 2 parameters are X & Y co-ordinates

keyissuemessage = "We will adopt this key issue once base applied in their software release."

Options4EventVersions = [
    "-",
    "Event Version - EMR Version",
    "Event Version - SMR Version",
    "Event Version - Factory(RMV) Version",
    "Event Version - S/W Event Version(VP,QP)",
    "Temporary Version - Pre Version",
    "Temporary Version - Test Version",
    "Etc"
]

Options2provideKeyIssueMsg = [
    "Default",
    "Editable"
]

Option2chooseAction = [
    "-",
    "Not Applicable",
    "Deferred"
]

def startSelenium(uname,passwd,sasurl,ec,keyissuemessage):
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)

            if getattr(sys, 'frozen', False):
                print("inside frozen")
                #Running from exe, so the path to exe is saved in sys._MEIPASS
                chrome_driver = os.path.join(sys._MEIPASS, "chromedriver.exe")
            else:
                print("Inside chrome driverpath")
                chrome_driver = "E:\OLD_E_DRIVE_DATA\Python36\Scripts\seleniumpython\chromedriver.exe"

            driver = webdriver.Chrome(executable_path=chrome_driver)

            # Creating webdriver instance for chrome
            driver.set_page_load_timeout(30) # If below SAS URL not responding in 30 secs it will throw page load timeout error

            chooseeventversion = eventversion.get()
            chooseActionItem = Action.get()

            print("sasfields[0]:", uname)
            print("sasfields[1]:", passwd)
            print("sasfields[2]:", sasurl)
            print("sasfields[3]:", chooseeventversion)
            print("sasfields[4]:", chooseActionItem)

            index = Options4EventVersions.index(chooseeventversion)
            print("index of selected event is:", index)

            indexforAction = Option2chooseAction.index(chooseActionItem)
            print("index of ActionItem is:", indexforAction)

            while True:
                try:
                    driver.get(sasurl)

                    # get the Session id of the Parent
                    parentGUID = driver.current_window_handle;

                    print(parentGUID)

                except Timeoutexception:
                    print("Time out retrying...")
                    continue
                else:
                    break
            driver.maximize_window()  # Maximizes the browser window

            driver.implicitly_wait(20)  # Implicit wait for 30 secs

            username_field = driver.find_element_by_xpath("//*[@id='loginForm']/table/tbody/tr[1]/td[3]/input")
            username_field.send_keys(uname) #sendKeys method is basically used to type some content into an editable field.

            password_field = driver.find_element_by_xpath("//*[@id='loginForm']/table/tbody/tr[3]/td[3]/input")
            password_field.send_keys(passwd)

            username_field.submit()

            driver.implicitly_wait(10)  # Implicit wait for 30 secs
            time.sleep(5)
            #driver.maximize_window()  # Maximizes the browser window

            # click on KeyIssuecheck
            print("clicking on keyIssuecheckbutton")
            KeyIssueCheck_button = driver.find_element_by_xpath("//*[@id = 'boardDetailBottomBtn']/table/tbody/tr/td[6]/input")

            # You can use the execute script method to execute the java script on the loaded page.
            # You can call the javaScript API to scroll to the bottom or any other position of a page.
            driver.execute_script("arguments[0].scrollIntoView();", KeyIssueCheck_button)

            print("KeyIssueMessage inside startselenium method:",keyissuemessage)

            try:
                KeyIssueCheck_button.click()
                driver.implicitly_wait(7)  #Implicit wait for 30 secs
                time.sleep(5)
                deferKeyIssues(driver, sasurl, index, indexforAction,  ec, keyissuemessage)
            except UnexpectedAlertPresentException:
                # Whenever alert gets triggered and popup appears on the webpage.The control remains with the parent webpage only.
                # So the first task for selenium webdriver is to switch focus from parent page to Alert pop up.
                alert_obj = driver.switch_to.alert
                print("alertmessage:",alert_obj.text)

                # Used to accept the alert Message
                alert_obj.accept()

                deferNoPermalinkKeyIssues(driver, indexforAction, keyissuemessage)

def deferKeyIssues(driver, sasurl, index,indexforAction,ec,keyissuemessage):
            #click on KeyIssueManager button
            KeyIssueManager_button = driver.find_element_by_xpath("//*[@id='keyIssueManagerBtn']")
            KeyIssueManager_button.click()

            # To calculate the number of defects in key issue manager area
            defect_count = len(driver.find_elements_by_xpath("//*[@id='keyIssueManagerArea']/table/tbody/tr"))

            # decrementing to find exact number of rows used for defects excluding header row
            dc = defect_count-1
            print("defects_count:", dc)

            # To find number of columns per each row of KeyIssue defect area
            col_count = len(driver.find_elements_by_xpath("//*[@id='keyIssueManagerArea']/table/tbody/tr[2]/td"))
            c = col_count
            print("col_count:", c)

            # To find number of event version options per each keyIssueManager Area
            print("eventversionOptions_Count:", ec)

            #Display KeyIssueMessage in deferkeyIssue Area
            print("keyissuemessage in deferKeyIssuesMethod:",keyissuemessage)

            driver.implicitly_wait(7)  # Implicit wait for 30 secs
            time.sleep(5)

            #dividing the xpath for dropdown menu to perform click operation on each KeyIssueDefect
            first_part = "//*[@id='keyIssueManagerArea']/table/tbody/tr["
            second_part = "]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[1]/td/select"

            # m is used to loop through number of defects
            m = 0

            if dc == 0:
                driver.back()
                driver.get(sasurl)
                # switch back to the parent window
                print("calling parentGUID")

            else:
                print("To conclude key issue when defect count is nonzero")
                #Getting xpath of dropdown menu for each KeyIssue
                for n in range(2, defect_count+1):
                    drop_down_final_path = first_part + str(n) + second_part

                #Traversing through each Key Issue defect
                    if m < defect_count:
                            # Finding the xpath for text area for each key issue defect
                            textareafirstpart = "//*[@id='keyIssueManagerArea']/table/tbody/tr["
                            textareasecondpart = "]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[1]/textarea"
                            textarea = textareafirstpart + str(n) + textareasecondpart

                            # Finding the xpath for save button area for each key issue defect
                            savebuttonfirstpart = "//*[@id='keyIssueManagerArea']/table/tbody/tr["
                            savebuttonsecondpart = "]/td[6]/table/tbody/tr[1]/td[3]/table/tbody/tr[2]/td[2]/input"
                            savebutton = savebuttonfirstpart + str(n) + savebuttonsecondpart

                            # Finding the xpath for defer button for each key issue defect
                            deferbuttonfirstpart  ="//*[@id='keyIssueManagerArea']/table/tbody/tr["
                            deferbuttonsecondpart ="]/td[8]/input[3]"
                            deferbutton = deferbuttonfirstpart + str(n) + deferbuttonsecondpart

                            #Find the xpath for Not Applicable button for each key issue defect
                            NotApplicablebuttonfirstpart ="//*[@id='keyIssueManagerArea']/table/tbody/tr["
                            NotApplicablebuttonsecondpart ="]/td[8]/input[2]"
                            NotApplicablebutton = NotApplicablebuttonfirstpart + str(n) + NotApplicablebuttonsecondpart

                            # Using Action chain to scroll down
                            myselect = Select(driver.find_element_by_xpath(drop_down_final_path))
                            element = driver.find_element_by_xpath(drop_down_final_path)
                            ActionChains(driver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

                            time.sleep(1)

                            #Select the required event option based on input
                            myselect.select_by_index(index)

                            #clear the text area field and insert text in text area
                            driver.find_element_by_xpath(textarea).clear()
                            textareaelement = driver.find_element_by_xpath(textarea)
                            textareaelement.send_keys(keyissuemessage)

                            # click on save button once you input text in text area
                            savebuttonelement = driver.find_element_by_xpath(savebutton)
                            savebuttonelement.click()

                            # Select the required action based on input 0:Not Applicable 1:defer
                            if indexforAction == 1:
                                # click on NotApplicable button for each key issue
                                NotApplicablebuttonelement = driver.find_element_by_xpath(NotApplicablebutton)
                                NotApplicablebuttonelement.click()
                            elif indexforAction == 2:
                                # click on defer button to defer the key issue
                                deferbuttonelement = driver.find_element_by_xpath(deferbutton)
                                deferbuttonelement.click()
                    #else:
                            #element = driver.find_element_by_xpath(drop_down_final_path)
                            #ActionChains(driver).key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
                    m = m+1

                closebutton = driver.find_element_by_xpath("/html/body/div[5]/div[1]/a/span")
                closebutton.click()

            deferNoPermalinkKeyIssues(driver, indexforAction, keyissuemessage)


def deferNoPermalinkKeyIssues(driver,indexforAction,keyissuemessage):

            # Display KeyIssueMessage in deferkeyIssue Area
            print("keyissuemessage in deferNopermalinkKeyIssues:", keyissuemessage)

            # To click on KeyIssue(No Permalink) button for deferring checklist key issues
            KeyIssueNoPermalinkbutton = driver.find_element_by_xpath("//*[@id='boardDetailBottomBtn']/table/tbody/tr/td[7]/input")
            KeyIssueNoPermalinkbutton.click()

            #  To calculate number of checklist issues in KeyIssueManagerArea(No Permalink)
            checkListManagerArea_count = len(driver.find_elements_by_xpath("//*[@id='checkListManagerArea']/table/tbody/tr"))
            print("Number of checkList Issues :", checkListManagerArea_count)

            # To traverse through each Keyissuechecklist Area
            for ci_count in range(2,checkListManagerArea_count+1):
                checkListManagerArea_firstpart = "//*[@id='checkListManagerArea']/table/tbody/tr["
                checkListManagerArea_secondpart = "]/td[7]/table/tbody/tr/td[1]/textarea"
                checkListManagerArea = checkListManagerArea_firstpart + str(ci_count) + checkListManagerArea_secondpart


                # clear the text area field & insert text in textarea
                driver.find_element_by_xpath(checkListManagerArea).clear()
                checkListManagerAreaelement = driver.find_element_by_xpath(checkListManagerArea)
                checkListManagerAreaelement.send_keys(keyissuemessage)


                # Finding the xpath for save button area for each checklist key issue defect
                savebuttonfirstpart = "//*[@id='checkListManagerArea']/table/tbody/tr["
                savebuttonsecondpart = "]/td[7]/table/tbody/tr/td[2]/input"
                savebutton = savebuttonfirstpart + str(ci_count) + savebuttonsecondpart


                # Finding the defer button for each checklistissue
                deferbuttonfirstpart = "//*[@id='checkListManagerArea']/table/tbody/tr["
                deferbuttonsecondpart = "]/td[8]/input[3]"
                deferbutton = deferbuttonfirstpart + str(ci_count) + deferbuttonsecondpart

                # Finding the NotApplicable button for each checklist issue
                NotApplicablebuttonfirstpart = "//*[@id='checkListManagerArea']/table/tbody/tr["
                NotApplicablebuttonsecondpart = "]/td[8]/input[2]"
                NotApplicablebutton = NotApplicablebuttonfirstpart + str(ci_count) + NotApplicablebuttonsecondpart

                # click on save button once you input the text in text area
                savebuttonelement = driver.find_element_by_xpath(savebutton)

                # Using Action chain to scroll down
                ActionChains(driver).key_down(Keys.CONTROL).click(savebuttonelement).key_up(Keys.CONTROL).perform()
                time.sleep(1)
                savebuttonelement.click()

                # Select the required action based on input 0:Not Applicable 1:defer
                if indexforAction == 1:
                    # click on NotApplicable button for each key issue
                    NotApplicablebuttonelement = driver.find_element_by_xpath(NotApplicablebutton)
                    NotApplicablebuttonelement.click()
                elif indexforAction == 2:
                     # click on defer button to defer the key issue
                     deferbuttonelement = driver.find_element_by_xpath(deferbutton)
                     deferbuttonelement.click()

                # click on defer button to defer the key issue
                deferbuttonelement = driver.find_element_by_xpath(deferbutton)
                deferbuttonelement.click()
            mbox.showinfo("Success", "You have Completed with Conclusion of KeyIssues")


def deferNoPermalinkKeyIssues_OneTime(driver,indexforAction,keyissuemessage):
             # Display KeyIssueMessage in deferkeyIssue Area
             print("keyissuemessage in deferNopermalinkKeyIssues:", keyissuemessage)

             # To click on KeyIssue(No Permalink) button for deferring checklist key issues
             KeyIssueNoPermalinkbutton = driver.find_element_by_xpath("//*[@id='boardDetailBottomBtn']/table/tbody/tr/td[7]/input")
             KeyIssueNoPermalinkbutton.click()

             #  To calculate number of checklist issues in KeyIssueManagerArea(No Permalink)
             checkListManagerArea_count = len(driver.find_elements_by_xpath("//*[@id='checkListManagerArea']/table/tbody/tr"))
             print("Number of checkList Issues :", checkListManagerArea_count)

             # To Calculate the checkListManager Action Type
             #checkListManagerActionType = driver.find_element_by_xpath("//*[@id ='checkListManagerActionType']")
             #checkListManagerActionType.click()
             checkListManagerActionType = Select(driver.find_element_by_xpath(checkListManagerActionType))
             checkListManagerActionType.select_by_index(indexforAction)

def optionmenuchangeevent4keyissuemsg(keyissuecomment,keyissuemessage):
            #Read textmsginput
            def readtextmsginput(textentry):
                global keyissuemessage
                keyissuemessage = textentry.get()
                mbox.showinfo("Done","Click on Run button below To Proceed Further")
                print("EditedKeyIssueMsg:",keyissuemessage)

            # Create a label to display defer Message to the User in GUI
            def displaykeyissuemessagelabel(keyissuemessage):
                defaultmsg = "Your key issues will be deferred with following message:"
                keyissuemsg = "We will adopt this key issue once base applied in their software release."
                label7 = Label(root, text=defaultmsg, font=("Courier New", 10, "italic"), fg="black").place(x=410,y=380)
                label8 = Label(root, text=keyissuemsg, font=("Courier New", 10, "italic"), fg="black").place(x=410,y=400)
                keyissuemessageinlabel = defaultmsg + keyissuemsg
                mbox.showinfo("Done", "Click on Run button below To Proceed Further")
                print("KeyIssueMessage to display in GUI application:", keyissuemessageinlabel)

            #Create a text entry to edit KeyissueMessage
            def displaykeyissuemsgtextentry():
                textentry = StringVar()
                keyissuemsgtextentry = Entry(root, textvariable=textentry, width=45, bg="lightgreen").place(x=220,y=425)
                work3 = Button(root, text="Read", width=10, height=1, bg="lightblue",command=lambda: readtextmsginput(textentry)).place(x=510, y=420)

            choosekeyissuemessage = keyissuecomment.get()

            if choosekeyissuemessage == "Default":
                displaykeyissuemessagelabel(keyissuemessage)

            elif choosekeyissuemessage == "Editable":
                displaykeyissuemsgtextentry()


heading = Label(root, text="Conclude Key Issues in SAS board" , font=("Times", 20, "bold"), fg="steelblue").pack()

label1  = Label(root, text= "Username:", font=("Courier New",15,"italic"), fg="black").place(x=10,y=200)
label2  = Label(root, text= "Password:", font=("Courier New",15,"italic"), fg="black").place(x=10,y=230)
label3  = Label(root, text= "SAS URL :", font=("Courier New",15,"italic"), fg="black").place(x=10,y=260)
label4  = Label(root, text= "Versions:", font=("Courier New",15,"italic"), fg="black").place(x=10,y=300)
label5  = Label(root, text= "Action:", font=("Courier New",15,"italic"), fg="black").place(x=10,y=340)
label6  = Label(root, text= "KeyIssueComment:", font=("Courier New",15,"italic"), fg="black").place(x=10,y=380)


name = StringVar()
username = Entry(root, textvariable=name, width=45, bg="lightgreen").place(x=150,y=210)

pwd = StringVar()
password = Entry(root, textvariable=pwd, width=45, bg="lightgreen",show='*').place(x=150,y=240)

sas_url = StringVar()
sasurl = Entry(root, textvariable=sas_url, width=45, bg="lightgreen").place(x=150,y=270)

#Create a tkinter variable to set the options for Options4EventVersions
eventversion = StringVar(root)
eventversion.set(Options4EventVersions[0]) #0:-,1:EMR,2:SMR,3:RMV,4:VP,QP,5:PreVersion,6:TestVersion,7:Etc
eventversioncount = len(Options4EventVersions)

#Create a tkinter variable for drop down menu to provide keyissuecomment based on default or editable
keyissuecomment = StringVar(root)
keyissuecomment.set(Options2provideKeyIssueMsg[0]) #0:Default,1:editable

#create a tkinter variable to choose the correct ActionItem whether to perform defer or Not Applicable.
Action = StringVar(root)
Action.set(Option2chooseAction[0])       #1:Not Applicable,2:Defer

#Place OptionMenu to choose eventversion
w1 = OptionMenu(root,eventversion,*Options4EventVersions).place(x=220,y=300)

#Place OptionMenu to choose Action Item
w2 = OptionMenu(root,Action,*Option2chooseAction).place(x=220,y=340)

#Place OptionMenu to provide keyissuecomment
w3 = OptionMenu(root,keyissuecomment,*Options2provideKeyIssueMsg).place(x=220,y=380)


#This object is created to choose default or editable option for key issue comment
work1 = Button(root, text="Submit", width=10, height=1, bg="lightblue",command=lambda: optionmenuchangeevent4keyissuemsg(keyissuecomment,keyissuemessage)).place(x=320,y=382)

#For each function object,the Tkinter interface layer registers a Tk command with a unique name.when that Tk command is called by the Button implementation,the command calls the corresponding python function.
work2 = Button(root, text="Run", width=20, height=2, bg="lightblue", command=lambda: startSelenium(name.get(),pwd.get(),sas_url.get(),eventversioncount,keyissuemessage)).place(x=200,y=470)

#Tool Developed by Integration Team
footer = Label(root, text="Developed by: LGSI Integration Team", width=50, height=3, bg="lightgreen").place(x=100,y=520)

root.mainloop()  #The window won't appear until we enter the Tkinter event loop. Our script will remain in the event loop until we close the window.

#mainloop() is an infinite loop used to run the application,wait for an event to occur & process the event till the window is not closed.