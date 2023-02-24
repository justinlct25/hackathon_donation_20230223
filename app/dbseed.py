from fund import app, db
from fund.models import Tag, DonationPeriod, DonationAmount

OFFICIAL_TAGS = ["stress", "leisure", "work-life-balance", "family", "friends", "couple", "depression", "suicide", "introvert"]
OFFICIAL_DONATION_PERIODS = ["weekly", "monthly", "yearly"]
OFFICIAL_DONATION_AMOUNTS = [50, 25, 10, 5]

with app.app_context():
    for tag in OFFICIAL_TAGS:
        if Tag.query.filter(Tag.tag==tag).first() is None:
            tag = Tag(tag=tag)
            db.session.add(tag)
            db.session.commit()
    for period in OFFICIAL_DONATION_PERIODS:
        if DonationPeriod.query.filter(DonationPeriod.period==period).first() is None:
            period = DonationPeriod(period=period)
            db.session.add(period)
            db.session.commit()
    for amount in OFFICIAL_DONATION_AMOUNTS:
        if DonationAmount.query.filter(DonationAmount.amount==amount).first() is None:
            amount = DonationAmount(amount=amount)
            db.session.add(amount)
            db.session.commit()
