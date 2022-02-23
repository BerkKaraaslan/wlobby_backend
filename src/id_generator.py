INITIAL_VALUE = 1

def get_user_id(): # This function returns current user id. We can use this id when creating a user.
    with open('IDs.txt') as f:
        lines = f.readlines()

    UserID = int(lines[0].rstrip())
    return UserID

def increment_user_id(): # This function increments user id. We MUST use this function after we call get_user_id function to ensure that our user id is up to date
    with open('IDs.txt') as f:
        lines = f.readlines()

    UserID = int(lines[0].rstrip())
    AdvertID = int(lines[1].rstrip())
    UserID = UserID + 1

    with open('IDs.txt', "w") as f:
        f.write(str(UserID) + "\n")
        f.write(str(AdvertID) + "\n")
        f.close()


def get_advert_id(): # This function returns current advert id. We can use this id when creating an advert.
    with open('IDs.txt') as f:
        lines = f.readlines()

    AdvertID = int(lines[1].rstrip())
    return AdvertID

def increment_advert_id(): # This function increments advert id. We MUST use this function after we call get_advert_id function to ensure that our advert id is up to date
    with open('IDs.txt') as f:
        lines = f.readlines()

    UserID = int(lines[0].rstrip())
    AdvertID = int(lines[1].rstrip())
    AdvertID = AdvertID + 1

    with open('IDs.txt', "w") as f:
        f.write(str(UserID) + "\n")
        f.write(str(AdvertID) + "\n")
        f.close()

def initialize_user_id(): # This function initializes user id with initial value which is 1
    with open('IDs.txt') as f:
        lines = f.readlines()

    UserID = INITIAL_VALUE
    AdvertID = int(lines[1].rstrip())

    with open('IDs.txt', "w") as f:
        f.write(str(UserID) + "\n")
        f.write(str(AdvertID) + "\n")
        f.close()

def initialize_advert_id(): # This function initializes advert id with initial value which is 1
    with open('IDs.txt') as f:
        lines = f.readlines()

    UserID = int(lines[0].rstrip())
    AdvertID = INITIAL_VALUE

    with open('IDs.txt', "w") as f:
        f.write(str(UserID) + "\n")
        f.write(str(AdvertID) + "\n")
        f.close()

def initialize_ids(): # This function initializes both user id and advert id with initial value which is 1
    UserID = INITIAL_VALUE
    AdvertID = INITIAL_VALUE

    with open('IDs.txt', "w") as f:
        f.write(str(UserID) + "\n")
        f.write(str(AdvertID) + "\n")
        f.close()
