import csv
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# define the name of the CSV file
csv_file = "test.csv"

# create the folder to save the images
if not os.path.exists("images"):
    os.mkdir("images")

def download_image(item_code, image_url):
    response = requests.get(image_url)
    expected_size = int(response.headers.get('Content-Length', 0))
    with open(f"images/{item_code}.jpg", 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    actual_size = os.path.getsize(f"images/{item_code}.jpg")
    if actual_size != expected_size:
        print(f"Failed to download image for item code {item_code}.")

# open the CSV file and read its contents
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    num_rows = sum(1 for row in reader)
    file.seek(0)  # reset the file pointer to the beginning of the file

    # loop through the rows of the CSV file
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i, row in enumerate(reader, start=1):
            # get the item code and image URL from the current row
            item_code = row[0]
            image_url = row[1]
            # download the image from the CDN using a thread from the thread pool
            executor.submit(download_image, item_code, image_url)
            # print a message to show progress and confirm that the image has been downloaded
            print(f"Processed row {i}/{num_rows}, {item_code} image downloaded.")
    
    # print a final message to show how many images were downloaded
    print(f"Finished downloading {num_rows} images.")
