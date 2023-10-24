from factory import db, bcrypt, auth

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @auth.verify_password
    def check_login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return True
        return False
