from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import os
import time
import re
import json

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.binary_location = '/opt/google/chrome/chrome'

chrome_driver = '/home/usr/scraper/chromedriver' #os.getcwd() + "/chromedriver"

# go to Google and click the I'm Feeling Lucky button
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
#
# Now just tell it wherever you want it to go
#driver.get("https://medium.com/@dalewahl")

# Return the title
# Good to use assert clause to make sure you are where you think you are
#print(driver.title)

def get_verify_text_css_class(data):
        """
	When google redirects you to confirm that it's you page, it asks you to click on 'Text' or 'Call'
	button and this is how the html of 'Text' button looks like:
	<span class="RveJvd snByac">Text</span>
	Note: the css class is kind of auto-generated and we are going to need to know that in order
	to click on the 'Text' button as it is a 'span' click even that google js capture and submit
	the form. This method returns you the auto-generated css class name that we'll use to get the
	span element and click on it
	"""
        index = data.find('>Text</span></content')
        s = data[index-40:index+40]
        c = s[s.rfind('<span'):s.find('>Text</span>')]
        return c[c.find('="')+2:-1]

def write(fn, data):
        with open(fn, 'w') as fh:
                fh.write(data)

def scroll_page(driver, no_of_pagedowns=20, sleep_between_scroll=0.2):
	body = driver.find_element_by_tag_name("body")
	url = driver.current_url
	print("Start scrolling to load %s", url)
	while no_of_pagedowns:
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(sleep_between_scroll)
		no_of_pagedowns-=1
		print("Scrolling more down to load %s: %s", no_of_pagedowns, url)

print("Opening link")
driver.get("https://medium.com/m/signin?redirect=https%3A%2F%2Fmedium.com%2F&operation=login")
print('opened, sleeping 10 seconds before entering to use google')
time.sleep(12)
write('login.html', driver.page_source)
driver.save_screenshot("logging-in.png")

button = driver.find_element_by_css_selector('[data-action="google-auth"]')
print("found the button")
button.click()
print("button clicked")
sleep_time = 8
print("sleeping for %s sec now before takging screenshot and saving html", sleep_time)
time.sleep(sleep_time)
driver.save_screenshot("logging-in-second.png")
write('google-auth-page.html', driver.page_source)

emailAddress = input("Please your google email address:")
email = driver.find_element_by_name("identifier")
email.send_keys(emailAddress)
email.send_keys(Keys.ENTER)
print("submitted enter after entering email address, sleeping for %s sec", sleep_time)
sleep_time = 12
time.sleep(sleep_time)
print("Taking screen shot and saving html to google_auth_email_submit.html/png")
driver.save_screenshot("google_auth_email_submit.png")
write("google_auth_email_submit.html", driver.page_source)

password = driver.find_element_by_name("password")
key = input("Please provide your password for google account "+ emailAddress)
password.send_keys(key)
password.send_keys(Keys.ENTER)
print("Password is submitted, going to sleep for %s seconds, check your mobile and allow")
sleep_time = 45
time.sleep(sleep_time)

if driver.current_url.find('medium.com') < 0:
	print("Password submitted, taking screenshot now")
	driver.save_screenshot("verify.png")
	write('verify.html', driver.page_source)

	#after submitting google may send you to another page
	#to confrim that it is you and navigate to this page where
	#you need to click on 'Text' or 'Call' option
	#now click on 'Text' button to verify
	#open the verify.html page, look for the class name for 'Text' button
	#button = driver.find_element_by_css_selector('span#RveJvd')
	button = driver.find_element_by_css_selector(get_verify_text_css_class(driver.page_source))
	button.click()
	print("We clicked on 'Text' button. Waiting %s seconds for new page to load", sleep_time)
	sleep_time = 10
	print("Taking screen shot of current page and save it to submit_code.png and submit_code.html")
	driver.save_screenshot('submit_code.png')
	write('submit_code.html', driver.page_source)

	#now that we have clicked on 'Text' button, we must have received a text message from Google
	#with 6-digit security code. Let's submit that here

	#now ask user to enter the code he/she received in text message
	code = input("Enter code 6 digit code you received from google (without 'G-'): ")
	code_element = driver.find_element_by_css_selector('aria-label="Enter the code"')
	code_element.send_keys(code)
	code_element.send_keys(Keys.ENTER)

	sleep_time = 10
	time.sleep(sleep_time)

	print("Security Code Submitted, waiting for %s seconds to take screenshots", sleep_time)
	write('after_code_submit.html', driver.page_source)
	print("Page source is saved on after_code_submit.html")
else:
	print("Password submitted, taking screenshot now")
	driver.save_screenshot("medium.png")
	write('medium.html', driver.page_source)

print("Congratulations, you have successfully signed in. Here is the current url:")
print(driver.current_url)

#### Bookmarks loading
print("Navigating to bookmarks page")
driver.get("https://medium.com/me/list/bookmarks")
print("Sleeping for %s seconds before taking screenshots")
sleep_time = 10
time.sleep(sleep_time)

body = driver.find_element_by_tag_name("body")
no_of_pagedowns = 20
print("Start scrolling to load bookmarks")
while no_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1
        print("Scrolling more down to load bookmarks: %s", no_of_pagedowns)

print("Saving bookmarks page to bookmarks.html")
write('bookmarks.html', driver.page_source)
print("Source written for bookmarks, taking screenshots")
driver.save_screenshot('bookmarks.png')

#### Recommendation/clapped stories
print("Navigating to profile page to get to clapped stories page")
profile = driver.find_element_by_css_selector('[class="avatar"]')
profile.click()
driver.save_screenshot('profile_menu_opened.png')
write('profile_menu_opened.html', driver.page_source)

profile_button = driver.find_element_by_xpath('//*[contains(text(), "Profile")]')
profile_button.click()

sleep_time = 12
print("Sleeping for %s before taking screenshot of profile page", sleep_time)
time.sleep(sleep_time)
driver.save_screenshot('profile.png')
write('profile.html', driver.page_source)

#now on profile-page, click on Claps button
claps_button = driver.find_element_by_xpath('//*[contains(text(), "Claps")]')
claps_button.click()

sleep_time = 12
print("Sleeping for %s before taking screenshot of profile page", sleep_time)
time.sleep(sleep_time)
driver.save_screenshot('claps.png')
write('claps_page.html', driver.page_source)

#now scroll the pages to get complete list of clapped stories before we download the page source
scroll_page(driver)
driver.save_screenshot('clapped_stories.png')
write('clapped_stories.html', driver.page_source)

#### Clapped links parsing
data = open('clapped_stories.html').read()
soup = BeautifulSoup(data, 'html.parser')
claps = soup.find_all('div', attrs={'class':'streamItem--postPreview'})
#each clap has, author, group published in, publish-date, title, title-link, title-image, total-claps
clap = claps[0]
meta = clap.find('div', attrs={'class':'postMetaInline'})
meta_links = meta.find_all('a', attrs={'class':'ds-link'})
username = meta_links[0].text
user_profile = meta_links[0].get('href')
publish_group = meta_links[1].text
publish_group_link = meta_links[1].get('href')
article_link = clap.find('div', attrs={'class':'postArticle-content'}).parent.parent.find('a').get('href')
title = clap.find('div', attrs={'class':'postArticle-content'}).text
image = clap.find('div', attrs={'class':'postArticle-content'}).find('img').get('src')

##### Bookmarks parsing ######
data = open('bookmarks.html').read()
soup = BeautifulSoup(data, 'html.parser')
bookmarks = soup.find_all('div', attrs={'class':'streamItem'})
#class Clap(object):
#	def __init__(self, writer, write_profile_link, group_name, group_link
#        pass

class Bookmark(object):
	def __init__(self, link, title, read_time, publish_date):
		self.link = link
		self.title = title
		self.read_time = read_time
		self.publish_date = publish_date		
	@classmethod
	def load_from_dom(cls, dom_item):
		anchor_tag = dom_item.find('a', attrs={'class':'link'})
		return cls(
			anchor_tag.get('href'), anchor_tag.text, 
			dom_item.find('span', attrs={'class':'readingTime'}).get('title'),
			dom_item.find('time').get('datetime'))
	def to_dict(self):
		return self.__dict__
	def __str__(self):
		return json.dumps(self.to_dict())


for bookmark in bookmarks:
	b = Bookmark.load_from_dom(bookmark)
	print(b)

	

#Next Step:
#1. Get the stories I've liked/clapped by visiting Profile/Claps section
#2. Build a database out of and assign priorities
#3. Clean up this code to setup a generic library that offers the functionality
#4. Perhaps, get the list of recommended stories for me and show them on my page?

