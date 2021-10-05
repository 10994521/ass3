from event import create_app

if __name__ == '__main__':
    n_app = create_app()
    n_app.run(debug=True)


# Use this ocde to create a db file (when terminal doesn't work)

#from event import db, create_app
#app = create_app()
#ctx = app.app_context()
# ctx.push()
# db.create_all()
# quit()
