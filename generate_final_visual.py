from PIL import Image
from fpdf import FPDF
import os

# Define the folder path and get the list of image filenames
folder_path = "visuals/"
filenames = os.listdir(folder_path)
image_filenames = [filename for filename in filenames if filename.endswith(".png")]

# Sort the image filenames by their name
image_filenames.sort()

# Define the page size and margins
PAGE_WIDTH = 210  # A4 paper width in mm
PAGE_HEIGHT = 297  # A4 paper height in mm
LEFT_MARGIN = 10  # left margin in mm
RIGHT_MARGIN = 10  # right margin in mm
TOP_MARGIN = 10  # top margin in mm
BOTTOM_MARGIN = 10  # bottom margin in mm

# Define the size of each image
IMAGE_WIDTH = (PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN) / 2  # image width in mm
IMAGE_HEIGHT = IMAGE_WIDTH  # image height in mm

# Calculate the number of rows of images that can fit on a single page
max_rows = int((PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) / IMAGE_HEIGHT)

# Create a new PDF document
pdf = FPDF()

# Pair the images and create a PDF document with fixed size images and multiple rows
for i in range(0, len(image_filenames), 2):
    # Add a new page to the PDF document if it's the beginning of a new row
    if i % (2 * max_rows) == 0:
        pdf.add_page()

    # Load the first image and resize it to fit the fixed size
    image1 = Image.open(os.path.join(folder_path, image_filenames[i]))
    image1.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))

    # Calculate the position of the first image on the current row
    x1 = LEFT_MARGIN + (PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN - 2 * IMAGE_WIDTH) / 2
    y1 = TOP_MARGIN + (i % (2 * max_rows)) * IMAGE_HEIGHT

    # Add the first image to the current row
    pdf.image(image1.filename, x1, y1, IMAGE_WIDTH, IMAGE_HEIGHT)

    # Load the second image and resize it to fit the fixed size if it exists
    if i + 1 < len(image_filenames):
        image2 = Image.open(os.path.join(folder_path, image_filenames[i + 1]))
        image2.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))

        # Calculate the position of the second image on the current row
        x2 = x1 + IMAGE_WIDTH
        y2 = y1

        # Add the second image to the current row
        pdf.image(image2.filename, x2, y2, IMAGE_WIDTH, IMAGE_HEIGHT)

# Save the PDF document to a file named "output.pdf"
pdf.output("output.pdf")
