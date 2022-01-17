import pytesseract as tes
import cv2

# Due to Tesseract being odd in how it displays some of the numbers/ results from the Dyno sheets
# we need to sanitize some of the input before displaying it.
# This is still in review but from what I can gather, this is made due to a false \n somewhere

def clean_array(arr):

    cleaned = []

    for data in arr:

        numbers = list(data)
        length = len(numbers)

        if "\n" in numbers:

            del numbers[numbers.index("\n"):(length+1)]
            cleaned.append(''.join(numbers))

        else:
            try:
                float(''.join(numbers))
                cleaned.append(''.join(numbers))
            except:
                print("[*] Found Non-Integer Data Figures [*]")

    return cleaned


tes.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path = input("Path to Input: ")

# Open Image in cv2
img = cv2.imread(path)

# Apply filters to increase likelihood of Tesseract picking it up..
# Tesseract doesn't fare well with the default dyno graphs
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

# Lets get the text from Tesseract
text = tes.image_to_string(img)

# Hopefully Tesseract was able to make a good guess, let's search through
# We're looking for two different stats
# Horsepower, commonly denoted "Power", "whp", "HP"
# Torque, commonly denoted "Torque", "Torques"
# This would be even easier, unfortunately most tuners use multiple runs
# Therefore there can be several occurrences of the words - we need the highest

power_keywords = ["power", "whp", "hp"]
torque_keywords = ["torque"]

power_found = []
torque_found = []

text = text.lower()
text = text.split(" ")

# Please note, this is not exactly the nicest way to do this searching - however
# It's kind of necessary due to 1). Tesseract picking up on spaces 2). Dyno Sheets
# With weird spacing... In an ideal world we could just use 'in'
for index, word in enumerate(text):

    for keyword in power_keywords:

        if keyword in word:

            # print(word)
            if text[index+1] == "=":
                power_found.append(text[index+2])
            else:
                power_found.append(text[index+1])

    for keyword in torque_keywords:

        if keyword in word:

            # print(word)
            if text[index + 1] == "=":
                torque_found.append(text[index + 2])
            else:
                torque_found.append(text[index + 1])

# Let's just do a quick check to ensure everything is smooth here...
# Theoretically the amount of words in both arrays combined should be even since there's two numbers per run
# So if the amount of the words is not even or not greater than 1... issues arose

if (len(power_found) + len(torque_found)) % 2 != 0:

    print("[*] Found an Odd Number of Data Figures [*]")
    exit(1)

elif len(power_found) + len(torque_found) < 1:

    print("[*] No Data Figures Found [*]")
    exit(1)

# This is where things could be different depending on who you ask
# We're going to take the highest horsepower found, and the torque that relates
# to it- not the highest of each :/

power_found = clean_array(power_found)
torque_found = clean_array(torque_found)

index = power_found.index(max(power_found))
print("Max HP: " + power_found[index])
print("Max Torque: " + torque_found[index])
