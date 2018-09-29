from app import app

@app.route('/')
def index():
    return "Only the best doggos!"