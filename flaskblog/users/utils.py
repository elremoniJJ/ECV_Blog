import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    print(f"Here is form_picture: {form_picture}")
    print(f"Here is form_picture.filename: {form_picture.filename}")
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_filename = f"{random_hex}{f_ext}"
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return pic_filename

