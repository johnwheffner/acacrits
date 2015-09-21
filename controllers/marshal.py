def index():
    response.title = "Marshals"
    grid = SQLFORM.grid(db.marshal, editable=True, user_signature=False)
    return locals()
