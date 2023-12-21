import os
import shutil
import fitz

from app.loggers import *

def bucketing(input_path, output_path, low_effort_high_yield_min_page,low_effort_high_yield_max_page,high_effort_high_yield_min_page, high_effort_high_yield_max_page, high_effort_low_yield_min_page):
    output = dict()

    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        try:
            if file_path.endswith('.pdf'):
                pdf_document = fitz.open(file_path)
                num_pages = pdf_document.page_count
                if (num_pages >= low_effort_high_yield_min_page and num_pages <= low_effort_high_yield_max_page):
                    effort_yield = "low_effort_high_yield"
                elif (num_pages >= high_effort_high_yield_min_page and num_pages <= high_effort_high_yield_max_page):
                    effort_yield = "high_effort_high_yield"
                elif (num_pages >= high_effort_low_yield_min_page):
                    effort_yield = "high_effort_low_yield"
                else:
                    effort_yield = ""

                output_folder = os.path.join(output_path, "file_bucketing",
                                             effort_yield, f"page-{num_pages}")
                os.makedirs(output_folder, exist_ok=True)
                shutil.copy(file_path, output_folder)
                if f"page-{num_pages}" not in output:
                    output[f"page-{num_pages}"] = []

                output[f"page-{num_pages}"].append(os.path.join(output_folder, filename))
            else:
                logger.warning(f"Unsupported file type: {file_path}")
        except Exception as ex:
            raise ex
    return output
