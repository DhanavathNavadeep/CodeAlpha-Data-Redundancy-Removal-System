from utils.similarity import similarity_score


def classify_record(record, database):

    new_name = record["Name"]
    new_email = record["Email"]
    new_phone = record["Phone"]

    for row in database:

        db_name = row[0]
        db_email = row[1]
        db_phone = row[2]

        if new_email == db_email:
            return "Duplicate"

        if new_phone == db_phone:
            return "Duplicate"

        score = similarity_score(new_name, db_name)

        if score >= 90:
            return "False Positive"

    return "Unique"