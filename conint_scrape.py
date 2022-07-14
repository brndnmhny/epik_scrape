import bs4 as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display


def correct_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url


def scrollDown(browser, numberOfScrollDowns):
    body = browser.find_element_by_tag_name("body")
    while numberOfScrollDowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return browser


def crawl_epik(url, run_headless=True):
    if run_headless:
        display = Display(visible = False, size = (1024, 768))
        display.start()

    url = correct_url(url)
    browser = webdriver.Chrome("C:/Users/brend/Downloads/chromedriver_win32/chromedriver.exe")
    browser.get(url)
    browser = scrollDown(browser, 500)
    elements = browser.find_elements_by_xpath("//div[@class = 'content-inner']/a")
    links = []
    for e in elements:
        link = e.get_attribute("href")
        links.append(link)

    posts = []
    for l in links:
        browser.get(l)
        t = browser.find_element_by_xpath("//h1[@class = 'entry-title']").get_attribute("innerHTML")
        d = browser.find_element_by_xpath("//div[@id = 'single-below-header']").get_attribute("innerHTML")
        b = browser.find_element_by_xpath("//div[@class = 'content-inner']").get_attribute("innerHTML")
        title = bs.BeautifulSoup(t, "html.parser").get_text(strip=True)
        date = bs.BeautifulSoup(d, "html.parser").get_text(strip=True)
        body = bs.BeautifulSoup(b, "html.parser").get_text(strip=True, )
        posts.append([title, date, body])

    browser.quit()

    return posts


def save(file_location, posts):
    with open(file_location, "w", encoding = "utf-8") as file:
        for post in posts:
            for p in post:
                file.write(p)
                file.write("\t")
            file.write("\n")
        file.close()


def main():
    epik_url = "https://www.epik.com/blog/"
    epik_posts = crawl_epik(epik_url, run_headless = False)
    print(epik_posts)
    save("C:/Users/brend/Documents/projects/conservative_internet/epik.txt", epik_posts)


main()
