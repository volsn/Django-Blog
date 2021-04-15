import sys
import logging
from miloblog import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from miloblog.models import BlogPost, User, Comment, NewsletterSubscription

admin = Admin(app)
admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(NewsletterSubscription, db.session))

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run()
