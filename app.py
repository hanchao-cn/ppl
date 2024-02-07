from quart import current_app

from common.db.DBPool import DBPool
from quartapp import create_app

app = create_app()


@app.before_serving
async def init_db():
    current_app.logger.info("Initializing database")
    current_app.db = DBPool(app=app)
    await current_app.db.create_all()
    current_app.logger.info("Database initialized")


@app.after_serving
async def close_db():
    current_app.logger.info("Closing database")
    del current_app.db
    current_app.logger.info("Database closed")


app.run(host='0.0.0.0', port=80)
