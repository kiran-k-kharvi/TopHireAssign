def validate_and_parse_query(query):
    count = 0
    for i in query:
        if i in {'[', ']', '{', '}'}:
            return False
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0
