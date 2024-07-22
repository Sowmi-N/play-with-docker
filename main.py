from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait                                                   
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

# Load local .env
load_dotenv()

# Defining default options for chrome browser
options = webdriver.ChromeOptions()                   
options.add_argument('--ignore-ssl-erros=yes')        
options.add_argument('--ignore-certificate-errors')                                                         
driver = webdriver.Remote(
        command_executor = 'http://localhost:4444/wd/hub',
        options = options
)

# Defining the start url

driver.get("https://labs.play-with-docker.com/")

# Print the title of start page

print("Started automation....")
print("The start page is : ")
print(driver.title)

# Defining implicit waits

driver.implicitly_wait(5)

# Get the login button

print(driver.title)
button1 = driver.find_element(By.ID, "btnGroupDrop1")
# Click the login button (button1)
print("Clicking login button...")
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "btnGroupDrop1"))).click()
# Get the docker button
button2 = driver.find_element(By.CLASS_NAME, "ng-binding")
# Click the docker button
# Check the page title
# sleep for few seconds to check url changes
#time.sleep(3)
#print("Title after 3 seconds...")
#print(driver.title)
#print(driver.current_url)

#a_tags = driver.find_elements(By.TAG_NAME, "a")
#for a in a_tags:
#    print(a.text)
#print("")
#print("Now printimg hidden text elements as well.")
#for a in a_tags:
#    print(a.get_attribute("innerText"))
#print("")

#print("Getting dropdown menus")
#print("")
dropdown_menu = driver.find_elements(By.CLASS_NAME, "dropdown-menu")
#for dmnu in dropdown_menu:
#    print(dmnu.text)
#    print(dmnu.get_attribute("style"))

print("Clicking the docker parent div of a tag")
actions = ActionChains(driver)
actions.move_to_element(dropdown_menu[0]).click().perform()

#WebDriverWait(driver, 5).until(EC.element_to_be_clickable((a_tags[1]))).click()
#print("Title after 3 seconds...")
#time.sleep(3)
#print(driver.title)
#print(driver.current_url)

# Saving main window
print("Getting current window handle")
original_window = driver.current_window_handle

WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
#print(driver.current_url)
print(driver.title)

# Few Variable
user = os.environ.get("USERNAME")
passwd = os.environ.get("PASSWORD")

# Now fill the username into username input
username = driver.find_element(By.ID, "username")
print("Writing username...")
username.send_keys(user, Keys.RETURN)

# Now fill the password
password = driver.find_element(By.ID, "password")
print("Writing password...")
password.send_keys(passwd, Keys.RETURN)

print("Waiting to login...")
#time.sleep(10)
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))

# Now we should be redirected to original page
print("Going back...")
driver.switch_to.window(original_window)
print("")

print("Printing current current window...")
print(driver.title)
print(driver.current_url)

# searching through links to check if start link is active or not
#for a in a_tags:
#    print(a.text)
#print("")

#print("Now printimg hidden text elements as well.")
#for a in a_tags:
#    print(a.get_attribute("innerText"))

while True:
    # Now we have to click start button
    form_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "landingForm")))
    #start_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located(form_element.find_element(By.TAG_NAME, "a")))
    time.sleep(10)
    start_button = form_element.find_element(By.TAG_NAME, "a")
    #start_button = form_element.find_element(By.TAG_NAME, "a")
    #print("")

    # Next click on start button
    print("Clicking the start button...")
    print(start_button.text)
    actions.move_to_element(start_button).click().perform()
    print("")

    #print(driver.title)
    #print(driver.current_url)

    print("Sleeping 10 seconds...")
    time.sleep(10)
    print("")

    print(driver.title)
    print(driver.current_url)
    print("")

    if("ooc" in driver.current_url):
        print("Out of Capacity detected...")
        print("Sleep 10 seconds..")
        time.sleep(10)
        print("Getting to start url")
        driver.get("https://labs.play-with-docker.com/")
    else:
        layout_column = driver.find_element(By.CLASS_NAME, "layout-column")
        md_sidenav = layout_column.find_element(By.TAG_NAME, "md-sidenav")
        md_content_main = layout_column.find_element(By.TAG_NAME, "md-content")
        md_content_sidenav = md_sidenav.find_element(By.TAG_NAME, "md-content")
        add_button = md_content_sidenav.find_element(By.TAG_NAME, "button")
        for i in range(1,5):
            print("Clicking add new instance button...")
            print(add_button.text)
            actions.move_to_element(add_button).click().perform()
            
            print("Sleeping 20 seconds....")
            time.sleep(20)

            print("Getting ssh command...")
            try:
                md_card = layout_column.find_element(By.TAG_NAME, "md-card")
                input_3 = md_card.find_element(By.ID, "input_3")
                print(input_3.get_attribute("value"))

                terminal_instance = layout_column.find_element(By.CLASS_NAME, "terminal-instance")
                terminal = terminal_instance.find_element(By.CLASS_NAME, "terminal")
                command = "kill -9 $(ps aux | grep 'sshd: /usr' | awk '{print $1}') && /usr/sbin/sshd -o PermitRootLogin=yes -o PrintMotd=yes -o AllowAgentForwarding=yes -o AllowTcpForwarding=yes -o X11Forwarding=yes -o X11DisplayOffset=10 -o X11UseLocalhost=no"
                print("Clicking terminal....")
                actions.move_to_element(terminal).click().perform()
                print("Sending commands...")
                terminal.send_keys(command, Keys.RETURN)
                print("Started docker")
                # Now we reached desired state so stay here
                stop = input("")
            except:
                print("Failed to create new instance retrying..., sleep 10 seconds...")
                time.sleep(10)
                continue
        # Find the close session button
        md_toolbar = md_sidenav.find_element(By.TAG_NAME, "md-toolbar")
        close_button = md_toolbar.find_element(By.TAG_NAME, "button")
        print("Pressing close button...")
        actions.move_to_element(close_button).click().perform()
        print("Waiting until session closes...")
        time.sleep(10)
        print("Getting to start url")
        driver.get("https://labs.play-with-docker.com/")



# Finally close the browser

driver.close()
