import requests
from bs4 import BeautifulSoup
import csv
import time


# Function to extract product details from a given Amazon page
def scrape_amazon_products(url):
    # Send a GET request to the URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store product details
    product_details = []

    # Find all product containers on the page
    products = soup.find_all('div', {'data-asin': True})  # Each product has a 'data-asin' attribute

    # Loop through each product and extract details
    for product in products:
        try:
            # Extract product name
            name = product.find('span', {'class': 'a-text-normal'}).text.strip()

            # Extract price (if available)
            price = product.find('span', {'class': 'a-price-whole'})
            price = price.text.strip() if price else 'Not Available'

            # Extract rating (if available)
            rating = product.find('span', {'class': 'a-icon-alt'})
            rating = rating.text.strip() if rating else 'Not Rated'

            # Extract seller name (if available)
            seller = product.find('span', {'class': 'a-size-small'})
            seller_name = seller.text.strip() if seller else 'Not Available'

            # Check if the product is in stock by looking for the "Out of stock" text
            out_of_stock = product.find('span', {'class': 'a-declarative'})

            if out_of_stock and 'Out of stock' in out_of_stock.text:
                continue  # Skip products that are out of stock

            # Store the product details in a dictionary
            product_details.append({
                'Product Name': name,
                'Price': price,
                'Rating': rating,
                'Seller Name': seller_name
            })

        except AttributeError as e:
            # Handle cases where some information might be missing
            print(f"Error extracting details for a product: {e}")
            continue

    return product_details


# Function to save the scraped data into a CSV file
def save_to_csv(products, filename="amazon_products.csv"):
    # Define the column names
    fields = ['Product Name', 'Price', 'Rating', 'Seller Name']

    # Open CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        # Write product details to the CSV file
        for product in products:
            writer.writerow(product)

    print(f"Data has been written to {filename}")


# Main function to scrape the data
def main():
    url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

    # Scrape product details from the Amazon page
    print("Scraping data...")
    products = scrape_amazon_products(url)

    if products:
        # Save the scraped data to a CSV file
        save_to_csv(products)
    else:
        print("No products found.")


if __name__ == "__main__":
    main()
