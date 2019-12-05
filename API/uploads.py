import os
from io import BytesIO
import boto3
import botocore
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

from flask import Blueprint, request, jsonify, Response, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from API.models import Website, User

s3 = boto3.resource('s3',
  aws_access_key_id=os.getenv('BUCKETEER_AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.getenv('BUCKETEER_AWS_SECRET_ACCESS_KEY'),
)

bucket = s3.Bucket('bucketeer-29e1dc32-7927-4cf8-b4de-d992075645e0')
bp = Blueprint('uploads', __name__, url_prefix="/uploads")


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/screenshot/grab', methods=('GET',))
@jwt_required
def grab_screenshot():
  user_id = get_jwt_identity()
  website = Website.query.filter_by(user_id=user_id).first()
  if website is None:
    return jsonify(screenshot_saved=False, message='No such Website.'), 404
  elif not website.active:
    return jsonify(screenshot_saved=False, message='Website Disabled.'), 200
  # options = Options()
  # options.headless = True
  # options.binary_location = os.environ['GOOGLE_CHROME_SHIM']
  # options.add_argument("--disable-gpu")
  # options.add_argument("--no-sandbox")
  # options.add_argument('window-size=1920x1080')
  chromedriver_path = "/app/.chromedriver/bin/chromedriver"
  chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
  options = webdriver.ChromeOptions()
  options.binary_location = chrome_bin
  options.add_argument("--disable-gpu")
  options.add_argument("--no-sandbox")
  options.add_argument('headless')
  options.add_argument('window-size=1920x1080')
  driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
  driver.get('http://' + website.domain + '.localhost:3000/')
  sleep(1)
  screenshot = driver.get_screenshot_as_png()
  screenshot = BytesIO(screenshot)
  bucket.upload_fileobj(screenshot, website.domain + '.kreoh.com.png')
  driver.quit()
  return jsonify(screenshot_saved=True), 200

@bp.route('/screenshot/<path:filename>', methods=('GET',))
def display_screenshot(filename):
  for f in bucket.objects.all():
    print(f.key)
  try:
    screenshot = BytesIO()
    bucket.download_fileobj(filename, screenshot)
    print('sdafs', screenshot)
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      return jsonify(screenshot_saved=False, message='No such Image.'), 404
    else:
      return jsonify(screenshot_saved=False, message='An Error has occured.'), 404
  return send_file(
    screenshot,
    mimetype='image/png',
  )

@bp.route('/favicon/set', methods=('POST', ))
@jwt_required
def save_favicon():
  user_id = get_jwt_identity()
  domain = User.query.filter_by(u_id=user_id).first().domain
  if 'favicon' not in request.files:
    return jsonify(msg="No File Sent."), 200
  favicon = request.files['favicon']
  if favicon.filename == '':
    return jsonify(msg='No Selected File.'), 200
  if favicon and allowed_file(favicon.filename):
    favicon_name = secure_filename(str(user_id) + '_' + domain + '_' + favicon.filename)
    favicon.save(os.path.join(current_app.config['UPLOAD_FOLDER'], favicon_name))
    return jsonify(msg='File Uploaded'), 201

# @bp.route('/favicon/<filename>', methods=('GET',))
# def get_favicon(filename):
#   return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/favicon/delete', methods=('POST',))
@jwt_required
def delete_favicon():
  filename = request.get_json()['filename']
  favicon = Path(current_app.config['UPLOAD_FOLDER'] + filename)
  try:
    favicon.unlink()
  except FileNotFoundError:
    pass
  return jsonify(), 200