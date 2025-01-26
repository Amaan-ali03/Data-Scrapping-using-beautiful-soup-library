
import requests
from bs4 import BeautifulSoup
import csv
import json

## Billboard Top 100 SONGS {RANK,TITLE AND ARTISTS}

# Function to scrape data from the specified website
def scrape_billboard_hot100():
    # URL of the Billboard Hot 100 chart
    url = "https://www.billboard.com/charts/hot-100"
    
    # Sending a GET request to fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage: {response.status_code}")
        return

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store song data
    songs = []

    # Loop through each song item on the chart
    for song_item in soup.find_all("li", class_="o-chart-results-list__item"):
        # Extract the song title
        title_tag = song_item.find("h3", id="title-of-a-story")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract the artist name
        artist_tag = song_item.find("span", class_="a-no-trucate")
        artist = artist_tag.text.strip() if artist_tag else "N/A"

        # Extract the rank of the song
        rank_tag = song_item.find("span", class_="c-label")
        rank = rank_tag.text.strip() if rank_tag else "N/A"

        # Add the extracted data to the songs list if title and artist are available
        if title != "N/A" and artist != "N/A":
            songs.append({"Rank": rank, "Title": title, "Artist": artist})

    # Save the extracted data to a CSV file
    with open("billboard_hot100_available.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Rank", "Title", "Artist"])
        writer.writeheader()
        writer.writerows(songs)

    # Save the extracted data to a TXT file
    with open("billboard_hot100_available.txt", "w", encoding="utf-8") as file:
        for song in songs:
            file.write(f"Rank: {song['Rank']}, Title: {song['Title']}, Artist: {song['Artist']}\n")

    print("Billboard Hot 100 available data saved to billboard_hot100_available.csv and billboard_hot100_available.txt")


    ## SCAPPING BOOKS INFO {TITLE , PRICE AND AVAILABILITY}
# Function to scrape data from the specified website
def scrape_books_data():
    # URL of the website to scrape
    url = "http://books.toscrape.com/"
    
    # Sending a GET request to fetch the webpage content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the webpage: {response.status_code}")
        return

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store book data
    books = []

    # Extracting book information
    for book in soup.find_all("article", class_="product_pod"):
        # Extract the title of the book
        title = book.h3.a["title"]
        
        # Extract the price of the book
        price = book.find("p", class_="price_color").text
        
        # Extract the availability status of the book
        availability = book.find("p", class_="instock availability").text.strip()

        # Append the book data to the list
        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })

    # Save data to a TXT file
    with open("books_data.txt", "w", encoding="utf-8") as txtfile:
        for book in books:
            txtfile.write(f"Title: {book['Title']}, Price: {book['Price']}, Availability: {book['Availability']}\n")

    print("Scraping completed. Data has been saved in .txt format.")


# Main function
def main():
    print("Starting the web scraping process...")
    scrape_books_data()
    scrape_billboard_hot100()

if __name__ == "__main__":
    main()
