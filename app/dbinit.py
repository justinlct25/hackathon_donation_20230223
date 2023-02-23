from fund import app, db

with app.app_context(): db.create_all()

# app.app_context().push()
# db.create_all()


# def initialize_db(app):
#     app.app_context().push()
#     db.init_app(app)
#     db.create_all()
#     db.session.commit()

# initialize_db(app)