import time

import requests
import json

def get_single_author_cpp_files_by_author(token, per_page=100, page=1):
    """
     Use the GitHub API to get
     Repos with single contributors
     """
    #self.change_torIP()  # change tor ip
    time.sleep(1)

    proxies = {
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050'
    }

    # Set the search parameters
    params = {
        "q": "language:c++author:1",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
        "page": page
    }

    headers = {
        "Authorization": f"Token {token}"
    }

    response = requests.get("https://api.github.com/repositories", proxies=proxies, params=params, headers=headers)


    user_list = []

    # If the request was successful, return the list of repositories
    if response.status_code == 200:
        results = response.json()

        for i in range(len(results)):
            res = results[i]["owner"]["login"]
            user_list.append(res)
            print(res)



    for item in user_list:
        with open('output/git_cpp_users.txt', 'w') as f:
            f.write(item + '\n')
            print('Hellooo')


        return user_list
    else:
        print(f"Request failed with status code {response.status_code}")
        return None





token = "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"
users =  get_single_author_cpp_files_by_author(token,per_page=100,page=1)


