import YTplaylist
# from YTplaylist import db

app = YTplaylist.app

# from YTplaylist.blueprints import authBP
# app.register_blueprint(authBP.bp)

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)