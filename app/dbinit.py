from fund import app, db

# with app.app_context(): db.create_all()

app.app_context().push()
db.create_all()
