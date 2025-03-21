from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.int("ADMIN")
DB_URI = env.str("DB_URI")

BOT_USERNAME = "Randomeuzbot"
