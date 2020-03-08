from crawler import *
from db_helper import *
import re
from datetime import datetime, timedelta
import sys, traceback

url_root = 'https://vacation.eztravel.com.tw'

def get_travel_date(link_path):
    target_url = link_path
    if link_path.startswith("http") == False:
        target_url = url_root+link_path
    content = get_web_content(target_url)
    soup = BeautifulSoup(content,'lxml')

    trip_title = soup.find('h1')
    trip_detail = {}
    link_path = link_path.split("/introduction/")
    trip_detail["product_key"] = link_path[1].split('/')[0]
    # print(trip_detail)

    trip_contents = soup.find('div', class_ = 'product-info css-td').text.split('\n')
    for line in trip_contents:
        if line:
            line = line.replace(' ', '')
        else: continue

        if line.startswith("出發"):
            start_date_string = re.findall('\d+\/\d+\/\d+', line)[0]
            trip_detail["start_date"] = str(datetime.strptime(start_date_string, '%Y/%m/%d').date())
        elif line.startswith("抵台"):
            end_date_string = re.findall('\d+\/\d+\/\d+', line)[0]
            trip_detail["end_date"] = str(datetime.strptime(end_date_string, '%Y/%m/%d').date())
        elif line.startswith("總機位數"):
            trip_detail["upper_bound"] = int(re.findall('\d+', line)[0])
        elif line.startswith("最少成行人數"):
            trip_detail["lower_bound"] = int(re.findall('\d+', line)[0])
        else:
            continue
    
    other_date = soup.find('a', class_ = 'toggle-btn')
    other_date_link = other_date.get("href", "")
    return (trip_detail, other_date_link)

def calc_dateString_range(start_string, end_string):
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    end_date = datetime.strptime(end_string, '%Y-%m-%d')
    return abs((start_date - end_date).days)

def shit_days(start_string, diff):
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    return (start_date + timedelta(days=diff)).date()
    
if __name__ == '__main__':  

    queue_number = ""

    if len(sys.argv) == 2:
        queue_number = sys.argv[1]

    init_database()
    file_folder = "./queue%s"%queue_number
    links, filename = read_links_from_json(file_folder)
    print("target filename: %s" %filename)

    trip_detail_list = []

    # for test
    # links = links[:1]
    # print(links[0]["title"])

    for data in links:
        travel_date_info = get_travel_date(data["link"])
        trip_detail = (
                data["title"], 
                data["travel_code"],
                travel_date_info[0]["product_key"], 
                int(data["price"]),
                travel_date_info[0]["start_date"],
                travel_date_info[0]["end_date"],
                travel_date_info[0]["lower_bound"],
                travel_date_info[0]["upper_bound"]
                )
        trip_detail_list.append(trip_detail)

        # trip_detail sample: ({'start_date': datetime.date(2020, 3, 5), 'end_date': datetime.date(2020, 3, 9), 'lower_bound': 16, 'upper_bound': 26}, '/pkgfrn/otherDate/VDR0000010446/DTS19-KIX48')
        get_other_date_url = url_root + travel_date_info[1]
        get_other_date_url = get_other_date_url.replace("otherDate", "pfProOtherDate")
        other_date_list = get_from_api(get_other_date_url)

        for other_date in other_date_list:
            start_date = other_date["date"]
            if start_date == trip_detail[4]: continue
            date_range = calc_dateString_range(trip_detail[4], trip_detail[5])
            end_date = str(shit_days(start_date, date_range))

            other_date_detail = (
                trip_detail[0], 
                trip_detail[1],
                trip_detail[2], 
                int(other_date["price"]),
                start_date,
                end_date,
                trip_detail[6],
                trip_detail[7]
                )

            # print(other_date_detail)
            trip_detail_list.append(other_date_detail)

    # print(trip_detail_list)

    save2EzTravel_db(trip_detail_list)
    # save2json(filename, trip_detail_list)
    mission_done(file_folder, filename)