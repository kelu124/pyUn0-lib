from flask import Flask
from config import Configuration
from flask import render_template
import sys

sys.path.append(Configuration.LIB_PATH)
from spi_connector import SpiConnector

app=Flask(__name__, static_url_path='/static')
app.config.from_object(Configuration)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def activ():
    UN0RICK = SpiConnector()
    UN0RICK.test_spi(3)
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__=='__main__':
    app.run(Configuration.HOST)
