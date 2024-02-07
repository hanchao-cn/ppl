from quart import Quart, jsonify


from common.db import config

app = Quart(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/chatportal'.format(config.username, config.password,
                                                                      config.db_address)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
async def hello():
    user = await User.query.first()
    return jsonify(name=user.name)

if __name__ == "__main__":
    app.run()