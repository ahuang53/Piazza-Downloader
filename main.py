from pyquery import PyQuery as pq
import os
import json
import re
import requests

from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
from piazza_api.exceptions import AuthenticationError, NotAuthenticatedError, \
    RequestError

piazza_url = 'https://piazza.com/class_profile/get_resource/'
classID = ''

'''Modified User Login function from piazza-api to login to piazza and
access resource files and download them with requests'''

def download(email, password, sections):
    """Login with email, password and get back a session cookie

    :type  email: str
    :param email: The email used for authentication
    :type  password: str
    :param password: The password used for authentication
    """
    session = requests.Session()
    # Need to get the CSRF token first
    response = session.get('https://piazza.com/main/csrf_token')

    # Make sure a CSRF token was retrieved, otherwise bail
    if response.text.upper().find('CSRF_TOKEN') == -1:
        raise AuthenticationError("Could not get CSRF token")
    
    # Remove double quotes and semicolon (ASCI 34 & 59) from response string.
    # Then split the string on "=" to parse out the actual CSRF token
    csrf_token = response.text.translate({34: None, 59: None}).split("=")[1]


    # Log in using credentials and CSRF token and store cookie in session
    response = session.post(
        'https://piazza.com/class', 
        data=r'from=%2Fsignup&email={0}&password={1}&remember=on&csrf_token={2}'.format(email, password, csrf_token)
    )

    # If non-successful http response, bail
    if response.status_code != 200:
        raise AuthenticationError(f"Could not authenticate.\n{response.text}")
    
    # Piazza might give a successful http response even if there is some other
    # kind of authentication problem. Need to parse the response html for error message
    pos = response.text.upper().find('VAR ERROR_MSG')
    errorMsg = None
    if pos != -1:
        end = response.text[pos:].find(';')
        errorMsg = response.text[pos:pos+end].translate({34: None}).split('=')[1].strip()

    if errorMsg is not None:
        raise AuthenticationError(f"Could not authenticate.\n{errorMsg}")
    
    
    current_directory = os.getcwd()

    #Retrieve all files in each section and download the files 
    for key in sections.keys():
        final_directory = os.path.join(current_directory, "downloaded_resources", key)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for item in sections[key]:
            print(item[1])
            
            # Open URL and read contents using requests
            page_response_obj = session.get(item[1])
            
             # Check if the request was successful
            if page_response_obj.status_code == 200:
                pdf_filename = os.path.join(final_directory, item[0])
                # Write the PDF content to a file
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(page_response_obj.content)
                print(f"Downloaded and saved: {pdf_filename}")
                
            else:
                print(f"Failed to download {item[0]}: {page_response_obj.status_code}")

if __name__ == "__main__":
    
    #use Piazza API to get classID
    p = Piazza()
    
    username = input("Email: ")
    password = input("Password: ")
    resourcesFile = input("Enter the name of the resources file (example = resources.html): ")

    p.user_login(username,password)
    classes = p.get_user_classes()

    for i in range(len(classes)):
        print("{}. {}".format((i+1), classes[i]['name']))

    idx = int(input("Which class are you downloading from: ")) - 1
    classID = classes[idx]['nid']
    
    #use pyquery to access the resources file
    doc = pq(filename = resourcesFile)
    script_content = doc('script').text()
    resources_json_str = re.search(r'var RESOURCES = (\[.*?\]);', script_content, re.DOTALL).group(1)
    json_object = json.loads(resources_json_str)
    out_file = open("allResources.json", "w")
    json.dump(json_object, out_file, indent = 6)
    out_file.close()

    #create dictionary containing all sections and the corresponding material
    sections = {}

    for item in json_object:
        if item['subject'][-3:] != "pdf" or item['config']['resource_type'] != "file":
            continue
        #section type
        sectionKey = item['config']['section']
        
        #create URL for material
        url = piazza_url + classID + '/' + item['id']
      
        if sectionKey not in sections.keys():
            sections[sectionKey] = []
                
        sections[sectionKey].append((item['subject'], url))

    download(username,password,sections)
    