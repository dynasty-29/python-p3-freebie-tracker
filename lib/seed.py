#!/usr/bin/env python3

from models import session, Company, Dev, Freebie  

# comapnies
hybe = Company(name="HYBE", founding_year=2013)
jyp = Company(name="JYP", founding_year=2019)
sm = Company(name="SM", founding_year=2000)
bighit = Company(name="BIGHIT", founding_year=2010)

# my devs
dev1 = Dev(name="BTS")
dev2 = Dev(name="SHINee")
dev3 = Dev(name="STRAY KIDS")
dev4 = Dev(name="BIGBANG")

# freebies
freebie1 = Freebie(item_name="army", value=20, dev=dev1, company=hybe)
freebie2 = Freebie(item_name="strays", value=5, dev=dev2, company=jyp)
freebie3 = Freebie(item_name="shawol", value=15, dev=dev3, company=sm)
freebie4 = Freebie(item_name="vip", value=10, dev=dev4, company=bighit)
freebie5 = Freebie(item_name="purple", value=25, dev=dev1, company=hybe)

# Add all objects to session and commit
session.add_all([hybe, jyp, bighit, sm, dev1, dev2, dev3, freebie1, freebie2, freebie3, freebie4, freebie5])
session.commit()

# Print seeded data for confirmation
print("Database seeded successfully!")
for dev in session.query(Dev).all():
    print(f"{dev.name} has freebies: {[freebie.item_name for freebie in dev.freebies]}")

# Close session
session.close()
