from PIL import Image, ImageDraw, ImageFont
import os

# Path to folder containing the images
folder_path = "visuals"

# Dictionary to store images according to their title
image_dict = {}

# Loop through all files in folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Split filename into title and subtitle
        title, subtitle = filename.split("_")
        subtitle = subtitle.split(".")[0]
        # Open the image and add it to the dictionary
        image = Image.open(os.path.join(folder_path, filename))
        if title not in image_dict:
            image_dict[title] = {}
        image_dict[title][subtitle] = image

# Loop through image pairs and create new images
for title in image_dict:
    # Get images for this title
    normal_image = image_dict[title]["normal"]
    anormal_image = image_dict[title]["anormal"]
    # Create new image
    new_image = Image.new("RGB", (normal_image.width + anormal_image.width, normal_image.height), (255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    # Add normal image
    new_image.paste(normal_image, (0, 0))
    draw.text((0, normal_image.height), "normal", fill=(0, 0, 0))
    # Add anormal image
    new_image.paste(anormal_image, (normal_image.width, 0))
    draw.text((normal_image.width, normal_image.height), "anormal", fill=(0, 0, 0))
    # Save new image
    if not os.path.exists("new_visuals"):
        os.makedirs("new_visuals")
    new_image.save(os.path.join("new_visuals", f"{title}.png"))
