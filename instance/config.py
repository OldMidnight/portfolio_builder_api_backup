#!/usr/bin/env python3
import os
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ['KREOH_DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "-JT}!^RF5.2W8;5@)G|2R;J%U%"
UPLOAD_FOLDER = os.environ['KREOH_UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'ico'}