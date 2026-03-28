from flask import render_template
from config import db, app
from Src.Router import Router

app.register_blueprint(Router)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  app.app_context().push()
  db.create_all()
  app.run()
