from crawler import *
from urllib.parse import urlparse
import sys, traceback
import random

ezTravel_root = "https://vacation.eztravel.com.tw/"

def get_travel_list_url(travel_code, page_num, depDateFrom, depDateTo):
    return 'https://vacation.eztravel.com.tw/pkgfrn/results/TPE/%s/%d?depDateFrom=%s&depDateTo=%s&avbl=0'%(travel_code, page_num, depDateFrom, depDateTo)

def get_travel_list(travel_code, depDateFrom, depDateTo, queue_number):

    url = get_travel_list_url(travel_code, 1, depDateFrom, depDateTo)
    web_content = get_web_content(url)
    
    soup = BeautifulSoup(web_content,'lxml')

    numer_of_pages = get_number_of_pages(soup)

    # # FOR TEST  
    # numer_of_pages = 1

    for page in range(1, numer_of_pages+1):
        filename = "./queue%s/link_%s_%d_%s_%s" %(queue_number, travel_code, page, depDateFrom, depDateTo)
        is_done = check_path_exist(filename+".json")
        if is_done: continue

        trip_detail_links = []
        if page != 1:
            url = get_travel_list_url(travel_code, page, depDateFrom, depDateTo)
            web_content = get_web_content(url)
            soup = BeautifulSoup(web_content,'lxml')

        # 找出目標，行程清單
        trip_list = soup.find_all('a', class_ = 'list-item-link')

        for trip in trip_list:
            detail_link = trip.get('href', None);
            print(detail_link)

            trip_title = trip.h2.string
            print(trip_title)

            price = trip.select('span.text-price')[0].string.strip().replace(',','')
            print(price)

            trip_detail_links.append({
                "link": detail_link,
                "title": trip_title,
                "price": price,
                "travel_code": travel_code
            })

        save2json(filename, trip_detail_links)
    # return trip_detail_links

def get_number_of_pages(soup):
    try:
        last_page = soup.find('a', attrs={'data-track-action':'{"val":"最末頁"}'})
        last_page_url = last_page.get('href', None)
        parse_last_page_url = urlparse(last_page_url)
        numer_of_pages = parse_last_page_url.path.split('/')[-1]
        return int(numer_of_pages)
    except:
        #找不到就假裝只有一頁
        return 1

def get_travel_detail(url):
    web_content = get_web_content(url, False)
    soup = BeautifulSoup(web_content,'lxml')
    
    trip_detail = soup.find('h1')
    print(trip_detail)

    trip_contents = soup.find('div', class_ = 'product-info css-td').get_text()

    print(trip_start_date.strip())


if __name__ == '__main__':

    # args = sys.argv
    if len(sys.argv) <4 :
        raise Exception("argument error.")
    
    try:
        queue_number = str(random.randint(1, 3))
        create_folder("./queue%s"%queue_number)

        if len(sys.argv) == 4:
            trip_detail_links = get_travel_list(sys.argv[3], sys.argv[1], sys.argv[2], queue_number)
        else:
            code_list = read_from_json('./data/travel_code_list.json')
            trip_detail_links = get_travel_list(code["travel_code"], sys.argv[1], sys.argv[2], queue_number)
        
    except:
        print("Got error. params: %s %s %s" %(sys.argv[3], sys.argv[1], sys.argv[2]))
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exc()
        pass
    