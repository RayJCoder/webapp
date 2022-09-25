from website import create_app
from flask import Flask, render_template
import os

app = create_app()
    
if __name__ == '__main__':
    app.run(debug=True)
    # server_port = os.environ.get('PORT', '8080')
    # app.run(debug=False, port=server_port, host='0.0.0.0')

