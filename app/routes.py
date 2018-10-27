from flask import render_template, flash, redirect, url_for # request, send_from_directory
from app import app # db
from pickle import load
from keras.models import load_model
from keras import backend
from app.forms import PhotoForm, CaptionForm
from app.model import extract_features_2, generate_caption
# from app.database import Image
from werkzeug.utils import secure_filename
# import os
import boto3

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['DISPLAY_FOLDER'], filename))
        # path = os.path.join(app.config['FINAL_FOLDER'], filename)

        s3 = boto3.resource('s3')

        if filename.rsplit('.', 1)[1].lower() in set(['jpg', 'jpeg']):
            # s3.Bucket('caption-maker-bucket').put_object(Key='image_{}.jpg'.format(db.session.query(Image).count()+1), Body=f)
            # stored_as = 'image_{}.jpg'.format(db.session.query(Image).count()+1)
            # image = Image(filepath = 'https://s3.amazonaws.com/caption-maker-bucket/' + stored_as, caption = caption)
            stored_as = 'uploaded_image.jpg'
            s3.Bucket('caption-maker-bucket').put_object(Key=stored_as, Body=f)

        elif filename.rsplit('.', 1)[1].lower() in set(['png']):
            stored_as = 'uploaded_image.png'
            s3.Bucket('caption-maker-bucket').put_object(Key='uploaded_image.png', Body=f)
        
        # db.session.add(image)
        # db.session.commit()

        # flash(caption)
        return redirect(url_for('caption', filename = stored_as))
    return render_template('index.html', title = 'The Caption App', form = form)

@app.route('/caption/<filename>', methods=['GET', 'POST'])
def caption(filename):
    # image = Image.query.filter_by(id = db.session.query(Image).count()).first_or_404()
    # caption = image.caption
    backend.clear_session()

    # load the tokenizer
    tokenizer = load(open('app/tokenizer.pkl', 'rb'))
    # hard-code max sequence length
    max_length = app.config['MAX_LENGTH']
    # load the model parameters
    model = load_model('app/resnet_model-ep03-loss3.586-val_loss3.777.h5')

    form = CaptionForm()
    if form.validate_on_submit():
        s3_client = boto3.client('s3')
        image = s3_client.get_object(Bucket='caption-maker-bucket',Key=filename)['Body']

        # prepare the photograph
        photo = extract_features_2(image)

        # generate the caption
        caption = generate_caption(model, photo, tokenizer, max_length)

        return render_template('caption.html', title = 'Generate Caption', filename = filename, caption = caption)
    return render_template('caption.html', title = 'Generate Caption', filename = filename, form = form)

# page describing use cases
# option for caption to be read aloud