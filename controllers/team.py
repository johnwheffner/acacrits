def index():
    response.title = "Teams"
    grid = SQLFORM.grid(db.team, editable=True, user_signature=False)
    return locals()
