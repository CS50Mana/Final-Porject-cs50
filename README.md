#CS_50 Final Project: ReadMe

#### Video Demo:  <https://youtu.be/Gq-IxL9O2uA>

#### Description:
## Definition of the project
The idea came, as I wanted to listen to documents rather then reading them. 

The program takes a pdf file, converts it to a text file then uses google API TextToSpeech to convert the text file into an audio file that can be downloaded.

## Packages used in the program
I used GOOGLE API TextoSpeech which can be used 90 days for free. 
I had to create a virtual inveronnement to install all the packages that I needed with TextToSpeech and the other files as well. That way I do not need to install packages I need only for this project in the python installed on the machine. 

I used Flask framwork for the frontend, mainly in creating the login and sign up pages, using different packages that are included in flask, like flask_wtf to create a form.

I also used pdfplumber which is a library in python that converts pdf files into text files. I first used PyPDF2, however the result was not that good, as I got some letters converted to symbols when writing the file into text_file. 

## The web App 
I created a web application with html and css and Bootstrap. 
When using the application, one can login, signup and upload the file she/he wishes to be read. The file should not exceed 5000 characteres, otherwise the APi texttospeech could not convert it in an audio file. Tha is why I added the ability to choose the number of pages one want to convert. 

One Adventage of the app, is that one can download the file and saves it in her or his machine. 

## The app files
the app contains one main file app.py that runs different routes and functions as well as the texttospeech API. 

there are mainly 4 pages : Home, Upload, Login and SignUp

In the Home page I prefered leting the page as light as possible using only an image which reflect the application function in a form of a microphone. The image was downloaded form the web site [istock] (https://www.istockphoto.com/de).

In the pages Login and Sign Up I used flask framework and flask_wtf and wtfforms to create the forms. For the database, I used SQLAlchemy to store the data in the backend. 

In the Upload page I created a space where we can upload pdf files and send them to the server temporarly, then they can be saved in our local machine in order to make changes on them. Once the file is saved in the machine, we call the function convert2 to convert the file into a text file using Pdfplumber library. It is then saved in a text file which will be converted into an audio file by the texttospeech google API. 

Once the file is converted, it can be directaly downloaded by the user. 




## Things I want to improve in the future
I want to add the WaveNet voice to make the experience of listing to the file more realistic. I want also to change the voice speed setting to make the reader reads slowly. 

As a future project I would use Vision API and other google cloud APIs to be able to listen to scientific articles. 

I can enlarge the function of the program to accept also text files. The use of other languages would also be of an adventage.



