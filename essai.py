import PyPDF2
from PyPDF2 import PdfFileReader

pdf_path=r"C:\Users\Manel\Desktop\CS_50\GoogleTextToSpeech\Master_thesis.pdf"
with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        print(number_of_pages)
        print(information)

print("Author" +': ' + information.author)
print("Creator" +': ' + information.creator)
print("Producer" +': ' + information.producer)

# creating a pdf file object
pdfFileObject = open(pdf_path,'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
print(pdfReader.numPages)
text_P=''
for i in range(0,pdfReader.numPages):
    # creating a page object
    pageObj = pdfReader.getPage(i)
    # extracting text from page
    text_P=text_P+pageObj.extract_text()
print(text_P)
#file1=open(r"C:\Users\Manel\Desktop\CS_50\GoogleTextToSpeech\Master.txt",'a')
#file1.writelines(text_P).encode("utf-8")

with open ('Master.txt','a',encoding="utf-8") as output:
    #write the response to the output file.
    output.write(text_P)
    print("Master thesis converted")
            