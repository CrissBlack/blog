from Blog import create_app
from flask_gravatar import Gravatar

app = create_app()
gravatar = Gravatar(app,
                        size=100,
                        rating='x',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)

if __name__ == '__main__':
    app.run()