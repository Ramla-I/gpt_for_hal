from PyPDF2 import PdfWriter,PdfReader
import pymupdf4llm
import os

# This calculation doesn't matter, the file assistant api takes care of this
# The datasheet has about 320,000 words
# Each file in the file assistant should be less than 12k tokens by default 
# Default file embedding parameters = 20 chunks, each chunk has 800 tokens with 400 tokens overlapping 
# so total unique tokens = (400 unrepeated tokens * 20) + (400 tokens repeated 2x * 20) / 2 = 12000 tokens
# so lets try to make sure each pdf only has 8k words as 1 token = 0.75 words
# 320,000 / 8000 = 40 files

def split_pdf(pdf_path, num_split_pdfs=40, output_path="../datasheet/82599/82599_datasheet_split"):
    # input_pdf = PdfReader(open("datasheet/82599_datasheet.pdf", "rb"))
    pdf_path = pdf_path.strip('\'"')
    pdf_path = os.path.normpath(pdf_path)

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"The file at {pdf_path} does not exist.")
    
    with open(pdf_path, 'rb') as file:
        input_pdf = PdfReader(file)
        pdf_len = int(len(input_pdf.pages))
        print(pdf_len)

        split_pdf_len = int(pdf_len / num_split_pdfs)
        remainder = pdf_len % num_split_pdfs

        pdfs = []

        for i in range(num_split_pdfs):
            pdfs.append(PdfWriter())
            for j in range(split_pdf_len):
                page = input_pdf.pages[i * split_pdf_len + j]
                pdfs[i].add_page(page)

        assert(len(pdfs) == num_split_pdfs)
        # add the remainder pages to the last pdf
        for i in range(remainder):
            page = input_pdf.pages[num_split_pdfs * split_pdf_len + i]
            pdfs[num_split_pdfs - 1].add_page(page)

        sum = 0
        for i in range(num_split_pdfs):
            sum += len(pdfs[i].pages)

        assert(sum == pdf_len)

        for i in range(num_split_pdfs):
            with open(output_path + "_" + str(i) + ".pdf", "wb") as f:
                pdfs[i].write(f)



# extract specific portion of the pdf and save it as another pdf
def extract_part_of_pdf(pdf_path, page_start=None, page_end=None):
    pdf_path = pdf_path.strip('\'"')
    pdf_path = os.path.normpath(pdf_path)

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"The file at {pdf_path} does not exist.")
    
    with open(pdf_path, 'rb') as file:
        input_pdf = PdfReader(file)
        
        total_pages = len(input_pdf.pages)
        if page_start is None:
            page_start = 0
        if page_end is None or page_end > total_pages:
            page_end = total_pages

        pdf = PdfWriter()
        for page_num in range(page_start, page_end):
            pdf.add_page(input_pdf.pages[page_num])

        with open(pdf_path + "_" + str(page_start) + "_" + str(page_end) + ".pdf", "wb") as f:
            pdf.write(f)


# extract specific portion of the pdf and convert to a str
def extract_text_from_pdf(pdf_path, page_start=None, page_end=None):
    pdf_path = pdf_path.strip('\'"')
    pdf_path = os.path.normpath(pdf_path)

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"The file at {pdf_path} does not exist.")
        
    text = ''
    
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)

        total_pages = len(reader.pages)
        if page_start is None:
            page_start = 0
        if page_end is None or page_end > total_pages:
            page_end = total_pages

        for page_num in range(page_start, page_end):
            text += reader.pages[page_num].extract_text()
    
    return text

def extract_markdown_from_pdf(pdf_path):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text

if __name__ == "__main__":
    extract_part_of_pdf("../datasheet/82599/pf_regs_w_summary.pdf", 20, None)