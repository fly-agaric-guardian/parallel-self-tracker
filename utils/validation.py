from datetime import datetime

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_valid_record(record):
    Paragon_list = ["Catherine", "Lemieux", "ADHQ", 
                    "Workshop", "Arak", "Jahn", 
                    "Brand", "Niamh", "NewDawn",
                    "Nehemiah", "Gaffar", "Shoshanna",
                    "Gnaeus", "Aetio", "Scipius"]
    condition1 = record[0].isalpha() and record[1].isalpha() and record[0] in Paragon_list and record[1] in Paragon_list
    condition2 = record[2] in ["OTP", "OTD"]
    condition3 = record[3] in ["WIN", "LOSE"]
    condition4 = record[4].isdigit() and int(record[4]) >= 0
    condition5 = is_valid_date(record[5])
    return condition1 and condition2 and condition3 and condition4 and condition5