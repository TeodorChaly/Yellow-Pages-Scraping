from bs4 import BeautifulSoup
import requests

def get_url(object, region_location, page):
    object = object.replace(" ","%20")
    location = region_location.split(",")[0].replace(" ","%20")
    region = region_location.split(",")[1]
    print(object,location,region,page)
    url = f"https://www.yellowpages.com/search?search_terms={object}&geo_location_terms={location}%2C%20{region}&page={page}"
    results = requests.get(url)
    return results


def offline_page(results):
    with open("result.html", "w") as file:
        file.write(results.text)

    with open("result.html", "r") as file:
        a = file.read()

    return a

def find_all_links(soup):
    domain_url = "https://www.yellowpages.com"
    list_of_urls = []
    for link in soup.find_all(class_ = "info-section info-primary"):
        full_url = link.find(class_ ="business-name").get("href")
        list_of_urls.append(domain_url+full_url)
    return list_of_urls

def crawling_pages(list_of_urls):
    maximum = 3
    count = 0
    for link in list_of_urls:
        if maximum!= count:
            collecting_info(link)
            count+=1
        else:
            break
def collecting_info(url):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "lxml")
    try:
        name = soup.find(class_="dockable business-name").get_text()
    except:
        name = "No name"
    try:
        phone2 = soup.find(class_="inner-section")
        phone1 = phone2.find(class_="phone dockable").get("href")
        phone = phone1.replace("tel:", "")
    except:
        phone = "No phone"

    try:
        website = soup.find(class_="website-link dockable").get("href")

    except:
        website = "No website"

    try:
        address = soup.find(class_="address").get_text()

    except:
        address = "No address"

    try:
        email = soup.find(class_="email-business").get("href")

    except:
        email = "No address"

    print(name, phone,website, address, email)
def main():
    results = get_url("Interior Designers", "Atlanta, GA", 2)
    text_of_page = offline_page(results)
    soup = BeautifulSoup(text_of_page, "lxml")
    list_of_urls = find_all_links(soup)
    crawling_pages(list_of_urls)
main()