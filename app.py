import os, subprocess, tempfile, shutil, uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template, after_this_request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_UPLOAD_MB','100')) * 1024 * 1024
EXTS = {'.mp4','.mov','.webm','.mkv','.mp3','.wav','.m4a','.ogg'}
VIDEO = {'360':'640:360','480':'854:480','720':'1280:720','1080':'1920:1080'}
AUDIO = {'mp3','m4a'}

@app.get('/health')
def health(): return jsonify(status='ok')

@app.get('/')
def home(): return render_template('index.html')

@app.get('/<page>')
def pages(page):
    if page not in {'about','privacy','terms','contact'}: return 'Not found',404
    return render_template('page.html', page=page)

@app.post('/api/convert')
def convert():
    upload = request.files.get('file')
    fmt = request.form.get('format','mp3')
    quality = request.form.get('quality','720')
    if not upload or not upload.filename: return jsonify(error='Choose a media file.'),400
    ext = Path(secure_filename(upload.filename)).suffix.lower()
    if ext not in EXTS: return jsonify(error='Unsupported input format.'),400
    if fmt not in {'mp3','m4a','mp4'}: return jsonify(error='Unsupported output format.'),400
    if fmt == 'mp4' and quality not in VIDEO: return jsonify(error='Unsupported resolution.'),400
    folder = tempfile.mkdtemp(prefix='mediasave_')
    src = os.path.join(folder, 'input'+ext)
    dest = os.path.join(folder, 'output.'+fmt)
    try:
        upload.save(src)
        if fmt == 'mp4':
            cmd = ['ffmpeg','-nostdin','-v','error','-y','-i',src,'-vf',f'scale={VIDEO[quality]}:force_original_aspect_ratio=decrease:force_divisible_by=2','-c:v','libx264','-preset','veryfast','-crf','25','-c:a','aac','-b:a','160k','-movflags','+faststart',dest]
        elif fmt == 'mp3':
            cmd = ['ffmpeg','-nostdin','-v','error','-y','-i',src,'-vn','-c:a','libmp3lame','-b:a','192k',dest]
        else:
            cmd = ['ffmpeg','-nostdin','-v','error','-y','-i',src,'-vn','-c:a','aac','-b:a','192k',dest]
        subprocess.run(cmd,check=True,timeout=150,capture_output=True)
        @after_this_request
        def cleanup(response):
            response.call_on_close(lambda: shutil.rmtree(folder,ignore_errors=True))
            return response
        return send_file(dest,as_attachment=True,download_name='mediasave-'+uuid.uuid4().hex[:8]+'.'+fmt)
    except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
        shutil.rmtree(folder,ignore_errors=True)
        return jsonify(error='Conversion failed. Check the file format or try a shorter clip.'),422
    except Exception:
        shutil.rmtree(folder,ignore_errors=True)
        return jsonify(error='Unexpected conversion error.'),500

@app.errorhandler(413)
def too_large(_): return jsonify(error='File exceeds the upload limit.'),413

if __name__ == '__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')))
