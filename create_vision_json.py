import os
import json
import re

def create_vision_benchmark_json(images_dir="images", output_file="vision_benchmark.json"):
    # Instruction for image-based puzzles
    INSTRUCTION = "Provide a descriptive one-sentence caption for the given image"
    
    # A regex pattern to match alphanumeric filenames ending with .jpg (e.g., a123b.jpg)
    pattern = re.compile(r'^[a-zA-Z0-9]+\.jpg$')
    
    # Read all files in the images directory
    files = os.listdir(images_dir)
    
    # This list will hold our JSON entries
    data = []
    
    # Iterate over files in the images directory
    for file_name in files:
        # Check if the file name is purely alphanumeric (plus the .jpg extension)
        if pattern.match(file_name):
            # Remove .jpg from the end to get the alphanumeric index
            idx = file_name[:-4]
            
            # Create one dictionary entry per valid JPG
            entry = {
                "index": idx,
                "category": "",
                "question": INSTRUCTION,
                "human_answer": ""
            }
            data.append(entry)
    
   
    # Write the list of dictionaries to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    create_vision_benchmark_json()
