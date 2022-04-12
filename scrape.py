import csv

import requests
from bs4 import BeautifulSoup

# !-- will scrape company list --!

# !-- scrape kashiwa from SUUMO --!

# csvの一行目(ヘッダー)
HEADER = ['物件名', 'アドレス', '最寄り', '築年/階', '階', '賃料/管理費', '敷金/礼金', '間取り/専有面積']
# webのリストのページ数
PAGE_NUM = 15

with open('kashiwa.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)

    for page in range(1, PAGE_NUM):
        # SUUMO URL (今回は柏駅まわり)
        url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?url=/chintai/ichiran/FR301FC001/&ar=030&bs=040&pc=20&smk=&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&cb=0.0&ct=9999999&et=15&mb=0&mt=9999999&cn=9999999&ta=12&sc=12217&oz=12217004&oz=12217005&oz=12217017&page=' + str(page)
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        list_contents = soup.find_all('div', class_='cassetteitem')
        for l in list_contents:
            if l.find('div', class_='cassetteitem_content-title') is None:
                pass
            else:
                name = l.find('div', class_='cassetteitem_content-title').text

            if l.find('li', class_='cassetteitem_detail-col1') is None:
                pass
            else:
                address = l.find('li', class_='cassetteitem_detail-col1').text

            near = ''
            if l.find('li', class_='cassetteitem_detail-col2') is None:
                pass
            else:    
                for item in l.find('li', class_='cassetteitem_detail-col2').find_all('div'):
                    if item is None:
                        pass
                    else:
                        near = near + str(item.string) + '\n'

            if l.find('li', class_='cassetteitem_detail-col3') is None:
                pass
            else:
                year = l.find('li', class_='cassetteitem_detail-col3').text

            monthly_pay = ''
            initial_pay = ''
            extent = ''
            # floor, monthly_pay, initial_pay, extent
            for n, item in enumerate(l.find_all('tbody')):
                for i, sub_item in enumerate(item.find_all('td')):
                    # 階
                    if i == 2:
                        floor = str(sub_item.string)

                    # 賃料
                    if i == 3:
                        monthly_pay = monthly_pay + str(n+1) + '. 賃料: ' + str(sub_item.find('span', class_='cassetteitem_other-emphasis').text) + '\n'
                        monthly_pay = monthly_pay + str(n+1) + '. 管理費: ' + str(sub_item.find('span', class_='cassetteitem_price--administration').text) + '\n'
                    
                    # 敷金/礼金
                    if i == 4:
                        initial_pay = initial_pay + str(n+1) + '. 敷金: ' + str(sub_item.find('span', class_='cassetteitem_price--deposit').text) + '\n'
                        initial_pay = initial_pay + str(n+1) + '. 礼金: ' + str(sub_item.find('span', class_='cassetteitem_price--gratuity').text) + '\n'
                    
                    # 間取り/専有面積
                    if i == 5:
                        extent = extent + str(n+1) + '. ' + str(sub_item.find('span', class_='cassetteitem_madori').text) + '\n'
                        extent = extent + str(n+1) + '. ' + str(sub_item.find('span', class_='cassetteitem_menseki').text) + '\n'

            row = [name, address, near, year, floor, monthly_pay, initial_pay, extent]
            writer.writerow(row)


# !-- scrape actors list --!

# HEADER = ['name', 'age', 'occupation', 'url']

# with open('actors_20.csv', 'w', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(HEADER)

#     for page in range(1, 47):
#         url = 'https://talent-dictionary.com/s/jobs/3/20?page=' + str(page)
#         r = requests.get(url)

#         soup = BeautifulSoup(r.text, 'html.parser')
#         actors = soup.find('ul', class_='list').find_all('li')
#         for actor in actors:
#             prof = actor.find('div', class_='right')

#             name = prof.find('a', class_='title').text
#             url = prof.find('a', class_='title').get('href')
#             occupation = prof.find('a', class_='job').text
#             if prof.find('span', class_='age') is None:
#                 pass
#             else:
#                 age = prof.find('span', class_='age').text

#             row = [name, age, occupation, url]
#             writer.writerow(row)