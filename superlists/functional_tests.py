from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://moja-witryna.pl:8000")

assert 'Congratulations' in browser.title