from flask import Flask, render_template
import requests, csv
import flask, jinja2

class Userimport:
    UPLOAD_FOLDER = '..'

    def userImport(self, file, instance, email, password ):
        p = Userimport()
        progress = 0
        endpoint = '/rest/api/2/user'
        user_list = []

        with open(file) as csvfile:

            readCSV = csv.reader(csvfile, delimiter=',')

            # Get the current position of the file read pointer
            last_pos = csvfile.tell()

            # Get the total number of rows within the file, minus 1 to disregard to header
            numline = len(csvfile.readlines()) - 1

            # Point it back to the first row of the file
            csvfile.seek(last_pos)

            # Jump to second row
            next(csvfile)

            for row in readCSV:
                print("\n")
                print('Attempting to create', row)

                email_address = row[3]
                name = row[1] + " " + row[2]
                username = row[0]

                # Make request
                data = {'displayName': name, 'emailAddress': email_address, 'name': username}
                response = requests.post("https://" + instance + endpoint, headers={"content-type": "application/json"}, json=data, auth=(email, password), timeout=10)
                print(response.text)

                if response.status_code == 201 or response.status_code == 200:
                    user_list.append(str(response.status_code) + "<br/>" + 'User,' '"'+name+'"'',' 'was successfully created with email address'',''"'+email_address+'"'',''and username'',''"'+username+'".<br/>')

                elif response.status_code == 500:
                    response = requests.get("https://" + instance + endpoint +"?username="+username, headers={"content-type": "application/json"}, auth=(email, password))

                    if response.status_code == 200 or response.status_code == 201:
                        user_list.append(str(response.status_code) + "<br/>" + 'User,' '"' + name + '"'',' 'was successfully created with email address'',''"' + email_address + '"'',''and username'',''"' + username + '".<br/>')

                    else:
                        user_list.append(str(response.status_code) + "<br/>" + str(response.text) + " " + username + "<br/>")

                elif response.status_code == 401:
                    user_list.append(str(response.status_code) + "<br/>" + str(response.text) + "<br/>")
                    return user_list

                else:
                    user_list.append(str(response.status_code) + "<br/>" + str(response.text) + " " + username + "<br/>")

            return user_list



