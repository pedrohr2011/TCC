# Desigualdade Verde Urbana no Rio de Janeiro

Projeto de TCC para visualizar vegetacao urbana e corpos hidricos no Rio de Janeiro usando imagens Sentinel-2, Google Earth Engine, Flask e Leaflet.

## O que o projeto faz

- Calcula NDVI para destacar vegetacao urbana.
- Calcula MNDWI para identificar rios e canais.
- Remove areas de agua da camada de vegetacao.
- Exibe as camadas em um mapa interativo com controle de opacidade.
- Atualiza as URLs de tiles do Google Earth Engine pelo servidor Flask.

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Autentique o Google Earth Engine, se ainda nao tiver feito isso:

```bash
earthengine authenticate
```

4. Se sua conta exigir um projeto especifico, informe o ID antes de iniciar:

```bash
set GEE_PROJECT_ID=seu-projeto-gee
```

5. Inicie o servidor:

```bash
python servidor.py
```

Depois disso, acesse `http://localhost:5000`.

## Arquivos principais

- `servidor.py`: servidor Flask e pipeline principal do Google Earth Engine.
- `area_verde.html`: interface do mapa em Leaflet.
- `pipelineetl.py`: versao de referencia que gera mapas com geemap.
- `Docs/`: documentacao tecnica do projeto.

## Observacoes

As URLs de tiles do Google Earth Engine expiram depois de algumas horas. Use o botao **Atualizar Imagens GEE** para gerar novas URLs durante a apresentacao ou testes.
