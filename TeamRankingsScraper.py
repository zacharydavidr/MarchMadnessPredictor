# import libraries
import urllib.request
import csv
from bs4 import BeautifulSoup


def main():

    stat_percent = ["offensive-rebounding-pct", "total-rebounding-percentage", "three-point-pct", "opponent-shooting-pct",
                   "offensive-efficiency", "defensive-efficiency"]
    #selection_show_dates = ["2017-03-12", "2016-03-13", "2015-03-15", "2014-03-16"]
    #years =["2017","2016","2015","2014"]

    selection_show_dates = ["2018-2-19"]
    years = ["2018"]
    index = 0
    for date in selection_show_dates:
        master_data_set = []
        storeTeamNamesByDate(master_data_set, date)

        for stat in stat_percent:
            storeStatByDate(master_data_set, stat, date)

        # open a csv file with append, so old data will not be erased
        out = open("data_"+str(years[index])+".csv", "w")
        row_string = ""
        for idx in range(0, len(stat_percent)):
            row_string += str(stat_percent[idx]) + " , "
        out.write(row_string + "\n")

        for row in range(0, len(master_data_set[0])):
            row_string = "Team,"
            for col in range(0, len(master_data_set)):
                row_string += str(master_data_set[col][row]) + " , "
            out.write(row_string + "\n")
        index += 1

def storeStatByDate(master_data_set, stat, date):
    print("-----------------------")
    # specify the url
    quote_page = "https://www.teamrankings.com/ncaa-basketball/stat/"+stat+"?date="+date
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, "html.parser")
    data_dictionary = dict()
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        team = tds[1].text
        value = float(tds[2].text.strip("%"))
        data_dictionary.update({team: value})

    stat_array = []
    for key in sorted(data_dictionary.items()):
        print(key[0]+":"+str(key[1]))
        stat_array.append(key[1])


    master_data_set.append(stat_array)


def storeTeamNamesByDate(master_data_set, date):
    print("-----------------------")
    # specify the url
    quote_page = "https://www.teamrankings.com/ncaa-basketball/stat/offensive-rebounding-pct?date="+date
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, "html.parser")
    data_dictionary = dict()
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        team = tds[1].text
        value = float(tds[2].text.strip("%"))
        data_dictionary.update({team: value})

    stat_array = []
    for key in sorted(data_dictionary.items()):
        print(key[0]+":"+str(key[1]))
        stat_array.append(key[0])

    master_data_set.append(stat_array)

if __name__ == "__main__":
    main()