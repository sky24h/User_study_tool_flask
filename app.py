from flask import Flask, request, render_template, send_from_directory
import os
from PIL import Image
import random

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
image_dir = './static/images/'

list_method = ['ours/', 'real/', 'pix2pixHD/', 'SPADE/']
list_style = ['ink/', 'wat/', 'monet/', 'van/', 'cez/']

def random_pick():
    pick_style = random.choice(list_style)
    pick_method1 = random.choice(list_method)
    pick_method2 = random.choice(list_method)

    while (pick_method1==pick_method2):
        pick_method2 = random.choice(list_method)
    image_a = random.choice(os.listdir(image_dir + pick_method1 + pick_style))
    image_b = random.choice(os.listdir(image_dir + pick_method2 + pick_style))
    return pick_method1 + pick_style + image_a, pick_method2 + pick_style + image_b

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

@app.route("/select", methods=["POST"])
def select():
    global count
    image_a, image_b = random_pick()
    count += 1
    if count == 500:
        return render_template('message.html', message1 = 'Test completed successfully.', message2 = 'Thank you very much !')
    list_a, list_b = request.form['image_a'].split('/'), request.form['image_b'].split('/')
    
    with open('./results/' + user_id + '.txt', 'a') as f:
        if 'A' in request.form['mode']:
            selected_filename = request.form['image_a']
            f.write(list_a[0] + '_' + list_b[0] + '_' + list_a[1] + '\n')
            print(list_a[0], list_b[0], list_a[1])

        elif 'B' in request.form['mode']:
            selected_filename = request.form['image_b']
            f.write(list_b[0] + '_' + list_a[0] + '_' + list_a[1] + '\n')
            print(list_b[0], list_a[0], list_a[1])

    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)


@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)

if __name__ == "__main__":
    app.run()

