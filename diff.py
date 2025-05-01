#highlight all the lighting fixtures on the drawings.
import pandas as pd
import fitz
import time

file='devices.xlsx'
df=pd.read_excel(file, engine='openpyxl')
pdf=fitz.open('repair.pdf')
print("opened file")
 
itemshighlight = df[['Type', 'Rate']].values.tolist()
itemshighlight.reverse()

allrects = []
start=time.time()
for page_num in range(len(pdf)):
    print("finding items")
    page = pdf.load_page(page_num)
    for item, rate in itemshighlight:
        print(f"item: {item}")
        rects= page.search_for(item)
        allrects.append(rects)
        print(f"process {len(rects)} for item: {item}")

    print("Removing duplicates")
    for i in range(1, len(itemshighlight)):
        rectscopy = allrects[i]
        for j in range(0, i):
            if itemshighlight[i][0] in itemshighlight[j][0]:
                for x in range(len(allrects[j])):
                    for y in range(len(allrects[i])):
                        if (allrects[i][y].x0 == allrects[j][x].x0 and allrects[i][y].y0 == allrects[j][x].y0 and allrects[i][y].y1 == allrects[j][x].y1):
                           del rectscopy[y]
                           break
        
        allrects[i] = rectscopy

    print("Highlighting")
    for x in range(0, len(allrects)):
        for y in range(0, len(allrects[x])):
            highlight =page.add_highlight_annot(allrects[x][y])
            highlight.set_info(info={"title": str(itemshighlight[x][1]),"subject": itemshighlight[x][0]})
 
    print(f"highlight done for page {page_num} out of {len(pdf)} pages")
 
print(f"highlight done for pdf")
name= 'repairt.pdf'  #make sure to rename the new file. 
pdf.save(name, garbage=4, deflate=True)
end= time.time()
print("pdf saved as "+name)
print("process time took: ", int(end-start), "second")