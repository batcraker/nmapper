from config.Server import Server
from flask import redirect, url_for
from controller.nmapper import nmapper_bp

app = Server()

@app.app.route('/')
def index():
    return redirect(url_for('nmapper_bp.index'))

#register the blueprint
app.app.register_blueprint(nmapper_bp)


if __name__ == '__main__':
    app.run(debug=True)
