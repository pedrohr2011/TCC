# -*- coding: utf-8 -*-
import ee
import geemap
import os
import webbrowser

GEE_PROJECT_ID = os.getenv('GEE_PROJECT_ID')

# 1. Inicializar Google Earth Engine
try:
    if GEE_PROJECT_ID:
        ee.Initialize(project=GEE_PROJECT_ID)
    else:
        ee.Initialize()
except Exception as e:
    print(f"Erro na inicialização: {e}\nTentando autenticar...")
    ee.Authenticate()
    if GEE_PROJECT_ID:
        ee.Initialize(project=GEE_PROJECT_ID)
    else:
        ee.Initialize()

# 2. Região de interesse (Jacarepaguá, RJ)
roi = ee.Geometry.Point([-43.3356, -22.8646])

# 3. Carregar Sentinel-2 (sem clip — GEE renderiza tiles em qualquer área navegada)
collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(roi)
    .filterDate('2025-01-01', '2025-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .map(lambda img: img.divide(10000)))

image = collection.median()

# 4. MNDWI - Índice de Água
mndwi = image.normalizedDifference(['B3', 'B11']).rename('MNDWI')
water_mask = mndwi.gt(0)

# 5. NDVI - Índice de Vegetação
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
ndvi_sem_agua = ndvi.updateMask(water_mask.Not())
vegetacao_urbana = ndvi_sem_agua.updateMask(ndvi_sem_agua.gt(0.25))

vis_ndvi = {
    'min': 0.25,
    'max': 0.8,
    'palette': ['lightgreen', 'green', 'darkgreen']
}


def fix_html_fullscreen(path):
    """Substitui height fixo por 100vh para o mapa ocupar a tela toda."""
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Remove height fixo do widget container e força fullscreen
    import re
    # Substitui qualquer height em px no container do mapa
    html = re.sub(r'(\.leaflet-container\s*\{[^}]*?)height\s*:\s*\d+px', r'\1height: 100vh', html)
    html = re.sub(r'(\.lm-Widget[^}]*?\{[^}]*?)height\s*:\s*\d+px', r'\1height: 100vh', html)

    # Garante que html e body também são fullscreen
    fullscreen_css = """
<style>
  html, body { margin: 0; padding: 0; height: 100%; }
  .lm-Widget, .jupyter-widgets, .leaflet-widgets,
  .widget-map, .jupyter-widgets-view {
    width: 100vw !important;
    height: 100vh !important;
  }
  .leaflet-container {
    width: 100vw !important;
    height: 100vh !important;
  }
</style>
"""
    html = html.replace('</head>', fullscreen_css + '</head>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


# 6. Mapa principal
print("Gerando mapa principal...")
Map = geemap.Map(center=[-22.8646, -43.3356], zoom=13)
Map.layout.height = '100vh'
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.3}, 'Imagem Real')
Map.addLayer(water_mask.selfMask(), {'palette': ['blue']}, 'Rios e Canais (MNDWI)')
Map.addLayer(vegetacao_urbana, vis_ndvi, 'Vegetação Urbana (NDVI)')

mapa_path = os.path.abspath('mapa_principal.html')
Map.save(mapa_path)
fix_html_fullscreen(mapa_path)
print(f"Mapa salvo em: {mapa_path}")
webbrowser.open(f'file:///{mapa_path}')

# 7. Mapa HD
print("Gerando mapa HD...")
Map_hd = geemap.Map(center=[-22.8646, -43.3356], zoom=13)
Map_hd.layout.height = '100vh'
Map_hd.add_basemap('HYBRID')
Map_hd.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.3}, 'Imagem Real (Sentinel-2)')
Map_hd.addLayer(water_mask.selfMask(), {'palette': ['blue']}, 'Rios e Canais (MNDWI)')
Map_hd.addLayer(vegetacao_urbana, vis_ndvi, 'Vegetação Urbana (NDVI)')

mapa_hd_path = os.path.abspath('mapa_hd.html')
Map_hd.save(mapa_hd_path)
fix_html_fullscreen(mapa_hd_path)
print(f"Mapa HD salvo em: {mapa_hd_path}")
webbrowser.open(f'file:///{mapa_hd_path}')

print("\nPronto!")
