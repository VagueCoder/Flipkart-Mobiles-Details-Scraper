# Flipkart-Mobiles-Details-Scraper
Another simple scraper using Python that scrapes the Mobile Details from [FlipKart.com](https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&sort=price_asc) to a CSV file for further use.

## Base System's Configurations
Sno. | Name | Version/Description
----:|:----:|:-------------------
1 | Operating System | Windows 10 Pro x64
2 | Language | Python 3.7.8rc1
3 | IDE | Visual Studio Code 1.51.0

## Imported Modules
Sno. | Name | Version
----:|:----:|:-------------------
1 | beautifulsoup4 | 4.9.3
2 | progressbar | 2.5
3 | pylint | 2.6.0
4 | requests | 2.25.0

Since VirtualEnv cannot be uploaded to Git repo, find the list of modules in [requirements.txt](https://github.com/VagueCoder/Flipkart-Mobiles-Details-Scraper/blob/master/requirements.txt).

## How to Use?
#### Run the scraper directly to run without filtering price:
```
python scraper.py
```
This will fetch something like [Mobiles-List-of-Price-Min-to-Max 13-Nov-2020 0817 hrs.csv](https://github.com/VagueCoder/Flipkart-Mobiles-Details-Scraper/blob/master/Mobiles-List-of-Price-Min-to-Max%2013-Nov-2020%200817%20hrs.csv) kind of data file.

#### Run the scraper by filtering on price:
```
python scraper.py 10000 20000
```
Here, 10000, 2000 are examples of prices you can mention and the program scrapes all the list of mobiles available between those price limits. The CSV file will have the prices mentioned on name.

#### Calling from a program:
```python
mobile_details = scraper.scrape_from_flipkart(low=minimum, high=maximum)
```
Replace minimum and maximum variable by strings of digits, like '10000', '20000' and the function returns a list of lists.
