import tor_tools as tor_tools
import os
import random
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException)
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

PROXY = 'socks5://localhost:9050'
options = webdriver.ChromeOptions()



#options.add_argument('--proxy-server=%s' % PROXY)
options.add_argument("--start-maximized")
#options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
#prefs = {"download.default_directory" : "/home/prime/PycharmProjects/iridescent"}
#options.add_experimental_option("prefs", prefs)
#driver = webdriver.Chrome(chrome_options=options)



class CodeChef():

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


    #url = "https://www.codechef.com/login?destination=/"
    url ="https://www.codechef.com/"
    user_xpath = "/html/body/section/div[2]/div/div[3]/div[2]/form/div/div[1]/div/div/input"
    user_xpath = "/html/body/section/div[2]/div/div[3]/div[2]/form/div/div[1]/div/div/input"
    pass_xpath = "/html/body/section/div[2]/div/div[3]/div[2]/form/div/div[2]/div/div[2]/input"
    login_xpath = "/html/body/section/div[2]/div/div[3]/div[2]/form/div/div[3]/input"
    practice_xpath = "/html/body/header/div/div[2]/div[1]/div/div/div[1]/a"
    top_performers_xpath = "/html/body/section[6]/div/div[2]/div[1]"
    tp_xpath = "/html/body/section[6]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/p[1]/a"
    tops_next_xpath="/html/body/main/div/div/div/aside/div[3]/div/div/table/tbody/tr/td[3]/a"
    view_all_xpath = "/html/body/section[6]/div/div[2]/div[1]/div/div[2]/div[6]/a"
    tops_table_xpath = "/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody"
    tt_rows ="/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[2]"
    next_page_xpath ="/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/table/tfoot/tr/td/div[1]/nav/ul/li[9]/button"
    ratings_head_xpath = "/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div[1]/h2"
    select_lang_xpath = "/html/body/center/center/table/tbody/tr/td/div/div/div/div/div[2]/div/div/div/div/form/table/tbody/tr/td[1]/select"
    go_button_xpath = "/html/body/center/center/table/tbody/tr/td/div/div/div/div/div[2]/div/div/div/div/form/table/tbody/tr/td[3]/input"
    first_solution_xpath = "/html/body/center/center/table/tbody/tr/td/div/div/div/div/div[2]/div/div/div/div/div[3]/table/tbody/tr[1]/td[8]/ul/li/a"
    download_code_xpath ="/html/body/div[1]/div/div[1]/div/div/div[4]/div/div/div/div[1]/ul/li[2]/div"
    code_text_xpath = "/html/body/div[1]/div/div[1]/div/div/div[4]/div/div/div/div[2]/div[1]/div[2]/div[2]/div"


    def __init__(self, my_user, my_pass):
        self.__my_user = my_user
        self.__my_pass = my_pass
        self.flat_leaders = []
        self.random_int = random.randint(0, 5)
        self.filtered_users_dict = ()
        self.count_loop = 0#Used to track loop instance
        self.user_processed = False
        self.error_timed_out = False



    def file_checker(self, user: str, contest: str, round: str) -> str:
        """
        Runs a check to see if the code file already exists

        """
        contest_dir = 'corpus/' + contest + '/' + user + '/' + round

        code_file_path = contest_dir + '/' + contest + '_' + user + '_' + round + '.cpp'

        exists = os.path.exists(code_file_path)

        print(code_file_path)

        if exists:
            self.user_processed = True
        if not exists:
            self.user_processed = False





    def make_corpus_dirs(self, path: str, contest: str, round: str,output) -> str:
        """
        :param path:
        :param contest:
        :param round:
        :param output:
        :return:
        """
        contest_dir = 'corpus/' + contest + '/' +path + '/' + round



        exists = os.path.exists(contest_dir)
        if not exists:
            print('corpus sub folder\n'
                  'does not exist!\n'
                  'Making the folder...')
            os.makedirs(contest_dir)
            print('The new directory is created')

            """
            writing code to .txt/.cpp
            """
            write_file = contest_dir + '/' + contest + '_' + path + '_' + round + '.cpp'

            with open(write_file , 'w') as f:
                f.writelines(output)
            
            """
            Create index 
            """
            index = 'corpus/' + contest + '/INDEX.txt'

            with open(index, 'a') as f:
                f.writelines(write_file+'\n')




    def wait_element(self, path: str) -> str:
        """
        waits for element to appear in Dom
        XPATH
        """
        return (WebDriverWait(CodeChef.browser, 20).until(EC.visibility_of_element_located((By.XPATH, path))))


    def find_element(self, path: str) -> str:
        """
        finds element
        XPATH
        """
        time.sleep(2)
        return CodeChef.browser.find_element(By.XPATH,path)


    def intial_setup(self):
        """
        Initial set up:
        1. login
        2. Find world ratings table
        3. Expand the ratings table / 15 per page
        """

        CodeChef.browser.get(CodeChef.url)
        """
        try:
            find_username = self.wait_element(path=CodeChef.user_xpath)
        except Exception as e:
            print(e, 'Username not found!')
            self.error_timed_out  = True
            time.sleep(.5)
            self.run()
            CodeChef.browser.navigate().refresh()
            print('Error. Re establising')
        """



        #find_username.send_keys(self.__my_user)
        #time.sleep(random_int)
        #find_password = self.wait_element(path=CodeChef.pass_xpath)
        #find_password.send_keys(self.__my_pass)
        #click_login = self.wait_element(path=CodeChef.login_xpath).click()
        wait_page = self.wait_element(path=CodeChef.practice_xpath)

        CodeChef.browser.execute_script("window.scrollTo(0, 2500)")
        time.sleep(3)
        self.find_element(path=CodeChef.view_all_xpath).click()#Expand table to next page




    def scrape_leaders_table(self):
        """
        Leaders are displayed in table, tranches of 15
        Loop 15 leaders
        For each, get the entry in the name field
        split the text at new line to get rid
        of some junk characters
        Return list of 15 leaders
        """
        leaders_list = []

        for i in range(1,16):

            row_num = [i]

            top_ranked_xpath= f"/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/div[2]/" \
                              f"table/tbody/tr{row_num}/td[1]/div[2]/a/div/span[2]"

            try:
                tb_row = self.wait_element(path=top_ranked_xpath)
            except Exception as e:
                print(e,'Failed to get name in the top ranged Table!')
                self.run()
                time.sleep(.5)
                CodeChef.browser.navigate().refresh()
                print('Error. Re establising')


            names_text= "".join(tb_row.text)
            ch = '\n'
            strValue = names_text.split(ch, 1)[0]
            leaders_list.append(strValue)
            print(strValue)

        return leaders_list




    def getX_top_leaders(self, pages: int) -> int:
        """
        Append each tranche of top x 15 leaders per page
        to a nested list.

        Loop the next page for the next tranche of 15

        create a flat list object of all names scraped
        """
        topXleaders = []

        while len(topXleaders) < pages:

            #tor_tools.PrivacyTools.change_torIP(self)

            time.sleep(self.random_int)
            topXleaders.append(self.scrape_leaders_table())#Get the top x leaders

            try:
                #self.find_element(path=CodeChef.next_page_xpath).click()#Go to the next page
                time.sleep(.5)
                self.wait_element(path=CodeChef.next_page_xpath).click()
            except Exception as e:
                print(e, 'Failed clicking next page for more leaders!')
                self.error_timed_out = True
                #self.run()
                CodeChef.browser.refresh()#Here is where duplicate user entries occur
                print('Error. Re establising')

        self.flat_leaders = set([x for sublists in topXleaders for x in sublists])#set() to fix double duplicates







    def get_participants(self,find,filtered_users ):
        """
        Navigate to each users personal profile
        Filter the page source

        If the text name of the contest round is seen:
        append name to list
        """
        for l in self.flat_leaders:
            url = 'https://www.codechef.com/users/'+l
            CodeChef.browser.get(url)
            src = CodeChef.browser.page_source
            text_found = bool(re.search(find, src))
            if text_found == True:
                 filtered_users.append(l)




    def isolate_contest(self, contest: str, contest_rounds: list) -> list :
        """

        Parse list of contest rounds on each profile
        loop each contest in the list arg

        Add the user + round they were found in to
        dictionary key, and value pair

        One dictionary per user
        """
        particpants_dict = {item: [] for item in contest_rounds}

        for c in contest_rounds:
            
            filtered_users = []

            self.get_participants(c,filtered_users)#

            particpants_dict[c]+=filtered_users#need to make values unique because of restarts in

        self.filtered_users_dict = particpants_dict

        print(self.filtered_users_dict)




    def get_code_text(self, contest: str) -> str:
        """
        Loop the filtered dict of users per contest round
        """

        contest = contest
     
        rounds_list = list(self.filtered_users_dict.keys())

        for r in rounds_list:

            time.sleep(1)

            comp_round = self.filtered_users_dict[r]

            for index, author in enumerate(comp_round):

                time.sleep(2)
                """
                Check if file exists sequence
                Only process this loop if the file is not 
                already stored as corpus 
                Allows some level of error recovery  
                """
                check_file = self.file_checker(user=author, contest=contest, round=r)

                if self.user_processed == False:
                    
                    time.sleep(self.random_int)

                    url = 'https://www.codechef.com/'+contest+'/status/' + r + ',' + author
                    CodeChef.browser.get(url)
                    print(r, index, author)
                    print(url)
                    time.sleep(3)
                    """
                    Language selection
                    """
                    try:
                        select_lang = self.find_element(path=CodeChef.select_lang_xpath)
                        select_lang.click()
                    except Exception as e:
                        print(e, 'Failed trying select language')
                        self.error_timed_out = True
                        self.run
                        CodeChef.browser.refresh()
                        print('Error. Re establising')


                    time.sleep(self.random_int)
                    """
                    view code
                    """
                    time.sleep(3)
                    try:
                        #self.find_element(path=CodeChef.go_button_xpath).click()  # Filter for C++17
                        self.wait_element(path=CodeChef.go_button_xpath).click()
                    except Exception as e:
                         print(e, 'Failed trying to view the code!')
                         time.sleep(.5)
                         #self.run()
                         CodeChef.browser.refresh()
                         print('Error. Re establising')
                    """
                    Select the first solution for problem solved
                    """
                    try:
                        self.find_element(path=CodeChef.first_solution_xpath).click()  # clicks into the first solution
                    except Exception as e:
                        print(e, 'Failed to click on the first solution found!')
                        self.error_timed_out = True
                        #time.sleep(.5)
                        CodeChef.browser.refresh()
                        pass
                         #more work to select correct submissions
                    """
                    Clicking on the view code solution button opens the link on a new tab in chrome. 
                    Therefore solution needed to switch between tabs.
                    """
                    print(CodeChef.browser.window_handles)
                    time.sleep(self.random_int)

                    #if self.error_timed_out ==False:
                    CodeChef.browser.switch_to.window(CodeChef.browser.window_handles[1])
                    time.sleep(3)
                    """
                    Getting the text of the code
                    """
                    print('The Current Index is ->',index)

                    try:
                        get_code_text = self.wait_element(path=CodeChef.code_text_xpath).text

                        self.make_corpus_dirs(path=author, contest=contest, round=r, output=get_code_text)

                        #get_code_text = self.find_element(path=CodeChef.code_text_xpath).text
                        #print(get_code_text)
                    except Exception as e:
                          print(e,'Failed to get code text')
                          #return
                          #CodeChef.browser.quit()
                          #time.sleep(.5)
                          #self.run()
                          #CodeChef.browser.refresh()
                          print('Error. Re establising')
                          pass


                    CodeChef.browser.close()
                    CodeChef.browser.switch_to.window(CodeChef.browser.window_handles[0])

                    """
                    Teardown
                    """
                    if index == comp_round[-1]:
                        self.error_timed_out = False
                        return


    def contest_ltime110a(self):
        """
        Change these two variables
        per contest
        """
        contest = 'LTIME110A'
        contest_rounds  = ['LARGEFAM', 'STRINGXOR', 'BINHAPP', 'TREERET']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)


    def contest_cook06(self):
        """
        Change these two variables
        per contest
        """
        contest = 'COOK06'
        contest_rounds = ['CHEFTEAM', 'HOLES', 'WINDOW2', 'COLLTIME', 'DIVNODIV']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)


    def contest_july10(self):
        """
        Change these two variables
        per contest
        """
        contest = 'JULY10'
        contest_rounds = ['ARRANGE2', 'HAPPY', 'LCM', 'VOTING', 'MAXCROSS', 'BLOCKS']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)



    def contest_ltime45(self):
        """
        Change these two variables
        per contest
        """
        contest = 'LTIME45'
        contest_rounds = [' OVERPNT', 'COOMILK', 'QHOUSE', 'BRIBETR']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)



    def contest_ltime103a(self):
        """
        Change these two variables
        per contest
        """
        contest = 'LTIME103A'
        contest_rounds = ['NOL_LESS', 'INTREENCLR', 'SLEEPTECH', 'OPTSORT', 'RMNTREV', 'MNULS']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)

    def contest_snckfl21(self):
        """
        Change these two variables
        per contest
        """
        contest = 'SNCKFL21'
        contest_rounds = ['ONESGUESS', 'ANDOFMAXES', 'EQPRFMAXSPLT', 'PERMRANGES', 'ROBBERYPLAN', 'BAKERY']
        self.isolate_contest(contest=contest, contest_rounds=contest_rounds)
        self.get_code_text(contest=contest)


    def process(self):

        #run.intial_setup()
        self.intial_setup()

        self.getX_top_leaders(pages=400)
        #run.contest_ltime110a()
        """
        Choose the contest here
        """
        self.contest_ltime110a()
        #self.contest_cook06()
        #self.contest_july10()
        #self.contest_ltime45()
        #self.contest_ltime103a()
        #self.contest_snckfl21()


    def run(self):
        self.process()


def test_module():
    run = CodeChef('brokeoshi', 'Vallois336!')
    run.run()

test_module()







































