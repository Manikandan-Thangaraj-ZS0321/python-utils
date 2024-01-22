import os
import shutil
import fitz

from app.loggers import logger

def bucketing(input_path, output_path, low_effort_min_page, high_effort_max_page):
    try:
        # Create a dictionary to store the output information
        output = dict()

        # Iterate through each file in the input path
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)

            # Check if the file is a PDF
            if file_path.endswith('.pdf'):
                # Open the PDF document using PyMuPDF
                pdf_document = fitz.open(file_path)
                num_pages = pdf_document.page_count

                # Iterate through the specified page ranges
                for i, j in zip(low_effort_min_page, high_effort_max_page):
                    if i <= num_pages < j:
                        # Create a folder for the current page range in the output path
                        folder_name = f'pages_from_{i}_to_{j}'
                        output_folder = os.path.join(output_path, "file_bucketing", folder_name)
                        os.makedirs(output_folder, exist_ok=True)

                        # Copy the PDF file to the output folder
                        shutil.copy(file_path, output_folder)

                        # Update the output dictionary with the file information
                        if folder_name not in output:
                            output[folder_name] = []
                        output[folder_name].append(os.path.join(output_folder, filename))
                        break

                # Close the PDF document
                pdf_document.close()

        # Return the output dictionary
        return output

    except FileNotFoundError as file_not_found_error:
        logger.error(f"Error: {file_not_found_error}. Please check if the input path exists.")
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")

