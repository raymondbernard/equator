import os
import requests

# We need PIL for saving local image objects
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True  # In case of partial or malformed images

from datasets import load_dataset

# ===============================================
# LOAD LOCAL PARQUET DATASET AND HANDLE PIL IMAGES
# Some rows have PIL image objects instead of URLs.
# We'll handle both cases.
# ===============================================


def main():
    # Two local Parquet shards
    data_files = {
        "train": ["train-00000-of-00002.parquet", "train-00001-of-00002.parquet"]
    }

    try:
        # Load locally, no streaming needed unless the file is huge.
        ds = load_dataset(
            "parquet",
            data_files=data_files,
            split="train"
            
        )
    except Exception as e:
        print(f"Error loading local Parquet file(s): {e}")
        ds = None

    if ds is None:
        print("Dataset could not be loaded from local Parquet. Exiting.")
        exit(1)

    os.makedirs("images", exist_ok=True)

    max_images = 10  # Adjust as needed
    count = 0

    for idx, record in enumerate(ds):
        if idx >= max_images:
            break

        # Adjust column names based on your Parquet schema
        unique_id = record.get("unique_id")
        image_data = record.get("image")

        if not unique_id or not image_data:
            print("Skipping record: Missing unique_id or image data.")
            continue

        # Case 1: 'image_data' is a URL string
        if isinstance(image_data, str):
            try:
                response = requests.get(image_data)
                if response.status_code == 200:
                    filename = os.path.join("images", f"{unique_id}.jpg")
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    count += 1
                    print(f"Downloaded {filename}")
                else:
                    print(f"Failed to download image for {unique_id} (HTTP {response.status_code}).")
            except Exception as err:
                print(f"Error downloading image for {unique_id}: {err}")

        # Case 2: 'image_data' is already a PIL Image object
        elif isinstance(image_data, Image.Image):
            filename = os.path.join("images", f"{unique_id}.jpg")
            try:
                image_data.save(filename)
                count += 1
                print(f"Saved local PIL image to {filename}")
            except Exception as err:
                print(f"Error saving PIL image for {unique_id}: {err}")
        else:
            # If the dataset's 'image' column is in some other format (dict, bytes, etc.)
            print(f"Unsupported image format for {unique_id}: {type(image_data)}")

    print(f"Downloaded {count} images successfully.")
if __name__ == "__main__":
    main()
