import requests, json, re, os, csv

group_list = []

class Groupimport:

    @staticmethod
    def createGroup(username, groupName, instance, auth_email, auth_pass):
        data_group = {'name': groupName}
        response = requests.post("https://" + instance + '/rest/api/2/group', headers={"content-type": "application/json"}, json=data_group, auth=(auth_email, auth_pass))

        if response.status_code == 201:
            global group_list
            group_list.append(str(response.status_code) + "<br/>" + 'Group, "'+groupName+'", has been successfully created!<br/>')
            g = Groupimport()
            g.makeRequest(username, groupName, instance, auth_email, auth_pass)

        else:
            group_list.append(str(response.status_code) + "<br/>" + 'Attemped to create the group '+ '"' + groupName + '"' + ', but got a ' + str(response.text) + '<br/>')

    @staticmethod
    def makeRequest(username, groupname, instance, auth_email, auth_pass):

        endpoint = '/rest/api/latest/group/user?groupname=' + groupname.strip()

        # Make request
        data = {'name': username}
        print ('\nAttempting to add ' + '"' + username + '"' + ' into the ' + '"' + groupname + '"' + ' group..')
        response = requests.post("https://" + instance + endpoint, headers={"content-type": "application/json"}, json=data, auth=(auth_email, auth_pass))

        if response.status_code == 201:
            print(response.status_code, 'User, ''"' + username + '"'', was added into the group ' + '"' + groupname + '"' + ' successfully!')
            group_list.append(str(response.status_code) + "<br/>" + 'User'',''"'+username+'"'',''was added into the group ' + '"' + groupname + '"' + ' successfully!<br/>')

        elif "The group" in response.text and response.status_code == 404:
            print(response.status_code, 'Group'+' "'+groupname+'" '+'does not exist in the target instance. Attempting to create it..' )
            group_list.append(str(response.status_code) + "<br/>" + 'Group'+' "'+groupname+'" '+'does not exist in the target instance. Attempting to create it..<br/>')

            # Instantiating an object of Groupimport() to call the method
            c = Groupimport()
            c.createGroup(username, groupname, instance, auth_email, auth_pass)
        else:
            group_list.append(str(response.status_code) + "<br/>" + str(response.text) + '<br/>')


    def groupImport(self, file, instance, email, password):
        global group_list
        group_list.clear()
        instance = instance

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
                username = row[0]
                groupname = row[1]

                # Instantiating an object of Groupimport() to call the method
                g = Groupimport()
                g.makeRequest(username, groupname, instance, email, password)

        return group_list
