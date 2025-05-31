from sqlalchemy import create_engine, text

# Connect to your SQLite database
engine = create_engine("sqlite:///data.db")

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE giveaway_giveaway ADD COLUMN winner_cnt INTEGER DEFAULT 1"))
    conn.commit()
