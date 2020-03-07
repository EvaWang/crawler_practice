from crawler import *
from db_helper import *

def get_travel_code():
    url_root = 'https://vacation.eztravel.com.tw/'
    root_content = get_web_content(url_root)
    root_soup = BeautifulSoup(root_content,'lxml')

    # 找出所有travel code
    code_list = []
    trip_code_list = root_soup.find_all('li', attrs = {"data-traveltype": "A1"})
    for trip_code in trip_code_list:
        code_val = trip_code.get('data-travelcode',None)
        if code_val is None: continue
        
        # code_list.append({
        #     "travel_code": code_val,
        #     "travel_code_name": str(trip_code.string),
        #     })
        code_list.append((code_val, str(trip_code.string)))
    return code_list

    
if __name__ == '__main__':  
    code_list = get_travel_code()

    save2Code_table(code_list)

    # create_folder("./data")
    # save2json("./data/travel_code_list", code_list)

    # TODO: 從參數決定存到DB還是json