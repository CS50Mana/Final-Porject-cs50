#---converting Docs files and PFD files into text files---#
import os
import pdfplumber
#----write a function that converts pdf file into text file---#

def convert2(filename,startpage, endpage):
    pdf= pdfplumber.open(r"C:\\Users\\Manel\\Desktop\\CS_50\\GoogleTextToSpeech\\static\\uploads"+"\\" + filename)
    n=len(pdf.pages)
    page_start=(int(startpage))
    print(page_start)
    page_end=(int(endpage))
    print(page_end)
    final=""
    for page in range(page_start,page_end + 1):
        data=pdf.pages[page].extract_text()
        final= final + "\n" + data
    print("whole document data:{}".format(final))
    with open('speech.txt','a',encoding = 'utf-8') as essai:
             essai.write(final)
    return final

