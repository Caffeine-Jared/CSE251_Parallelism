"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
# TODO Add your threaded class definition here
class kill_me_i_hate_threading(threading.Thread): 
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = None

    def run(self):
        global call_count
        self.response = requests.get(self.url).json()
        call_count += 1
# TODO Add any functions you need here
def retrieve_top_api_urls():
    thread = kill_me_i_hate_threading(TOP_API_URL)
    thread.start()
    thread.join()
    return thread.response

def retrieve_film_details(api_urls): 
    film_thread = kill_me_i_hate_threading(api_urls["films"] + "6") # here is whre I can set the specific film im retrieving - which is no=w set to film 6
    film_thread.start() 
    film_thread.join()
    film = film_thread.response

    chars_threads = [kill_me_i_hate_threading(url) for url in film["characters"]]
    planets_threads = [kill_me_i_hate_threading(url) for url in film["planets"]]
    starships_threads = [kill_me_i_hate_threading(url) for url in film["starships"]]
    vehicles_threads = [kill_me_i_hate_threading(url) for url in film["vehicles"]]
    species_threads = [kill_me_i_hate_threading(url) for url in film["species"]]

    for thread in chars_threads + planets_threads + starships_threads + vehicles_threads + species_threads: 
        thread.start()

    for thread in chars_threads + planets_threads + starships_threads + vehicles_threads + species_threads:
        thread.join()
    
    # for thread in chars_threads:
    #     thread.start()

    # for thread in planets_threads:
    #     thread.start()

    # for thread in starships_threads:
    #     thread.start()

    # for thread in vehicles_threads:
    #     thread.start()

    # for thread in species_threads:
    #     thread.start()

    # for thread in chars_threads:
    #     thread.join()

    # for thread in planets_threads:
    #     thread.join()

    # for thread in starships_threads:
    #     thread.join()

    # for thread in vehicles_threads:
    #     thread.join()

    # for thread in species_threads:
    #     thread.join()

    chars = [thread.response for thread in chars_threads]
    planets = [thread.response for thread in planets_threads]
    starships = [thread.response for thread in starships_threads]
    vehicles = [thread.response for thread in vehicles_threads]
    species = [thread.response for thread in species_threads]

    return film, chars, planets, starships, vehicles, species
# USE LOG.WRITE FUNCTION FOR THE TIME STAMPS -  
def print_film_details(film, chars, planets, starships, vehicles, species):
    def display_names(title, name_list):
        log = Log(show_terminal=False)
        log.write('')
        log.write(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        log.write(", ".join(names))
    log = Log(show_terminal=False)
    log.write('-' * 40)
    log.write(f'Title   : {film["title"]}')
    log.write(f'Director: {film["director"]}')
    log.write(f'Producer: {film["producer"]}')
    log.write(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)
# using log.write actually slowed down the completion time by 0.001s
def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    # TODO Retrieve Top API urls
    api_urls = retrieve_top_api_urls()
    # TODO Retireve Details on film 6
    film, chars, planets, starships, vehicles, species = retrieve_film_details(api_urls)
    # TODO Display results
    print_film_details(film, chars, planets, starships, vehicles, species)
    
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
