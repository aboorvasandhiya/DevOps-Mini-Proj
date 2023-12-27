from hal import hal_usonic as usonic
global Rfid_input

pin_input = []
password1 = [1,2,3,4]
password2 = [2,3,4,5]
password3 = [3,4,5,6]

ID1 = 989291917179
ID2 = 948765671378
ID3 = 26364129254

def main(pin_input):
    global password1, password2, password3
    if (pin_input == password1 or pin_input == password2 or pin_input == password3):
        print("CORRECT")
        return True
    else:
        print("WRONG")
        return False

def RFIDtest(Rfid_input):

    global ID1,ID2,ID3

    if (ID1 == Rfid_input) or (ID2 == Rfid_input) or (ID3 == Rfid_input):
        print("Correct")
        return True

    else:
        print("Wrong")
        return False
def checkultrasound(distance):
    if distance < 10:
        return True
    else:
        return False







if __name__ == "__main__":
    main()
