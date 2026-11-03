
import os

from app import app
from models import db, User, Ticket
from init_db import build_users, seed_tickets


def initialize_database(seed_demo_data=False):
    with app.app_context():
        db.create_all()

        if not seed_demo_data:
            print("Demo data seeding is disabled.")
            return

        if User.query.first() or Ticket.query.first():
            print("Existing database data preserved.")
            return

        users = build_users()
        seed_tickets(users)
        db.session.commit()
        print("Demo users and tickets seeded successfully.")


initialize_database(
    seed_demo_data=os.environ.get("SEED_DEMO_DATA", "").strip().lower()
    in {"1", "true", "yes"}
)

if __name__ == "__main__":
    app.run()
