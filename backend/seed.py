from app import app
from models import db, Guest, Episode, Appearance
import csv
from datetime import datetime

with app.app_context():
    # Optional: Clear existing records
    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()

    db.session.commit()

    episode_number = 1  # we'll increment this

    with open('seed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            show_date_str = row['Show'].strip()
            try:
                show_date = datetime.strptime(show_date_str, '%m/%d/%y')
            except ValueError:
                print(f"Skipping invalid date: {show_date_str}")
                continue

            # Create episode
            episode = Episode(date=show_date, number=episode_number)
            db.session.add(episode)
            episode_number += 1

            # Get guest list (can be multiple guests in one row)
            guest_names = [name.strip() for name in row['Raw_Guest_List'].split(",")]
            occupation = row['GoogleKnowlege_Occupation'].strip()

            for name in guest_names:
                # Check if guest already exists
                guest = Guest.query.filter_by(name=name).first()
                if not guest:
                    guest = Guest(name=name, occupation=occupation)
                    db.session.add(guest)

                # Create appearance
                appearance = Appearance(episode=episode, guest=guest, rating=3)  # default rating
                db.session.add(appearance)

        db.session.commit()
        print("Database seeded successfully.")
