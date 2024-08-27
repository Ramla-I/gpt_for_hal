# The datasheet has about 320,000
# Each file in the file assitant should be less than 12k tokens by default 
# Default file embedding parameters = 20 chunks, each chunk has 800 tokens with 400 tokens overlapping 
# so total unique tokens = (400 unrepeated tokens * 20) + (400 tokens repeated 2x * 20) / 2 = 12000 tokens
# so lets try to make sure each pdf only has 8k words as 1 token = 0.75 words
# 320,000 / 8000 = 40 files

from PyPDF2 import PdfWriter,PdfReader
input_pdf = PdfReader(open("datasheet/82599_datasheet.pdf", "rb"))

num_split_pdfs = 40
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
    with open("datasheet/82599_datasheet_split_" + str(i) + ".pdf", "wb") as f:
        pdfs[i].write(f)