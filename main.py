from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def add_results(link, name):
    print(f'<a href="{link}">Chapter {index} - {name}</a>')
    with open("result.txt", mode="a", encoding="UTF-8") as result_file:
        print(f'<a href="{link}">Chapter {index} - {name}</a>', file=result_file)

#create file just to make sure
result_file = open("result.txt", mode="w")
result_file.close()

driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(4)
# driver.get("https://graverobbertl.site/prologue-the-beginning-of-the-two/")
driver.get("https://graverobbertl.site/prologue-the-beginning-of-the-two/")


index = 0
end_flag = False
while end_flag == False:
    #get chapter's name and link
    chapter_link = driver.current_url
    chapter_name = driver.find_element_by_xpath('//div[contains(@class, "post-header")]/h1').text
    
    #if chapter_name.lower() contains "SPT Cha" then chapter_name = driver.find('//div[contains(@class="strong-text-or-something")]/strong')
    if "spt cha" in chapter_name.lower(): #if chapter has tl's-note in the beggining
        try:
            chapter_name = driver.find_element_by_xpath("//div[contains(@class, 'post-entry')]/p[contains(@class, 'font-size')]/strong").text
        except NoSuchElementException: #if chapter doesn't have chapter name - most likely it is a tl-note page
            # next_chapter_link = driver.find_element_by_xpath('//p[contains(@class,"has-text-align-center")]/strong/a').get_attribute('href')
                not_found_next_chapter_button = len(driver.find_elements_by_xpath('//div[contains(@class, "wp-block-button")]/a[text()[contains(.,"Next Chapter")]]')) == 0
                if not_found_next_chapter_button:
                    next_chapter_link = driver.find_element_by_xpath('//p[contains(@class, "has-text-align-center")]//a[contains(.,"CHAPTER") or contains(.,"chapter") or contains(.,"Chapter")]').get_attribute('href')
                    driver.get(next_chapter_link)
                    continue #try to find a link to the chapter and return to beggining of the loop
                else:
                    chapter_name = driver.find_element_by_xpath('//div[contains(@class, "post-header")]/h1').text


    add_results(chapter_link, chapter_name)
    index += 1

    next_chapter_link = driver.find_element_by_xpath('//div[contains(@class, "wp-block-button")]/a[text()[contains(.,"Next Chapter")]]').get_attribute("href")
    if next_chapter_link == None:
        next_chapter_link = f"https://graverobbertl.site/spt-chapter-{index}/"
    if next_chapter_link == chapter_link:
        end_flag = True
    else:
        driver.get(next_chapter_link)