import Testing_Functions


def test_pin1():


    test_password = [1,2,3,4]


    entry = Testing_Functions.main(test_password)

    assert (entry == True)




def test_wrong_pin():

    test_password = [9,8,7,6]

    entry = Testing_Functions.main(test_password)

    assert (entry == False)


def test_ultrasound():


    #entry = test_keypad.checkultrasound(distance = 7)

    entry = Testing_Functions.checkultrasound(distance=11)

    assert(entry == False)

def test_Correct_RFID():


    entry = Testing_Functions.RFIDtest(Rfid_input = 26369169255)

    assert(entry == False)


def test_Wrong_RFID():
    entry = Testing_Functions.RFIDtest(Rfid_input=26364129254)

    assert (entry == True)












