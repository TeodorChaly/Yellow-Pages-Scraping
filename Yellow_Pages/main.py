from bs4 import BeautifulSoup
import requests

def get_url(object, location):
    url = "https://www.yellowpages.com/search?search_terms=Interior+Designers&geo_location_terms=Atlanta%2C+GA"
    results = requests.get(url)
    return results


results = get_url("Interior Designers", "Atlanta, GA")


with open("result.html", "w") as file:
    file.write(results.text)

with open("result.html", "r") as file:
    a = file.read()
    print(a)

suop = BeautifulSoup(results.text, "lxml")