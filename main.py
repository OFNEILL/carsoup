import sys

import requests
from bs4 import BeautifulSoup

global baseUrl

baseUrl = "https://www.celtictuning.co.uk/component/ctvc/search?dvla="

# get command line arguments
args = sys.argv

# remove the first argument (as it is always the scipt name)
args.pop(0)

licensePlate = args[0]


def main(licensePlate):
    # URL of the webpage you want to get
    vehicle = None

    try:
        # add the number plate into URI of request
        url = baseUrl + licensePlate

        # Make the GET request
        print("Retrieving results for plate", licensePlate + "...")
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Retrieve the HTML on the page
            html = response.text
            print("[Code 200] Results received")
            print()

            vehicle = scrape(html)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except:
        print("Uh oh, an unspecified error occured. Talk to Joseph.")
        print()

    return vehicle


def scrape(html):
    # create a soup from html content
    soup = BeautifulSoup(html, "html.parser")

    # get vehicle vehicleAttributes
    print("Retrieving vehicle attributes...")

    vehicleAttributes = soup.find(class_="ctvs_list")
    print("Attributes retrieved")

    vehicleList = vehicleAttributes.find_all("p")
    vehicleList = vehicleAttributes.find_all("span") + vehicleAttributes.find_all("p")
    # para for para in paragraphs if not para.find('strong')]
    vehicle = [v for v in vehicleList if not v.find("strong")]

    vehicle = [v.get_text().strip() for v in vehicle if v.get_text().strip() != ""]

    # declare vars
    brand = vehicle[0]
    name = vehicle[1]
    model = vehicle[2]
    year = vehicle[3]
    fuel = vehicle[4]
    engine = vehicle[5]
    ecu = vehicle[6]

    print()

    print(
        f"Vehicle Details:\n"
        f"Brand:   {brand}\n"
        f"Name:    {name}\n"
        f"Model:   {model}\n"
        f"Year:    {year}\n"
        f"Fuel:    {fuel}\n"
        f"Engine:  {engine}\n"
        f"ECU:     {ecu}"
    )

    res = {
        "brand": brand,
        "name": name,
        "model": model,
        "year": year,
        "fuel": fuel,
        "engine": engine,
        "ecu": ecu,
    }

    return res


if licensePlate == None or licensePlate == "":
    # command has been used incorrectly
    print("Please specify a license when making a command")
    print()
    print("EXAMPLE:")
    print("python ecu-scraper REG41 TRO")
    print()

else:
    VEHICLE = main(licensePlate)
