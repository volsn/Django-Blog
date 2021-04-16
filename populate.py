import os
import random
from faker import Faker
from miloblog import db
from miloblog.models import User, BlogPost, BlogCategory, Comment, UserStatus

# Drop existing data
db.session.query(User).delete()
db.session.query(BlogPost).delete()
db.session.query(Comment).delete()
db.session.commit()

EXAMPLE_TEXT = """
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque <a href="#">penatibus</a> et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, <strong>pretium quis, sem.</strong></p>
<p>Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim.</p>
<p><strong>Aliquam lorem ante</strong>, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. <strong>Etiam rhoncus</strong>. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante <a href="#">tincidunt tempus</a>.</p>
<blockquote>
 <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
</blockquote>
<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, <a href="#">nascetur ridiculus</a> mus. Donec quam felis, ultricies nec, pellentesque eu, <strong>pretium quis, sem.</strong></p>
<div class="row">
 <div class="col-md-4">
    <ul>
       <li>Donec quam felis</li>
       <li>Consectetuer adipiscing</li>
    </ul>
 </div>
 <div class="col-md-4">
    <ul>
       <li>Donec quam felis</li>
       <li>Consectetuer adipiscing</li>
    </ul>
 </div>
 <div class="col-md-4">
    <ul>
       <li>Donec quam felis</li>
       <li>Consectetuer adipiscing</li>
    </ul>
 </div>
</div>
<p>Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. <strong>Etiam rhoncus</strong>. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante <a href="#">tincidunt tempus</a>.</p>
"""

N_USERS = 10
N_BLOGPOSTS = 40
N_COMMENTS = 5

fake = Faker()

# Admin user
admin = User(email='boss@mail.com',
             username='admin_',
             password='bigboss')
admin.profile_image = 'admin_.png'
admin.status = UserStatus.admin
db.session.add(admin)
db.session.commit()

profile_pics = [file for file in os.listdir('miloblog/static/profile_pics')
                if file != 'admin_.png' and (file.endswith(('.jpg', '.jpeg', '.png',)))]
for _ in range(N_USERS):
    profile = fake.simple_profile()
    user = User(email=profile['mail'],
                username=profile['username'],
                password='qwerty')
    user.profile_image = random.choice(profile_pics)
    user.first_name = profile['name'].split()[0]
    user.last_name = profile['name'].split()[1]

    # random.choice(string.ascii_letters + string.digits) * 10 - random password
    db.session.add(user)
    db.session.commit()


images = [file for file in os.listdir('miloblog/static/articles')
          if file.endswith(('.jpg', '.jpeg', '.png',))]

for i in range(1, N_BLOGPOSTS + 1):
    blog_post = BlogPost(title=fake.sentence(),
                         text=EXAMPLE_TEXT,
                         main_image=random.choice(images),
                         short_description=fake.sentence(15),
                         category=random.choice(list(BlogCategory)[1:]),
                         user_id=random.randint(1, N_USERS))

    num_comments = random.randint(1, N_COMMENTS)
    for _ in range(num_comments):
        comment = Comment(user_id=random.randint(2, N_USERS),
                          blog=i,
                          approved=True,
                          text=''.join(fake.paragraphs(2)))
        db.session.add(comment)
        db.session.commit()

    comments = Comment.query.order_by(Comment.date.desc()).limit(num_comments)

    try:  # TODO
        reply = Comment(user_id=1,
                        reply_to=comments[random.randint(1, num_comments)].id,
                        blog=i,
                        approved=True,
                        text=''.join(fake.paragraphs(2)))
        db.session.add(reply)
    except:
        pass

    db.session.add(blog_post)
    db.session.commit()
