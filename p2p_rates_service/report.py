from .database import SessionLocal, Click, init_db

init_db()

def print_stats():
    db = SessionLocal()
    result = db.query(Click.target_url, Click.user_id).all()
    db.close()
    stats = {}
    for url, user in result:
        stats.setdefault(url, {})
        stats[url][user] = stats[url].get(user, 0) + 1
    for url, users in stats.items():
        print(f"URL: {url}")
        for user, count in users.items():
            print(f"  {user}: {count}")

if __name__ == "__main__":
    print_stats()
