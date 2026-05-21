# -*- coding: utf-8 -*-
from flask import Flask, jsonify, send_from_directory
import ee
import os
import threading
import webbrowser
from app.gee_config import initialize_gee

app = Flask(__name__, static_folder=os.path.dirname(__file__))

# Inicializacao do Google Earth Engine
initialize_gee()

# Pipeline GEE para URLs de tiles
def gerar_urls():
    roi = ee.Geometry.Point([-43.3356, -22.8646])
    collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(roi)
        .filterDate('2025-01-01', '2025-12-31')
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        .map(lambda img: img.divide(10000)))
    image = collection.median()

    mndwi = image.normalizedDifference(['B3', 'B11']).rename('MNDWI')
    water_mask = mndwi.gt(0)
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    ndvi_sem_agua = ndvi.updateMask(water_mask.Not())
    vegetacao_urbana = ndvi_sem_agua.updateMask(ndvi_sem_agua.gt(0.25))

    return {
        'rgb':  image.getMapId({'bands': ['B4','B3','B2'], 'min': 0, 'max': 0.3})['tile_fetcher'].url_format,
        'agua': water_mask.selfMask().getMapId({'palette': ['0000FF']})['tile_fetcher'].url_format,
        'ndvi': vegetacao_urbana.getMapId({'min':0.25,'max':0.8,'palette':['90EE90','008000','006400']})['tile_fetcher'].url_format,
    }

# Cache inicial, carregado em segundo plano para nao travar a inicializacao
_cache = {'urls': None, 'loading': False, 'error': None}

def _carregar_cache():
    _cache['loading'] = True
    _cache['error'] = None
    try:
        _cache['urls'] = gerar_urls()
        print("✓ URLs GEE carregadas.")
    except Exception as e:
        _cache['error'] = str(e)
        print(f"✗ Erro ao carregar GEE: {e}")
    finally:
        _cache['loading'] = False

threading.Thread(target=_carregar_cache, daemon=True).start()

# Rotas da aplicacao
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'area_verde.html')

@app.route('/api/tiles')
def tiles():
    if _cache['loading']:
        return jsonify({'status': 'loading'}), 202
    if _cache['error']:
        return jsonify({'status': 'error', 'message': _cache['error']}), 500
    return jsonify({'status': 'ok', 'urls': _cache['urls']})

@app.route('/api/refresh')
def refresh():
    try:
        urls = gerar_urls()
        _cache['urls'] = urls
        return jsonify({'status': 'ok', 'urls': urls})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Inicializacao local
if __name__ == '__main__':
    threading.Timer(1.2, lambda: webbrowser.open('http://localhost:5000')).start()
    print("Servidor iniciado em http://localhost:5000")
    app.run(port=5000, debug=False)
