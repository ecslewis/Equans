import fitz
import re
#note: please repair pdf before proceeding with the code as it WILL NOT work if the file is corrupted.
#proceed on bluebeam and repair the file.
#process time takes 20-30 mins depending on size of file

doc = fitz.open('fet.pdf')

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    annot = page.first_annot
    while annot:
        if annot.type[0] == fitz.PDF_ANNOT_SQUARE:   # since its a rectangle
            rect = annot.rect
            text = page.get_textbox(rect)

            # extract
            match = re.search(r'\d+', text)
            if match:
                number = match.group()
                annot.set_info(subject=number)
                annot.update()
                print(f"Extracted Number: {number}")
            # else:
            #     print(f"No number found at {rect}")
        annot = annot.next

#savce changes
print("Uploaded changes...")
doc.save("fet1.pdf", garbage=3, incremental=False)
print("DONE! check your files")

