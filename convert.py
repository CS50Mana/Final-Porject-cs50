#---converting Docs files and PFD files into text files---#
from docx import Document
import PyPDF2
from PyPDF2 import PdfFileReader

text="Direct_aid_demande.docx"

# write a function that takes a docx as argument and convert its paragraphs into text
def convert_doc(name_of_file):
    text=""
    doc_dict={}
    document=Document(name_of_file)
    index=0
    for par in document.paragraphs:
        index+=1
        if len(par.text)>0:
            doc_dict[index]=par.text
        par=list(doc_dict.values())
    i=0
    for i in range(len(par)):
        if par[i] !=' ':
            text = text + par[i] + ".\n"
    return text

#text_converted=convert_doc(text)
#print(text_converted)

#----write a function that converts pdf file into text file---#

# pdf convertor

def convert_pdf(file):
    #pdfFileObj=open(file_path,'rb')
    #create pdf file reader 
    pdfreader=PyPDF2.PdfFileReader(file)

    #ask the user whether she wants to convert the intire file or some pages
    replay= input("If you want to convert the intire text enter 1 ")

    if replay== '1':
        text_all=''
        # convert the intire pdf 
        for i in range(0,pdfreader.numPages):
            #create a page object
            pageobj=pdfreader.getPage(i)
            text_all=text_all + pageobj.extract_text()
        print(text_all)
        #save the intire file 
        with open('text_converted.txt','a',encoding="utf-8") as complete_text:
            complete_text.write(text_all)
        return text_all
    else:
        #ask the user for a number of the page she wants to convert
        
        while True:
            page_number_start=(input('give a page number(start): '))
            page_number_end=(input('give a page number(end): '))
            if page_number_start.isnumeric() and page_number_end.isnumeric():
                page_number_start= int(page_number_start) -1
                page_number_end=int(page_number_end) -1
                for i in range(page_number_start,page_number_end + 1):
                    pageobj=pdfreader.getPage(i)
                    text_Page=''
                    text_Page=text_Page + pageobj.extract_text()
                    print(text_Page)
                    with open('page.txt','a',encoding="utf-8") as essai:
                       essai.write(text_Page)
                return text_Page
            else:
                print("enter a number please! ")
        
    

text=convert_pdf("Master_thesis.pdf")
print(text)
