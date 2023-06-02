import re
import requests
import csv
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Function to get email addresses from a webpage
def get_emails_from_webpage(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Extract email addresses using regular expression
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)

    return emails

# Function to get all links on a webpage
def get_links_from_webpage(url, domain):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the page
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and not href.startswith('javascript') and not href.startswith('#'):
            absolute_url = urljoin(url, href)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc == domain:
                links.append(absolute_url)

    return links

# Get user input for website URL
url = input("Enter website address to extract email addresses from: ")

# Get the domain name from the URL
domain = urlparse(url).netloc

# Initialize a set to keep track of visited URLs
visited = set()

# Initialize a list to store all email addresses
all_emails = []

# Initialize a list to store all links to be visited
links_to_visit = [url]

# Keep visiting links until there are no more links to visit
while links_to_visit:
    # Get the next link to visit
    link = links_to_visit.pop(0)

    # Check if the link has already been visited
    if link in visited:
        continue

    # Add the link to the visited set
    visited.add(link)

    # Call the function to get email addresses from the website
    emails = get_emails_from_webpage(link)

    # Print the list of emails
    print(f"Email addresses found on {link}:")
    for email in emails:
        print(email)

    # Add the emails to the all_emails list
    all_emails.extend(emails)

    # Call the function to get all links on the webpage
    links = get_links_from_webpage(link, domain)

    # Add the links to the links_to_visit list
    links_to_visit.extend(links)

# Save emails to a CSV file
filename = "emails.csv"
with open(filename, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Email"])
    for email in all_emails:
        writer.writerow([email])

print(f"The list of emails has been saved to the {filename} file.")
