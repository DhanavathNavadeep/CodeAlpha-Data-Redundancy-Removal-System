from utils.database import insert_user


def validate(record):

    if record["Name"] == "":
        return False

    if "@" not in record["Email"]:
        return False

    if len(record["Phone"]) != 10:
        return False

    return True


def save(record):

    insert_user(
        record["Name"],
        record["Email"],
        record["Phone"]
    )