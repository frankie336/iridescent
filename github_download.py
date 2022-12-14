import time
import requests
import os
import stem
import io
import pycurl
import stem.process
from stem.util import term
from stem.control import Controller
from stem import Signal



class GitHubCode():
    def __init__(self):

        self.access_token = "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"

    def change_torIP(self):
        """
        Change Tor Identity
        https://stem.torproject.org/faq.html
        """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print('Changed IP!')


    def get_single_contributors(self,page:int) ->int:
        """
        Use the GitHub API to get
        Repos with single contributors
        """
        self.change_torIP()  # change tor ip
        time.sleep(1)

        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }

        OWNER = "octocat"
        params = {
            "affiliation": OWNER,
            "collaborator": OWNER,
             "page": page,
            "per_page": 100,
        }



        response = requests.get("https://api.github.com/repositories",proxies=proxies, params=params)

        repositories = response.json()


        rep_len = len(repositories)


        repos_dicts = []

        for i in range(rep_len):
            name =  repositories[i]["name"]

            repos = repositories[i]["owner"]["repos_url"]

            rep_dict = {"name": name, "repos":repos}

            repos_dicts.append(rep_dict)

        return repos_dicts


    def view_cpp_repos(self):

        test = []

        headers = {
            "Authorization": f"token {self.access_token}"
        }

        repo_dicts = self.get_single_contributors(page=2)

        for dict in repo_dicts:

            time.sleep(10)

            print(dict)
            url = dict["repos"]

            self.change_torIP()


            # Send a GET request to the URL and store the response
            response = requests.get(url,headers=headers)

            if response.status_code == 200:

                self.change_torIP()
                time.sleep(1)

                print('hello')
                # Get the list of repositories from the response
                repositories = response.json()

                username = dict["name"]

                for repo in repositories:

                    time.sleep(1)
                    # Get the URL for the repository's contents
                    repo_url = f"https://api.github.com/repos/{username}/{repo['name']}/contents"

                    print(repo_url)



                    # Send a GET request to the URL and store the response
                    repo_response = requests.get(repo_url,headers=headers)

                    files = repo_response.json()

                    time.sleep(1000)


                    # Check the status code of the response to make sure the request was successful
                    if repo_response.status_code == 200:
                        # Get the list of files from the response
                        files = repo_response.json()

                        #print(files[0]["name"])

                        time.sleep(1000)

                        # Loop through the files and print the name of each file that has a C++ source file extension
                        for file in files:
                            test.append(file["name"])
                            if file["name"].endswith((".cpp", ".hpp", ".cc",".js")):
                                print(file["name"],'<--FOUND c++')
                    else:
                         print(f"No C++ files found in {repo['name']}")

            else:
                pass

            print(test)




def test_module():

    run = GitHubCode()
    run.view_cpp_repos()

test_module()