def index():
    response.title = "Officials"
    grid = SQLFORM.grid(db.official, editable=True, user_signature=False)
    return locals()
