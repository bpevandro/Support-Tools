import requests, json, re
from datetime import datetime, timedelta

class Worklogs:

    # It receives minuntes as input and converts it into d:h:m
    def getTime(self, timeMin):
        test = timeMin
        minutes = timedelta(minutes=test)
        d = datetime(1, 1, 1) + minutes
        return d

    def getWorklogs(self, instance, email, password, issue, work_hours):

        users = {}
        ENDPOINT = '/rest/api/2/issue/'+issue

        RESPONSE = requests.get("https://" + instance + ENDPOINT, headers={"content-type": "application/json"}, auth=(email, password))
        print(RESPONSE.status_code)
        if RESPONSE.status_code == 200:

            DATA = RESPONSE.json()
            JSON_WORKLOG_OBJ = DATA['fields']['worklog']['worklogs']
            WORK_HOURS = int(work_hours)
            WORK_HOURS = WORK_HOURS * 60

            # time_tracking must be initialized with a value; otherwise, if issue has no worklogs, it will throw a stacktrace when trying
            # to return it at line 94.
            time_tracking = 0

            i = 0

            # Iterates through "json_worklog_obj" to get the users as well as the time spent by them
            for x in JSON_WORKLOG_OBJ:
                timeSpent_final = 0

                # It stores the author's name into "user"
                user = str(JSON_WORKLOG_OBJ[i]['author']['name'])

                # It stores the author's time spent into "timeSpent"
                timeSpent = str(JSON_WORKLOG_OBJ[i]['timeSpent'])

                time_tracking = str(DATA['fields']['timetracking'])

                # Time Spent format: 1d 2h 3m
                # This step splits the timeSpent into groups using REGEX
                timeSpent_re = re.search(r'([0-9]+d)?( )?([0-9]+h)?( )?([0-9]+m)?( )?', timeSpent, re.M | re.I)
                group_1 = timeSpent_re.group(1)
                group_3 = timeSpent_re.group(3)
                group_5 = timeSpent_re.group(5)

                # This checks if the groups exist and remove the letters from the timeSpent and convert it to integers
                if group_1 is not None:
                    group_1_re = re.search(r'[0-9]+', group_1, re.M | re.I)
                    group_1_re = int(group_1_re.group(0))
                    group_1_re = group_1_re * WORK_HOURS
                    timeSpent_final = timeSpent_final + group_1_re

                if group_3 is not None:
                    group_3_re = re.search(r'[0-9]+', group_3, re.M | re.I)
                    group_3_re = int(group_3_re.group(0))
                    group_3_re = group_3_re * 60
                    timeSpent_final = timeSpent_final + group_3_re

                if group_5 is not None:
                    group_5_re = re.search(r'[0-9]+', group_5, re.M | re.I)
                    group_5_re = int(group_5_re.group(0))
                    timeSpent_final = timeSpent_final + group_5_re

                flag = 0

                # Iterates through users dictionary to see if the current user retrieve from the JSON exists already
                for user_loop in users:

                    # If it does exist, get the existing value and sum up with the new value retrieve from JSON
                    if user == user_loop:
                        total = users.get(user) + timeSpent_final
                        users[user] = total
                        flag = 1

                # Saving it as {"author": "timeSpent"}
                if flag != 1:
                    users[user] = timeSpent_final

                i += 1

            for key, value in users.items():

                    p = Worklogs()
                    finalTime = p.getTime(value)
                    finalDay = finalTime.day - 1
                    users[key] = str(finalDay)+"d "+ str(finalTime.hour) + "h " + str(finalTime.minute) + "m."

            return RESPONSE.status_code, time_tracking, users

        else:

            return RESPONSE.status_code, None, None