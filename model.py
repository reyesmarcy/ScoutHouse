"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    downpayment = db.Column(db.Integer, nullable=False)
    other_debts  = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed"""

        return f"""<User user_id={self.user_id}
                         email={self.email}
                         salary={self.salary}
                         downpayment={self.downpayment}
                         other_debts={self.other_debts}"""


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

