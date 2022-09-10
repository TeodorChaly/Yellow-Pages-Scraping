from bs4 import BeautifulSoup
import requests


def get_url(object, region_location, page):
    object = object.replace(" ", "%20")
    location = region_location.split(",")[0].replace(" ", "%20")
    region = region_location.split(",")[1]
    print(object, location, region, page)
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
    for link in soup.find_all(class_="info-section info-primary"):
        full_url = link.find(class_="business-name").get("href")
        list_of_urls.append(domain_url + full_url)
    return list_of_urls


def crawling_pages(list_of_urls):
    for link in list_of_urls:
        collecting_info(link)



def collecting_info(url):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "lxml")
    try:
        name = soup.find(class_="dockable business-name").get_text().replace(",",";")
    except:
        name = "No name"
    try:
        phone2 = soup.find(class_="inner-section")
        phone1 = phone2.find(class_="phone dockable").get("href")
        phone = phone1.replace("tel:", "")
    except:
        phone = "No phone"

    try:
        website = soup.find(class_="website-link dockable").get("href").replace(",",";")
        if "https://api.superpages.com/xml/se" in website:
            website = "Problem"
    except:
        website = "No website"

    try:
        address = soup.find(class_="address").get_text().replace(",",";")

    except:
        address = "No address"

    try:
        email = soup.find(class_="email-business").get("href")

    except:
        email = "No address"

    try:
        rating = soup.find(class_="yp-ratings")
        rating = rating.find_next().get("class")
        stars = ""
        for i in rating:
            if i != "rating-stars":
                stars += i
            else:
                pass

    except:
        stars = "No star"
    link = url
    csv_text = name + "," + phone + "," + website + "," + address + "," + email + "," + stars +"," + link + "\n"
    csv_editor(1,csv_text )


def csv_editor(status, csv_text):
    if status == 0:
        with open("results.csv", "w"):
            pass
    elif status == 1:
        with open("results.csv", "a") as file:
            file.write(csv_text)

def main():
    results = get_url("Interior Designers", "Atlanta, GA", 1)
    text_of_page = offline_page(results)
    soup = BeautifulSoup(text_of_page, "lxml")

    page_number = soup.find(class_="pagination").get_text()
    page_numbers = page_number.split("12345")[0].split("of")[1].strip()
    page_numbers = int(page_numbers) / 30

    csv_editor(0, None)

    for i in range(1,int(page_numbers)):
        results = get_url("Interior Designers", "Atlanta, GA", i)
        text_of_page = offline_page(results)
        soup = BeautifulSoup(text_of_page, "lxml")
        list_of_urls = find_all_links(soup)
        crawling_pages(list_of_urls)
    try:
        results = get_url("Interior Designers", "Atlanta, GA", page_numbers+1)
        text_of_page = offline_page(results)
        soup = BeautifulSoup(text_of_page, "lxml")
        list_of_urls = find_all_links(soup)
        crawling_pages(list_of_urls)
    except:
        print()

main()
