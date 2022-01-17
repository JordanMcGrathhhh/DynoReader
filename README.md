# DynoReader - Jordan McGrath - 1-17-2022

This program attempts to use Google's Tesseract OCR program to identify Horsepower and Torque figures from Dyno Sheets..
Despite only being able to automatically recognize and read two of the four original dyno sheets, this program serves as a great 
introduction to OCR and shows its true limits with less-than ideal input data.

As displayed in the code, OpenCV is used to attempt to give Tesseract a better shot at understanding the data presented.
To my surprise, it made the world of a difference in testing. 
Without the tweaks given by OpenCV, DynoReader wasn't able to read any of the supplied Dyno Sheets clearly. 
With two small commands (Changing RBG -> Gray scale and blowing up the image using INTER_CUBIC), Tesseract read 50% of the graphs supplied. 

The limitations really show in this program due to several key issues:
1). Non-standardization of Dyno Sheets
2). Iffy-guessing on Tesseract

As shown in the code, there's plenty of checks (and even some odd written code to catch unexpected results). That being said, it's impossible to catch 
every small mistake Tesseract makes- especially for cases like Fail-2-Dyno.jpg where the lines overlap the text.
Unfortunately, this is where OCR is not as magical as I could hope for. 
Going forward I'd like to explore this area a little more, I think more pre-processing would net more positive results. 

* To use this program:

1). Download Google's Tesseract program \n
2). Install pyTesseract and opencv-python
3). Run ./main.py and feed in Dyno sheets
