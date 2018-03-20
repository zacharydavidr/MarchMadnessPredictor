# import libraries
import urllib.request
from bs4 import BeautifulSoup


def main():
    team_name_dict = get_team_name_dict()

    stat_percent = ["offensive-rebounding-pct", "total-rebounding-percentage", "opponent-ftm-per-100-possessions",
                    "three-point-pct", "opponent-shooting-pct", "win-pct-close-games",
                    "opponent-effective-field-goal-pct", "points-from-3-pointers", "points-from-2-pointers",
                    "win-pct-all-games", "free-throw-pct", "free-throws-made-per-game", "assist--per--turnover-ratio",
                    "personal-fouls-per-possession", "true-shooting-percentage"]

    predictors_headers = ""
    classifier_headers = ""

    # ---- main processing loop ----
    years = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
             "2014", "2015", "2016", "2017"]

    for year in years:
        print("Processing year ... " + year)
        kenpom_pre_tournament_data = open("summary" + str(year) + "_pt.csv", "r").readlines()
        summary_year_pt_out = open("out_" + str(year) + ".csv", "w")
        kp_predictors_dict = {}
        kp_classifier_dict = {}

        # handle the headers for the kenpom pretourney data, split into predictors and classifiers
        predictors_headers = ""
        classifier_headers = ""
        headers = kenpom_pre_tournament_data[0]
        headers_array = headers.split(",")
        for i in range(0, 11):
            predictors_headers += headers_array[i] + ","

        for i in range(11, 19):
            classifier_headers += headers_array[i] + ","

        # skip the header line of the file for data processing
        for line in kenpom_pre_tournament_data[1:]:
            line = line.strip()
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
            for i in range(11, 19):
                kp_classifier_line += line_array[i] + ","
            kp_classifier_dict.update({team_name: kp_classifier_line})

        # add a blank key for all teams in t
        tr_predictors_dict = {}
        for key in team_name_dict:
            tr_predictors_dict.update({team_name_dict[key]: " "})

        date = get_selection_show_date_by_year(year)
        BASE_URL = "https://www.teamrankings.com"
        STAT_URL = BASE_URL + "/ncaa-basketball/stat/"
        RPI_URL = BASE_URL + "/ncb/rpi/"

        for stat in stat_percent:
            print("Stat: " + str(stat))
            url = STAT_URL + stat + "/?date=" + date
            add_stat_by_date(tr_predictors_dict, url)
            predictors_headers += stat + ","

        url = RPI_URL + "?date=" + date
        print("RPI... ")
        add_stat_by_date(tr_predictors_dict, url)
        predictors_headers += "RPIRank" + ","

        # write out the falue
        new_line = predictors_headers + classifier_headers
        summary_year_pt_out.write(new_line.lstrip(",\n").rstrip(",\n") + "\n")
        for key in team_name_dict:

            # skip teams that weren't in D1
            team_name = team_name_dict[key]
            if (check_team_for_ineligibility(team_name, year)):
                continue

            temp_line = kp_predictors_dict[team_name]
            temp_line += tr_predictors_dict[team_name]
            temp_line += kp_classifier_dict[team_name]
            summary_year_pt_out.write(temp_line.lstrip(",\n").rstrip(",\n") + "\n")

        summary_year_pt_out.close()

    # combine all years into one file
    master_out = open("master.csv", "w")
    my_line = predictors_headers + classifier_headers
    master_out.write(my_line.lstrip(",").rstrip(",") + "\n")

    for year in years:
        print("Writing Year: " + str(year))
        temp_in = open("out_" + str(year) + ".csv", "r").readlines()
        for line in temp_in[1:]:
            master_out.write(line.lstrip(",\n").rstrip(",\n") + "\n")

    # ---- process 2018 ------
    print("--------")
    print("Processing year ... 2018")
    tr_predictors_dict = {}
    kp_predictors_dict = {}
    BASE_URL = "https://www.teamrankings.com"
    predictors_headers = ""

    for key in team_name_dict:
        tr_predictors_dict.update({team_name_dict[key]: " "})

    year = 2018
    date = "2018-03-12"
    summary_year_pt_out = open("out_2018.csv", "w")
    kenpom_pre_tournament_data = open("summary" + str(year) + "_pt.csv", "r").readlines()
    headers = kenpom_pre_tournament_data[0]
    headers_array = headers.split(",")
    for i in range(0, 11):
        predictors_headers += headers_array[i].strip("\n") + ","

    # skip the header line of the file for data processing
    for line in kenpom_pre_tournament_data[1:]:
        line = line.strip()
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

    # Seeds released, no longer need to get seed form team rankings
    # print("Getting predicted seeds... ")
    # //SEED_URL = BASE_URL + "/ncaa-tournament/bracketology/"
    # add_seed(tr_predictors_dict, SEED_URL)
    # predictors_headers += "seed" + ","

    for stat in stat_percent:
        print("Stat: " + str(stat))
        STAT_URL = BASE_URL + "/ncaa-basketball/stat/"
        STAT_URL += stat + "/?date=" + date
        add_stat_by_date(tr_predictors_dict, STAT_URL)
        predictors_headers += stat + ","

    RPI_URL = BASE_URL + "/ncb/rpi/" "/?date=" + date
    print("RPI... ")
    add_stat_by_date(tr_predictors_dict, RPI_URL)
    predictors_headers += "RPIRank" + ","

    summary_year_pt_out.write(predictors_headers.lstrip(",\n").rstrip(",\n") + "\n")
    for key in team_name_dict:

        # skip teams that weren't in D1
        team_name = team_name_dict[key]
        if check_team_for_ineligibility(team_name, year):
            continue

        temp_line = kp_predictors_dict[team_name]
        temp_line += tr_predictors_dict[team_name]
        summary_year_pt_out.write(temp_line.lstrip(",\n").rstrip(",\n") + "\n")

    summary_year_pt_out.close()


def add_seed(tr_predictors_dict, url):
    # specify the url and get the web page
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    table = soup.find('table')

    for tr in table.find_all('tr')[2:]:
        value = 0.0
        tds = tr.find_all('td')
        team = tds[2].text

        if tds[0].text == "":
            value = 0
        else:
            value = int(tds[0].text.strip(""))

        # update the value for the team
        team = team.strip()
        team = trim_record_from_team_name(team)
        prev_value = tr_predictors_dict[team]
        new_value = prev_value + str(value) + ","

        tr_predictors_dict.update({team: new_value})


def add_stat_by_date(tr_predictors_dict, url):
    # specify the url and get the web page
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    table = soup.find('table')

    for tr in table.find_all('tr')[1:]:
        value = 0.0
        tds = tr.find_all('td')
        team = tds[1].text

        if tds[2].text == "--":
            value = float(0.0)
        else:
            value = float(tds[2].text.strip("%"))

        if "rpi" in url:
            value = int(tds[0].text.strip())

        # update the value for the team
        team = team.strip()
        if "rpi" in url:
            team = trim_record_from_team_name(team)
        prev_value = tr_predictors_dict[team]
        new_value = prev_value + str(value) + ","

        tr_predictors_dict.update({team: new_value})


def trim_record_from_team_name(team):
    reversed_name = team[::-1]
    if reversed_name.find("(") != -1:
        reversed_trimmed_name = reversed_name[reversed_name.find("(") + 1:]
        trimmed_name = reversed_trimmed_name[::-1]
        return trimmed_name.strip()
    else:
        return team


def get_selection_show_date_by_year(year):
    selection_show_dates = ["2017-03-12", "2016-03-13", "2015-03-15", "2014-03-16", "2013-03-17", "2012-03-11",
                            "2011-03-13", "2010-03-14", "2009-03-15", "2008-03-16", "2007-03-11", "2006-03-12",
                            "2005-03-13", "2004-03-14", "2003-03-16", "2002-03-10"]

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
    elif line_array[1] == "Utah Valley St.":
        line_array[1] = "Utah Valley"
    elif line_array[1] == "Southwest Missouri St.":
        line_array[1] = "Missouri St."
    elif line_array[1] == "Troy St.":
        line_array[1] = "Troy"
    elif line_array[1] == "Middle Tennessee St.":
        line_array[1] = "Middle Tennessee"
    elif line_array[1] == "Southwest Texas St.":
        line_array[1] = "Texas St."

    #2003 morris brown not tracked by team rankings

# Teams come into and out of D1
#  '>=' means they joined D1
# '>' means they fell out of D1
# Returns true if team was not a D1 school that year, returns false otherwise
def check_team_for_ineligibility(team_name, year):
    if team_name == "Abl Christian" and int(year) < 2014:
        return True
    elif team_name == "Grd Canyon" and int(year) < 2014:
        return True
    elif team_name == "Incar Word" and int(year) < 2014:
        return True
    elif team_name == "Mass Lowell" and int(year) < 2014:
        return True

    elif team_name == "New Orleans" and int(year) < 2013:
        return True
    elif team_name == "N Kentucky" and int(year) < 2013:
        return True

    elif team_name == "Neb Omaha" and int(year) < 2012:
        return True
    elif team_name == "Centenary" and int(year) >= 2012:
        return True

    elif team_name == "Wins-Salem" and int(year) >= 2011:
        return True

    elif team_name == "South Dakota" and int(year) < 2010:
        return True
    elif team_name == "North Dakota" and int(year) < 2010:
        return True
    elif team_name == "Seattle" and int(year) < 2010:
        return True
    elif team_name == "SIU Edward" and int(year) < 2010:
        return True

    elif team_name == "Bryant" and int(year) < 2009:
        return True
    elif team_name == "Houston Bap" and int(year) < 2009:
        return True

    elif team_name == "CS Bakersfld" and int(year) < 2008:
        return True
    elif team_name == "Fla Gulf Cst" and int(year) < 2008:
        return True
    elif team_name == "NC Central" and int(year) < 2008:
        return True
    elif team_name == "Presbyterian" and int(year) < 2008:
        return True
    elif team_name == "SC Upstate" and int(year) < 2008:
        return True

    elif team_name == "Central Ark" and int(year) < 2007:
        return True
    elif team_name == "NJIT" and int(year) < 2007:
        return True
    elif team_name == "Wins-Salem" and int(year) < 2007:
        return True
    elif team_name == "Bham Southern" and int(year) >= 2007:
        return True

    elif team_name == "Kennesaw St" and int(year) < 2006:
        return True
    elif team_name == "N Dakota St" and int(year) < 2006:
        return True
    elif team_name == "N Florida" and int(year) < 2006:
        return True
    elif team_name == "S Dakota St" and int(year) < 2006:
        return True

    elif team_name == "Longwood" and int(year) < 2005:
        return True
    elif team_name == "N Colorado" and int(year) < 2005:
        return True
    elif team_name == "UC Davis" and int(year) < 2005:
        return True
    elif team_name == "Utah Val St" and int(year) < 2005:
        return True






if __name__ == "__main__":
    main()
