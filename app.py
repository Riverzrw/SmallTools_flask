import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from forms import UploadForm

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.sdf', '.mol', '.pdbqt']
app.config['UPLOAD_PATH'] = 'upload_files'

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/index')
def home():
    return index()


@app.route('/docking_new')
def docking():
    return render_template('docking_new.html')


@app.route('/get_target')
def get_target():
    return render_template('get_target.html')

@app.route('/protein_3D')
def get_3D_structure():
    return render_template('protein_3D.html')

# 验证表单：配体文件文件格式是否正确，蛋白文件格式是否正确
@app.route('/docking/check', methods = ['GET', 'POST'])
def check_upload():
    files = []
    if request.method == 'GET':
        return render_template('docking_new.html')
    else:
        form = UploadForm(CombinedMultiDict([request.form, request.files]))

        if form.validate():
            # 获取post提交的数据
            ligand_file = request.files.get('ligand_file')
            protein_file = request.files.get('protein_file')

            # secure_filename(ligand_file.filename) 获取文件的名字
            ligand_file_name = secure_filename(ligand_file.filename)
            protein_file_name = secure_filename(protein_file.filename)
            print(ligand_file_name, protein_file_name)
            files.append(ligand_file_name)
            files.append(protein_file_name)
            for file in files:
                if file:
                    file_ext = os.path.splitext(file)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                        # TODO 需要返回提醒用户上传文件格式不正确，正确的格式是什么
                        abort(400)

                # 保存文件到files文件夹
                # save(文件路径)
            ligand_file.save(os.path.join(app.config['UPLOAD_PATH'], ligand_file_name))
            protein_file.save(os.path.join(app.config['UPLOAD_PATH'], protein_file_name))
            return render_template('check.html', result=request.form, ligand_file_name=ligand_file_name, protein_file_name=protein_file_name)
        else:
            # TODO 需要把错误返回到页面上提示给用户
            print(form.errors)





if __name__ == '__main__':
    app.run()
