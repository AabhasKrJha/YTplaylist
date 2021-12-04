import YTplaylist
# from YTplaylist import db

app = YTplaylist.app

from YTplaylist.blueprints import auth
app.register_blueprint(auth.bp)

from YTplaylist.blueprints import dashboard
app.register_blueprint(dashboard.bp)

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)