def index():
    response.title = "Athletes"
    grid = SQLFORM.grid(db.athlete, editable=True, user_signature=False)
    return locals()
