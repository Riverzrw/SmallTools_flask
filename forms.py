from wtforms import Form, FileField, StringField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed, FileRequired


class UploadForm(Form):
    # FileRequired 文件必须传
    # FileAllowed 允许上传的类型
    ligand_file = FileField(validators=[FileRequired(), FileAllowed(['sdf', 'pdbqt', 'pdb'])])
    ligand_file = StringField(validators=[InputRequired()])
