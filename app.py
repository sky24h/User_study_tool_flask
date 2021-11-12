from flask import Flask, request, render_template, send_from_directory
import os
import random
from utils import pick_with_style, pick

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#get all the paths
image_dir = './static/images/'
list_method_to_compare = [image_dir + x for x in os.listdir(image_dir)]
list_style_to_compare = os.listdir(list_method_to_compare[0])

#Set to True if you want to compare one to one.
one_to_one = True
#Set to False if there is only one type of output image.
with_style = True
#Set to True if the samples are randomly generated.
#Set to False if you want to compare samples which have same input (please change the file name to the same as the input).
random_pick = True
#Number of methods
num_method = len(list_method_to_compare)

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
            f.write(list_a[0] + '_' + list_b[0] + '_' + list_a[1] + '\n')
            print(list_a[0], list_b[0], list_a[1])

        elif 'B' in request.form['mode']:
            selected_filename = request.form['image_b']
            f.write(list_b[0] + '_' + list_a[0] + '_' + list_a[1] + '\n')
            print(list_b[0], list_a[0], list_a[1])

    return render_template('main.html', image_a = image_a, image_b = image_b, user_id = user_id, count = count)


@app.route('/<filename>')
def send_image(filename):
    return send_from_directory("./",filename)

if __name__ == "__main__":
    app.run()

