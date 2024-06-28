from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def filter_listings():
    # Set up the WebDriver (e.g., for Chrome)
    driver = webdriver.Chrome()
    base_url = "https://cityexpert.rs/prodaja-nekretnina/novi-sad"
    current_page = 1
    referent_price_per_sqm = 1800
    apartments = []

    while True:
        try:
            if current_page > 30:
                break

            print()
            print(f"Starting with page = {current_page}")
            url = f"{base_url}?currentPage={current_page}"

            # Navigate to the website
            driver.get(url)
            current_page += 1

            listings = driver.find_elements(By.CLASS_NAME, "property-card")

            # Extract data from the elements
            for listing in listings:
                price_wrapper = listing.find_element(
                    By.CLASS_NAME, "property-card__price"
                ).text
                price = int(price_wrapper.split(" ")[0].replace(".", ""))

                size_wrapper = listing.find_element(
                    By.CLASS_NAME, "property-card__features"
                ).text
                size = int(size_wrapper.split(" ")[0].replace(".", ""))

                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")

                price_per_sqm = price / size

                if price_per_sqm <= referent_price_per_sqm:
                    apartments.append(
                        {
                            "price": price,
                            "price_per_sqm": price_per_sqm,
                            "link": link,
                        }
                    )
        except:
            print("Error occurred")
            continue

    driver.quit()

    return apartments


# Main function to run the script
def main():
    apartments = filter_listings()
    apartments.sort(key=lambda x: x["price"])

    for apartment in apartments:
        print()
        print(f"Total price: {apartment['price']} EUR")
        print(f"Price per sqm: {apartment['price_per_sqm']:0.2f} EUR")
        print(f"Link: {apartment['link']}")


if __name__ == "__main__":
    main()