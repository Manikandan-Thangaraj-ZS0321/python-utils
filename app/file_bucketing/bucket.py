import os
import shutil
import fitz

from app.loggers import logger

def create_folder(output_path, category, folder_name):
    folder_path = os.path.join(output_path, "file_bucketing", category, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def copy_to_folder(file_path, output_folder):
    shutil.copy(file_path, output_folder)


def update_output(output, folder_name, output_folder, filename):
    if folder_name not in output:
        output[folder_name] = []
    output[folder_name].append(os.path.join(output_folder, filename))


def bucketing(input_path, output_path, min_page, max_page,
              low_effort_high_yield_min_page, low_effort_high_yield_max_page,
              high_effort_high_yield_min_page, high_effort_high_yield_max_page,
              high_effort_low_yield_min_page):
    try:
        output = dict()

        for root, dirs, files in os.walk(input_path):
            for filename in files:
                file_path = os.path.join(root, filename)

                if file_path.endswith('.pdf'):
                    pdf_document = fitz.open(file_path)
                    num_pages = pdf_document.page_count

                    if low_effort_high_yield_min_page <= num_pages < low_effort_high_yield_max_page:
                        for i, j in zip(min_page, max_page):
                            if i <= num_pages < j:
                                folder_name = f'pages_from_{i}_to_{j}'
                                output_folder = create_folder(output_path, "low_effort_high_yield", folder_name)
                                copy_to_folder(file_path, output_folder)
                                update_output(output, folder_name, output_folder, filename)
                                break

                    elif high_effort_high_yield_min_page <= num_pages < high_effort_high_yield_max_page:
                        for i, j in zip(min_page, max_page):
                            if i <= num_pages < j:
                                folder_name = f'pages_from_{i}_to_{j}'
                                output_folder = create_folder(output_path, "high_effort_high_yield", folder_name)
                                copy_to_folder(file_path, output_folder)
                                update_output(output, folder_name, output_folder, filename)
                                break

                    elif num_pages > high_effort_low_yield_min_page:
                        folder_name = f'pages_above_{high_effort_low_yield_min_page}'
                        output_folder = create_folder(output_path, "high_effort_low_yield", folder_name)
                        copy_to_folder(file_path, output_folder)
                        update_output(output, folder_name, output_folder, filename)

                    pdf_document.close()

        return output

    except FileNotFoundError as file_not_found_error:
        logger.error(f"Error: {file_not_found_error}. Please check if the input path exists.")
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")

