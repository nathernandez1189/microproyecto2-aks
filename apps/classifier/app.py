import io
import os
import threading
import time
import warnings

import torch
from flask import Flask, jsonify, render_template, request
from PIL import Image, ImageOps, UnidentifiedImageError
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

from common.observability import instrument

torch.set_num_threads(int(os.getenv('TORCH_NUM_THREADS', '1')))
Image.MAX_IMAGE_PIXELS = 20_000_000
warnings.simplefilter('error', Image.DecompressionBombWarning)
weights = MobileNet_V3_Small_Weights.IMAGENET1K_V1
model = mobilenet_v3_small(weights=weights).eval()
transform = weights.transforms()
lock = threading.Lock()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
instrument(app, 'classifier')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/healthz')
def health():
    return jsonify(status='ok')


@app.get('/readyz')
def ready():
    return jsonify(status='ready', model='MobileNetV3 Small', classes=len(weights.meta['categories']))


@app.errorhandler(413)
def too_large(_):
    return jsonify(error='La imagen supera el límite de 5 MB.'), 413


@app.post('/predict')
def predict():
    uploaded = request.files.get('img')
    if uploaded is None or not uploaded.filename:
        return jsonify(error='Adjunta una imagen en el campo img.'), 400
    try:
        image = Image.open(io.BytesIO(uploaded.read()))
        if image.format not in ('JPEG', 'PNG', 'WEBP'):
            return jsonify(error='Usa una imagen JPEG, PNG o WebP.'), 415
        image.load()
        image = ImageOps.exif_transpose(image).convert('RGB')
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        return jsonify(error='La imagen está dañada, no es válida o tiene demasiados píxeles.'), 400
    started = time.perf_counter()
    tensor = transform(image).unsqueeze(0)
    with lock, torch.inference_mode():
        probabilities = model(tensor).softmax(dim=1)[0]
        scores, indices = probabilities.topk(5)
    predictions = [{'label': weights.meta['categories'][i], 'score': round(float(s), 6)}
                   for s, i in zip(scores.tolist(), indices.tolist())]
    return jsonify(model='MobileNetV3 Small', dataset='ImageNet-1K',
                   predictions=predictions, inference_ms=round((time.perf_counter() - started) * 1000, 2),
                   pod=os.getenv('HOSTNAME', 'local'), width=image.width, height=image.height)
