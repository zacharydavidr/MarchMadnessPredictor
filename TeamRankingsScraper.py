# import libraries
import urllib.request
import csv
from bs4 import BeautifulSoup


def main():

    team_name_dict = get_team_name_dict()

    years = ["2017", "2016", "2015", "2014", "2013", "2012"]
    stat_percent = ["offensive-rebounding-pct", "total-rebounding-percentage",
                    "three-point-pct", "opponent-shooting-pct"]

    predictors_headers = ""
    classifier_headers = ""

    for year in years:
        print("Processing year ... " + year)
        summary_year_pt_in = open("summary" + str(year) + "_pt.csv", "r").readlines()
        summary_year_pt_out = open("out_" + str(year) + ".csv", "w")
        kp_predictors_dict = {}
        kp_classifier_dict = {}


        # handle the headers for the kenpom pretourney data, split into predictors and classifiers
        predictors_headers = ""
        classifier_headers = ""
        headers = summary_year_pt_in[0]
        headers_array = headers.split(",")
        for i in range(0, 11):
            predictors_headers += headers_array[i] + ","

        for i in range(11, 18):
            classifier_headers += headers_array[i] + ","

        # skip the header line of the file for data processing
        for line in summary_year_pt_in[1:]:

            # replace kenpom team name with team rankings team name
            line_array = line.split(",")
            process_name_exceptions(line_array)
            line_array[1] = team_name_dict[line_array[1]]
            team_name = line_array[1]

            # split the predictors[0-10] from the class
            # Season,Team,AdjTempo,RankAdjTempo,AdjOE,RankAdjOE,AdjDE,RankAdjDE,AdjEM,RankAdjEM,seed

            kp_predictors_line = ""
            for i in range(0, 11):
                kp_predictors_line += line_array[i] + ","
            kp_predictors_dict.update({team_name: kp_predictors_line})

            # split the predictors[15-18] from the class

            kp_classifier_line = ""
            for i in range(11, 18):
                kp_classifier_line += line_array[i] + ","
            kp_classifier_dict.update({team_name: kp_classifier_line})

        # add a blank key for all teams in t
        tr_predictors_dict = {}
        for key in team_name_dict:
            tr_predictors_dict.update({team_name_dict[key]: " "})

        date = get_selection_show_date_by_year(year)

        for stat in stat_percent:
            add_stat_by_date(tr_predictors_dict, stat, date)
            predictors_headers += stat + ","

        # write out the falue
        summary_year_pt_out.write(predictors_headers + classifier_headers + "\n")
        for key in team_name_dict:

            # skip teams that weren't in D1
            team_name = team_name_dict[key]
            if(check_team_for_ineligiblity(team_name,year)):
                continue

            temp_line = kp_predictors_dict[team_name]
            temp_line += tr_predictors_dict[team_name]
            temp_line += kp_classifier_dict[team_name] + "\n"
            summary_year_pt_out.write(temp_line)

    # combine all years into one file
    master_out = open("master.csv", "w")
    master_out.write(predictors_headers + classifier_headers + "\n")

    for year in years:
        temp_in = open("out_" + str(year) + ".csv", "r").readlines()

        for line in temp_in[1:]:
            master_out.write(line)






def add_stat_by_date(tr_predictors_dict, stat, date):
    # specify the url and get the web page
    print("Stat: " + str(stat))
    quote_page = "https://www.teamrankings.com/ncaa-basketball/stat/"+stat+"?date="+date
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, "html.parser")

    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        team = tds[1].text
        value = float(tds[2].text.strip("%"))

        # update the value for the team
        team = team.strip()
        prev_value = tr_predictors_dict[team]
        new_value = prev_value + str(value) + ","

        tr_predictors_dict.update({team: new_value})


def get_selection_show_date_by_year(year):
    selection_show_dates = ["2017-03-12", "2016-03-13", "2015-03-15", "2014-03-16","2013-03-17","2012-03-11"]
    for date in selection_show_dates:
        if year in date:
            return date
    exit("No selection show date found for " + str(year))


def get_team_name_dict():
    # read in file to convert names between team rankings and kenpom
    team_names_file = open("team_name_conversions.csv", "r").readlines()
    team_name_dict = {}

    # don't need the headers line
    for line in team_names_file[1:]:
        kp_name, tr_name, team_id = line.split(",")

        # kenpom name is the key
        temp_dict = {kp_name.strip(): tr_name.strip()}
        team_name_dict.update(temp_dict)

    return team_name_dict

# Kenpom names change from year to year, so let's make sure they match our conversation table
def process_name_exceptions(line_array):
    if line_array[1] == "Arkansas Little Rock":
        line_array[1] = "Little Rock"
    elif line_array[1] == "IPFW":
        line_array[1] = "Fort Wayne"
    elif line_array[1] == "Texas Pan American":
        line_array[1] = "UT Rio Grande Valley"


def check_team_for_ineligiblity(team_name,year):
    # ----------2013---------
    if team_name == "Abl Christian" and int(year) <= 2013:
        return True
    elif team_name == "Grd Canyon" and int(year) <= 2013:
        return True
    elif team_name == "Incar Word" and int(year) <= 2013:
        return True
    elif team_name == "Mass Lowell" and int(year) <= 2013:
        return True

    # ---------2012---------
    elif team_name == "New Orleans" and int(year) <= 2012:
        return True
    elif team_name == "N Kentucky" and int(year) <= 2012:
        return True


if __name__ == "__main__":
    main()
