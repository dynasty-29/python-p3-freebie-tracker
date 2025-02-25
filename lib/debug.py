#!/usr/bin/env python3

from sqlalchemy import create_engine

from models import Company, Dev, session

# checking for specific queries 
my_dev = session.query(Dev).all()
print(my_dev)
my_co = session.query(Company).all()
print(my_co)

# Now testing the function give freebies
hybe = session.query(Company).filter_by(name="HYBE").first()
bts = session.query(Dev).filter_by(name="BTS").first()
hybe.give_freebie(bts, "for youth", 12)

session.commit()

# Verify Alice received the new freebie
print(bts.freebies)
if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()
