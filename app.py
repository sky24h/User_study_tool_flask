# web-app for API image manipulation

from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import random

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

with open('./static/list.txt','r') as f:
    name_list = f.read().splitlines()

def random_pick():
    image_a = random.choice(name_list)
    image_b = random.choice(name_list)
    return image_a+'.png', image_b+'.png'

global count
count = 0

# default access page
@app.route("/")
def main():
    return render_template('index.html')


# upload selected image and forward to processing page
@app.route("/start", methods=["POST"])
def start():
    global user_id, count
    count = 1
    user_id = request.form['id']
    if user_id == '':
        return render_template('message.html', message1 = 'User ID cannot be EMPTY !', message2 = 'Please input one as you like.')
    image_a, image_b = random_pick()
    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)


# flip filename 'vertical' or 'horizontal'
@app.route("/select", methods=["POST"])
def select():
    global count
    image_a, image_b = random_pick()
    count += 1
    if count == 500:
        return render_template('message.html', message1 = 'Test completed successfully.', message2 = 'Thank you very much !')

    if 'A' in request.form['mode']:
        selected_filename = request.form['image_a']
    elif 'B' in request.form['mode']:
        selected_filename = request.form['image_b']
    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run()

