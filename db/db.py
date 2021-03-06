from psutil import cpu_percent
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datatrain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(120), default="Puno")
    history = db.Column(db.String(360), default="Patrimonio del museo Carlos Dreyer")
    images = db.Column(db.Boolean, default=False)
    video = db.Column(db.Boolean, default=False)
    model_3d = db.Column(db.Boolean, default=False)

    model_id = db.Column(db.Integer, db.ForeignKey('model.id'),
        nullable=False)
    model = db.relationship('Model',
        backref=db.backref('profiles', lazy=True))
   
    def __repr__(self):
        return '<Profile %r>' % self.model


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), default="")
    bucket = db.Column(db.String(80), default="gs://nerf-models")
    type = db.Column(db.String(80), default="patrimonio")
    status = db.Column(db.String(80), default="starting")
    process = db.Column(db.String(80), default="")
    factor = db.Column(db.String(80), default="0") #
    factor_guess = db.Column(db.String(80), default="0") #
    checkpoint = db.Column(db.String(120), default="0")
    last_test= db.Column(db.String(120), default="0")
    last_step= db.Column(db.String(120), default="0")
    max_step= db.Column(db.String(120), default="0")
    time_train = db.Column(db.String(120), default="0")
    time_render = db.Column(db.String(120), default="0")
    config = db.Column(db.String(120), default="llff")
    files_checker = db.Column(db.String(120), default="00000000")
    
    
    def __repr__(self):
        return '<Model %r>' % self.model

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_step= db.Column(db.String(120), default="0")
    i_loss= db.Column(db.String(120), default="0")
    avg_loss= db.Column(db.String(120), default="0")
    weight_l2= db.Column(db.String(120), default="0")
    lr = db.Column(db.String(120), default="0")
    rays_per_sec= db.Column(db.String(120), default="0")
    psnr = db.Column(db.String(120), default="0") #
    ssim = db.Column(db.String(120), default="0") #
    eval_time = db.Column(db.String(120), default="0") #
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'),
        nullable=False)
    model = db.relationship('Model',
        backref=db.backref('trains', lazy=True))

    
    def __repr__(self):
        return '<Train %r>' % self.model

class Eval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    psnr= db.Column(db.String(120), nullable=False)
    ssim= db.Column(db.String(120), nullable=False)
    eval= db.Column(db.String(120), nullable=False)
    eval_path = db.Column(db.String(120), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'),
        nullable=False)
    model = db.relationship('Model',
        backref=db.backref('evals', lazy=True))

    
    def __repr__(self):
        return '<Eval %r>' % self.model

class Render(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type= db.Column(db.String(120), nullable=False)
    n_images= db.Column(db.String(120), nullable=False)
    render_path= db.Column(db.String(120), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'),
        nullable=False)
    model = db.relationship('Model',
        backref=db.backref('renders', lazy=True))

    
    def __repr__(self):
        return '<Render %r>' % self.model

class Tpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type= db.Column(db.String(120), default="VM")
    acelerator= db.Column(db.String(120), default="v3-08")
    cores= db.Column(db.String(120), default="8")
    tpu_mem= db.Column(db.String(120), default="128")
    mem= db.Column(db.String(120), default="365")
    cpu= db.Column(db.String(120), default="96")
    model = db.Column(db.String(120), default="")
    pid_model = db.Column(db.String(120), default="")
    status = db.Column(db.Boolean, default=False)
    type_step = db.Column(db.String(120), default="none")
    
    def __repr__(self):
        return '<TPU %r>' % self.acelerator

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), default="")
    cpu_percent = db.Column(db.String(120), default="0")
    mem_percent = db.Column(db.String(120), default="0")
    type_step = db.Column(db.String(120), default="none")

    def __repr__(self):
        return '<Performance %r>' % self.model