import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

global baseUrl

baseUrl = "https://www.celtictuning.co.uk/component/ctvc/search?dvla="

# Initialize Flask app
app = Flask(__name__)


def process(licensePlate):
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
    variant = vehicle[3]
    year = vehicle[4]
    fuel = vehicle[5]
    engine = vehicle[6]
    ecu = vehicle[7]

    print()

    print(
        f"Vehicle Details:\n"
        f"Brand:   {brand}\n"
        f"Name:    {name}\n"
        f"Model:   {model}\n"
        f"Variant: {variant}\n"
        f"Year:    {year}\n"
        f"Fuel:    {fuel}\n"
        f"Engine:  {engine}\n"
        f"ECU:     {ecu}"
    )

    res = {
        "brand": brand,
        "name": name,
        "model": model,
        "variant": variant,
        "year": year,
        "fuel": fuel,
        "engine": engine,
        "ecu": ecu,
    }

    return res


# Route to return vehicle details
@app.route("/vehicle/<string:licensePlate>", methods=["GET"])
def get_vehicle(licensePlate):
    res = None

    if licensePlate == None or licensePlate == "":
        # command has been used incorrectly
        res = {"error": "licensePlate is required"}

    else:
        # Vehicle data
        res = process(licensePlate)

    # Return the data as JSON
    return jsonify(res)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
