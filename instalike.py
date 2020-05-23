from secret import contra 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep 

class InstaBot:
    def __init__(self, username, password):
        print(password)
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get('https://www.instagram.com')
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Ahora no')]")\
            .click()
        sleep(2)
    def get_followers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_users_profile()
        return followers

    def _get_users_profile(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def _get_users_pic(self):
        sleep(2)
        users = []
        height = self.driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div").value_of_css_property("padding-top")
        match = False
        while match==False:
            lastHeight = height
            # step 1 get elements list from web
            elements = self.driver.find_elements_by_xpath("//*[@id]/div/a")
            # step 2 save to my list
            for element in elements:
                if element.get_attribute('title') not in users:
                    users.append(element.get_attribute('title'))
            # step 3 scroll down for get new element
            self.driver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            sleep(1)
            # step 4 check, is this last scrollelements?
            height = self.driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div").value_of_css_property("padding-top")
            if lastHeight==height:
                match = True
        # close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/button")\
            .click()
        self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/button")\
            .click()
        return users

    def get_users_pic_like(self):
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button")\
            .click()
        followers = self._get_users_pic()
        print(followers)

    def list_pics(self):
        sleep(2)    
        # finds the button which gives the next picture
        body = self.driver.find_element_by_css_selector('body')
        for i in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            sleep(1)
        pics = self.driver.find_elements_by_class_name("_9AhH0")
        return pics

    def get_users_pic_like_range(self, inicio, fin):
        pics = self.list_pics()
        users = []
        for i in range(inicio, fin):
            pics[i].click()
            users.append(self.get_users_pic_like())
        return users
    def comparison(self, inicio, fin):
        followers = self.get_followers()
        likes = self.get_users_pic_like_range(inicio, fin)
        estadistica = []
        for i in likes:
            follow = 0 
            unfollow = 0
            for j in likes[i]:
                for k in followers:
                    if(likes[j] == followers[k]):
                        follow = follow+1
                    else:
                        unfollow = unfollow+1
            estadistica.append([follow], [unfollow])

        
prueba = InstaBot('stefano0594', contra)
prueba.comparison(0, 4)