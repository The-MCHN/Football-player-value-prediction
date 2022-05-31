
def get_club_codes():
    with open("clubcodes.txt", "r") as f:
        lines = f.readlines()
        return [line.replace("\n", "") for line in lines]

