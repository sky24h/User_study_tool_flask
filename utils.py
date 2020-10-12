import os
import random


def pick_with_style(path_method_to_compare, list_style_to_compare, random_pick = True):
    pick_style = random.choice(list_style_to_compare)
    pick_method1, pick_method2 = random.sample(set(path_method_to_compare),2)
    
    while (pick_method1==pick_method2):
        pick_method2 = random.choice(path_method_to_compare)
    image_a = random.choice(os.listdir(os.path.join(pick_method1, pick_style)))
    if random_pick:
        image_b = random.choice(os.listdir(os.path.join(pick_method2, pick_style)))
    else:
        image_b = image_a
    return os.path.join(pick_method1, pick_style, image_a), os.path.join(pick_method2, pick_style, image_b)

def pick(path_method_to_compare, random_pick = True):
    pick_method1, pick_method2 = random.sample(set(path_method_to_compare),2)
    
    while (pick_method1==pick_method2):
        pick_method2 = random.choice(path_method_to_compare)
    image_a = random.choice(os.listdir(pick_method1))
    if random_pick:
        image_b = random.choice(os.listdir(pick_method2))
    else:
        image_b = image_a
    return os.path.join(pick_method1, image_a), os.path.join(pick_method2, image_b)




