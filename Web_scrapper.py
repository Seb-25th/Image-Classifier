import pycurl
import re
import csv

# List of URLs of the pages to download the files
urls = [
    "https://www.bing.com/images/search?q=wine%20bottle&qs=n&form=QBIRMH&sp=-1&ghc=1&lq=0&pq=wine%20bottle&sc=10-11&cvid=3071C5F65A4E4AC3941F0E8BFFE80656&ghsh=0&ghacc=0&first=1",
    "https://www.bing.com/images/search?q=wine+images&form=HDRSC4&first=1"   
]

# Name of the file to save the links starting with "tse1", "tse2", "tse3", "tse4"
name_archivo = "links_tse.txt"

# Initialize curl
c = pycurl.Curl()

# List to store the links starting with "tse1", "tse2", "tse3", "tse4"
links_tse = []

# Callback function to write the links starting with "tse1", "tse2", "tse3", "tse4" in the file
def write_links(data):
    # Split the content by lines
    lines = data.decode('utf-8').split('\n')
    for line in lines:
        # If the line contains "tse1", "tse2", "tse3", or "tse4", add it to the list
        if "tse1" in line or "tse2" in line or "tse3" in line or "tse4" in line:
            links_tse.append(line)

# Process each URL
for url in urls:
    # Set URL for the request
    c.setopt(c.URL, url)

    # Reset the links_tse list for each URL
    links_tse = []

    # Set the callback function to write the links
    c.setopt(c.WRITEFUNCTION, write_links)

    # Execute request
    c.perform()

# Close Curl connection
c.close()

# Write the links starting with "tse1", "tse2", "tse3", or "tse4" in the file
with open(name_archivo, 'w', encoding='utf-8') as f:
    for link in links_tse:
        f.write(link + '\n')

print("Links starting with 'tse1', 'tse2', 'tse3', or 'tse4' saved in", name_archivo)

# Now we read the file and extract the URLs starting with "https://tse" and ending with "
with open(name_archivo, 'r', encoding='UTF8') as file:
    data = file.read().rstrip()

pattern = r'https://tse[^\s"]*?t=1'

urls = re.findall(pattern, data)

# Writing URLs to CSV file
with open('wine_urls.csv', 'w', newline='') as csvfile:
    fieldnames = ['URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for url in urls:
        writer.writerow({'URL': url})

print("URLs saved in wine_urls.csv")
