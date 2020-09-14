import requests
import json
import datetime

def get_page(url):
    #print('\nURL to test: ',url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(url, headers=headers)

def month_format(month):
    if month < 10:
        return '0' + str(month)
    return str(month)

def camp_available(data):
    camp_dates = []
    camp_dates = json_reader(camp_dates, data)
    return camp_dates

def json_reader(camp_dates, data):

    for key,value in data.items():
        #print (str(key)+'->'+str(value))
        if str(key) == 'campsite_id':
            camp_id = value
            print('Campsite ID: ', value)
        if str(key) == 'loop':
            camp_loop = value
            print('Campsite Loop: ', value)
        if str(value) == 'Available':
            camp_dates.append('\t'+str(key)[:10]+' is available.')
            #campsite_output(data)# if available get name, date, url
        if type(value) == type(dict()):
            json_reader(camp_dates,value)
        elif type(value) == type(list()):
            for val in value:
                if type(val) == type(str()):
                    pass
                elif type(val) == type(list()):
                    pass
                else:
                    json_reader(camp_dates,val)
    if len(camp_dates) < 1:
        camp_dates.append('\tNothing is available in this time period')
    return camp_dates

def get_camp_info(id, month, year):
    url = 'https://www.recreation.gov/api/camps/availability/campground/{}/month?start_date={}-{}-01T00%3A00%3A00.000Z'\
        .format(id, str(year), month_format(month))
    return get_page(url)

def date_range():
    dates_to_check = []
    response = False
    while response == False:
        date_range_input = input('Check specific month (1) or check next three months(2): ')
        try:
            date_range_input = int(date_range_input)
            if date_range_input == 1:
                years_to_check = input('Year to check: ')
                months_to_check = input('Month to check (1-12): ')
                try:
                    years_to_check = int(years_to_check)
                    months_to_check = int(months_to_check)
                    dates_to_check.append([months_to_check, years_to_check])
                    response = True
                except:
                    print('Month or Year is invalid')
            elif date_range_input == 2:
                now = datetime.datetime.now()
                for i in range(1,4):
                    dates_to_check.append(month_fix(now.month+i, now.year))
                    response = True
            else:
                print('Input is invalid')

        except:
            print('Inputs are invalid')
    return dates_to_check

def month_fix(month, year):
    date_fixed = []
    if month > 12:
        month -=12
        year += 1
    return [month, year]


def main():
    campground = ['234248','234262','233133','234161','234163','234185','234271','234173',\
                  '234187','234621','234154','234125','233322','234155','234248','234149',\
                  '234247','234189','233894']
    #campground = ['233894']

    dates_to_check = []
    dates_to_check = date_range()

    for dates in dates_to_check:
        start_month = dates[0]
        start_year = dates[1]
        for id in campground:
            camp_info = get_camp_info(id, start_month, start_year)
            print('\nLink to camp: https://www.recreation.gov/camping/campgrounds/{}'.format(id))
            campsite = json.loads(camp_info.text)
            camp_dates = camp_available(campsite)
            for dates in camp_dates:
                print(dates)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
