import requests
import re
from bs4 import BeautifulSoup


# Function to get the HTML content
def get_html(url):
    response = requests.get(url)

    return response.content


# Function to parse the HTML and filter results
def filter_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    listings = soup.find_all("div", class_="flex w-2/3 flex-col justify-between py-2")

    apartments = []

    for listing in listings:
        wrapper_div = listing.find(
            "div", class_="w-3/8 flex-shrink-0 overflow-clip text-right desk:w-1/3"
        )

        # Extracting numerical values from text
        try:
            price_byte = wrapper_div.find(
                "p",
                class_="rounded-tl bg-spotlight px-2 py-1 text-lg font-bold desk:text-2xl",
            ).encode("utf8")
            price = extract_integer(price_byte)

            size_byte = wrapper_div.find(
                "p",
                class_="rounded-bl border border-spotlight bg-spotlight-300 px-2 text-2xs font-medium text-spotlight-700 desk:text-xs",
            ).encode("utf8")
            size = extract_integer(size_byte)
        except ValueError:
            continue  # skip this listing if there are issues with extracting values

        if size <= 1800:
            link = listing.find("a")["href"]
            apartments.append(
                {
                    "price": price,
                    "price_per_sqm": size,
                    "link": f"https://www.4zida.rs{link}",
                }
            )

    return apartments


def extract_integer(byte_value):
    split_value = byte_value.split(b">")
    value = split_value[1].split(b"\xc2")[0]
    value = int(value.decode("utf8").replace(".", ""))

    return value


# Main function to run the script
def main():
    current_page = 1
    base_url = "https://www.4zida.rs/prodaja-stanova/novi-sad"
    all_results = []

    while True:
        print(f"Starting with page = {current_page}")
        url = f"{base_url}?strana={current_page}"
        html = get_html(url)
        if current_page > 25:
            break

        apartments = filter_listings(html)

        all_results.extend(apartments)
        current_page += 1

    for result in all_results:
        print()
        print(f"Total price: {result['price']} EUR")
        print(f"Price per sqm: {result['price_per_sqm']} EUR")
        print(f"Link: {result['link']}")


if __name__ == "__main__":
    main()