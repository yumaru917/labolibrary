"""
Crawler of Town-News
"""

import selenium
from selenium import webdriver
import time
import datetime
import os
import pandas as pd


class GetHTML(object):

    def __init__(self):

        self.major_list = ['Engineer']
        self.url_list = {
            "NEM":
                "http://www.n.t.u-tokyo.ac.jp/online/lab/list/",
            "BioEngineering":
                "http://www.bioeng.t.u-tokyo.ac.jp/faculty/index.html",
            "mechanics":
                "http://www2.mech.t.u-tokyo.ac.jp/research/"
        }
        self.laboratory_list = {}
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        # self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome('C:\\Users\\greee\\anaconda3\\envs\\django-env\\chromedriver.exe'
                                       , options=self.options)
        print('webdriver starts.')

    def make_new_directory(self):

        try:
            os.mkdir("utokyo")
        except FileExistsError:
            print("directory 'utokyo' already exists.")
            pass

        for category in self.major_list:
            new_dir_name = "utokyo/" + category
            try:
                os.mkdir(new_dir_name)
            except FileExistsError:
                print("directory '" + new_dir_name + "' already exists.")
                pass

    def get_NEM_laboratory_list(self):
        self.driver.get(self.url_list['NEM'])

        time.sleep(2)

        NEM_laboratory_list = []

        elements = self.driver.find_elements_by_class_name("modPartsBlock01Content")

        for element in elements:

            lab_name_element = element.find_element_by_class_name("modPartsTitle01")
            lab_keyword_element = element.find_element_by_class_name("myBlockItemCatch")
            lab_detail_element = element.find_element_by_class_name("myBlockItemTxt")
            lab_urls = []
            try:
                lab_url_elements = element.find_elements_by_class_name("myBlockItemLink")
                for lab_url_element in lab_url_elements:
                    url = lab_url_element.find_element_by_tag_name("a").get_attribute("href")
                    lab_urls.append(url)
            except selenium.common.exceptions.NoSuchElementException:
                pass

            lab_name = lab_name_element.text
            lab_keyword = lab_keyword_element.text
            lab_keyword = lab_keyword.replace(',', '，')
            lab_keyword = lab_keyword.replace('・', '，')
            lab_detail = lab_detail_element.text
            lab_detail = lab_detail.replace(',', '，')
            lab_detail = lab_detail.replace('\n', '')

            NEM_laboratory_list.append([lab_name, lab_keyword, lab_detail, lab_urls])

        with open('utokyo/Engineer/NEM.csv', 'w', encoding='utf-8') as f:
            for lab_info in NEM_laboratory_list:
                f.write(lab_info[0] + ',' + lab_info[1] + ',' + lab_info[2])
                if lab_info[3]:
                    for lab_url in lab_info[3]:
                        f.write(',' + lab_url)
                else:
                    pass
                f.write('\n')

    def get_BioEngineering_laboratory_list(self):
        self.driver.get(self.url_list['BioEngineering'])

        time.sleep(2)

        BioEng_laboratory_list = []
        detail_url_list = []

        elements = self.driver.find_elements_by_class_name("verbaseline")

        for element1 in elements:
            sections = element1.find_elements_by_class_name('section')
            for element in sections:
                try:
                    detail_url_element1 = element.find_element_by_class_name("floatL-01")
                    detail_url1 = detail_url_element1.find_element_by_tag_name('a').get_attribute("href")
                    laboratory_url1 = detail_url_element1.find_element_by_class_name('title-03')
                    laboratory_url1 = laboratory_url1.find_element_by_class_name('float-R')
                    laboratory_url1 = laboratory_url1.find_element_by_tag_name('a').get_attribute("href")
                    detail_url_list.append([detail_url1, laboratory_url1])
                    print(detail_url1)

                    detail_url_element2 = element.find_element_by_class_name("floatR-01")
                    detail_url2 = detail_url_element2.find_element_by_tag_name('a').get_attribute("href")
                    laboratory_url2 = detail_url_element2.find_element_by_class_name('title-03')
                    laboratory_url2 = laboratory_url2.find_element_by_class_name('float-R')
                    laboratory_url2 = laboratory_url2.find_element_by_tag_name('a').get_attribute("href")
                    detail_url_list.append([detail_url2, laboratory_url2])
                    print(detail_url2)
                except selenium.common.exceptions.NoSuchElementException:
                    pass

        print(len(detail_url_list))

        with open('utokyo/Engineer/BioEngineering.csv', 'w', encoding='utf-8') as f:

            for detail_url in detail_url_list:
                time.sleep(2)
                self.driver.get(detail_url[0])
                professor_name = self.driver.find_element_by_class_name('title-01').text
                print(professor_name)
                lab_detail_elements = self.driver.find_elements_by_class_name('section')
                lab_detail = lab_detail_elements[3].text
                lab_detail = lab_detail.replace(',', '，')
                lab_detail = lab_detail.replace('\n', '')
                lab_detail = lab_detail.replace('研究室の目指すもの', '')
                print(lab_detail)

                f.write(professor_name + ',' + lab_detail + ',' + detail_url[1] + '\n')

    def get_mechanics(self):
        print('i')
        self.driver.get(self.url_list['mechanics'])
        print(self.driver.get(self.url_list['mechanics']))
        for i in range(6):
            if i == 0:
                continue
            element = self.driver.find_element_by_id("research{}".format(i))
            elements = element.find_elements_by_tag_name("li")
            for ele in elements:
                # print(ele.text)
                # teacher = ele.find_element_by_class_name('teacher-name').text
                # belong = ele.find_element_by_class_name('teacher-belong').text
                url = ele.find_element_by_class_name('teacher-website')
                url = url.find_element_by_tag_name('a').get_attribute("href")
                print(url)
                # text = ele.find_element_by_class_name('research-text').text
                # theme_list = []
                # themes = ele.find_elements_by_class_name('teacher-website')
                # for theme in themes:
                #     theme_text = theme.find_element_by_tag_name('li').text
                #     theme_list.append(theme_text)
                #
                # print(teacher, belong, url, text, theme_text)

    def get_html_file(self, urls):
        number = 0
        previous_magazine_date = "default"
        for url in urls:
            self.driver.get(url[2])
            if previous_magazine_date != url[1]:
                number = 0
                previous_magazine_date = url[1]
            else:
                pass

            filename = "town-news/" + url[0] + "/" + str(url[1]) + '/page-' + str(number + 1) + '.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(self.driver.page_source))
            time.sleep(1)
            number += 1

    def get_html_of_all_category(self):
        """
        This is the main function of this Class.

        Make the directory categorized three types.

        In order to crawl all detail page on the specific site, the posted date is used.
        To say specifically, after crawling all content of list page, compare the posted date of the first page with
        that of last page. If the dates are same, crawling is stopped, but if not, continue the crawling to the next
        list page.

        :return: Nothing
        """

    def check_count(self, urls, dir_name):

        file_count = 0
        for pathname, dirnames, filenames in os.walk(dir_name):
            file_count += len(filenames)

        url_count = 0
        for url in urls:
            if url[1] == urls[0][1]:
                url_count += 1
            else:
                break
        print(url_count)
        print(file_count)
        if file_count == url_count:
            print('Verification conditions: Clear')
        else:
            print('Verification conditions: False')

    def __del__(self):

        """
        close webdriver

        :return -> string: 'webdriver ends.'
        """

        self.driver.close()
        print('webdriver ends.')


class RunCrawling(object):

    """
    This class is only used for run the all of crawling programs.
    """

    get_html = GetHTML()
    # get_html.make_new_directory()
    # get_html.get_NEM_laboratory_list()
    # get_html.get_BioEngineering_laboratory_list()
    # get_html.get_html_of_all_category()
    get_html.get_mechanics()


if __name__ == '__main__':
    RunCrawling()
