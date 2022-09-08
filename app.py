from flask import Flask, request, render_template, send_from_directory
import os
import random
from utils import pick_with_style, pick

# declare constants
HOST = '0.0.0.0'
PORT = 5555

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#get all the paths
image_dir = './static/images'

image_dir = image_dir + '/' if image_dir[-1] != '/' else image_dir
list_method_to_compare = [os.path.join(image_dir, x) for x in os.listdir(image_dir)]

#Set to False if there is only one type of output image.
with_style = False
if with_style:
    list_style_to_compare = os.listdir(list_method_to_compare[0])

#Set to False if you want to compare images in pairs.
random_pick = True

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

    # if exist, continue counting
    if os.path.exists('./results/' + user_id + '.txt'):
        with open('./results/' + user_id + '.txt', 'r') as r:
            count = len(r.readlines()) + 1

    if user_id == '':
        return render_template('message.html', message1 = 'User ID cannot be EMPTY !', message2 = 'Please input one as you like.')
    if with_style:
        image_a, image_b = pick_with_style(list_method_to_compare, list_style_to_compare, random_pick = True)
    else:
        image_a, image_b = pick(list_method_to_compare, random_pick = True)
    print('image_a', image_a, 'image_b', image_b)

    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)

@app.route("/select", methods=["POST"])
def select():
    global count

    if with_style:
        image_a, image_b = pick_with_style(list_method_to_compare, list_style_to_compare, random_pick)
    else:
        image_a, image_b = pick(list_method_to_compare, random_pick)
    count += 1
    print('image_a', image_a, 'image_b', image_b)
    if count == 500:
        return render_template('message.html', message1 = 'Test completed successfully.', message2 = 'Thank you very much !')
    
    list_a, list_b = request.form['image_a'].replace(image_dir, '').split('/'), request.form['image_b'].replace(image_dir, '').split('/')
    
    with open('./results/' + user_id + '.txt', 'a') as f:
        if 'A' in request.form['mode']:
            selected_filename = request.form['image_a']
            if with_style:
                f.write(list_a[0] + '_' + list_b[0] + '_' + list_a[1] + '\n')
                print(list_a[0], list_b[0])
            else:
                f.write(list_a[0] + '_' + list_b[0] + '_' + '0' + '\n')
                print(list_a[0], list_b[0], list_a[1])

        elif 'B' in request.form['mode']:
            selected_filename = request.form['image_b']
            if with_style:
                f.write(list_b[0] + '_' + list_a[0] + '_' + list_a[1] + '\n')
                print(list_b[0], list_a[0])
            else:
                f.write(list_b[0] + '_' + list_a[0] + '_' + '0' + '\n')
                print(list_b[0], list_a[0], list_a[1])

    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)


@app.route('/<filename>')
def send_image(filename):
    return send_from_directory("./",filename)

if __name__ == "__main__":
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
