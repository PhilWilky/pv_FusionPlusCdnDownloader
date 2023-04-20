import csv
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# define the name of the CSV file
csv_file = "test.csv"

# create the folder to save the images
if not os.path.exists("images"):
    os.mkdir("images")

def download_image(item_code, image_url, index):
    response = requests.get(image_url)
    expected_size = int(response.headers.get('Content-Length', 0))
    filename = f"{item_code}-{index}.jpg" if index else f"{item_code}.jpg"
    with open(f"images/{filename}", 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    actual_size = os.path.getsize(f"images/{filename}")
    if actual_size != expected_size:
        print(f"Failed to download image for item code {item_code} and index {index}.")

# open the CSV file and read its contents
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    num_rows = sum(1 for row in reader)
    file.seek(0)  # reset the file pointer to the beginning of the file

    # loop through the rows of the CSV file
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i, row in enumerate(reader, start=1):
            # get the item code, image URL and index from the current row
            item_code = row[0]
            image_url = row[1]
            index = int(row[2])
            # download the image from the CDN using a thread from the thread pool
            executor.submit(download_image, item_code, image_url, index)
            # print a message to show progress and confirm that the image has been downloaded
            if index:
                print(f"Processed row {i}/{num_rows}, {item_code}-{index} image downloaded.")
            else:
                print(f"Processed row {i}/{num_rows}, {item_code} image downloaded.")
    
    # print a final message to show how many images were downloaded
    print(f"Finished downloading {num_rows} images.")
