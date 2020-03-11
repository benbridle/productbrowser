# ProductBrowser

ProductBrowser is a product information browser, designed and created for use by staff at Lighting Direct. 

![ProductBrowser](https://i.imgur.com/tCjqzAm.gif)
<p align="center">(stock levels intentionally removed)</p>

ProductBrowser collates product information from five different systems used internally at Lighting Direct, making it immediately available and easily searchable to help with answering customer queries. The interface is designed to reduce the number of interactions required to find the desired information, while still being discoverable and intuitive.

## Note

The code in this repository is only intended to be used as a demonstration of programming ability. The database files, documents, and web scrapers containing sensitive information pertaining to Lighting Direct have all been removed, which has the effect of preventing the program from launching.

## Structure

The entirety of the program logic is within the `application_module/ldproductbrowser` folder, with the sole exception of the program entry point at `src/main/python/main.py`. 

## Libraries used

- PyQt5, for the user interface
- FBS, for cross-platform building
- SQLite3, for the product information database
- BeautifulSoup and Requests, for web scraping
- Pillow, for manipulating product images 