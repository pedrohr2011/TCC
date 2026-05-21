# TCC: Mapa Vivo da Desigualdade Verde Urbana no Rio de Janeiro

Projeto de TCC que implementa um pipeline ETL de imagens Sentinel-2 no Google Earth Engine para visualizar vegetacao urbana e corpos hidricos no municipio do Rio de Janeiro. O resultado e exibido em um mapa interativo com camadas alternaveis, controle de opacidade e atualizacao sob demanda das imagens processadas.

## Objetivo

O projeto busca apoiar a analise da distribuicao desigual de areas verdes urbanas no Rio de Janeiro. Para isso, combina imagens multiespectrais Sentinel-2, indices espectrais de vegetacao e agua, processamento em nuvem e uma interface web local para exploracao visual.

## Principais Recursos

- Processamento de imagens Sentinel-2 SR Harmonized pelo Google Earth Engine.
- Composicao RGB para visualizacao da imagem real.
- Calculo de MNDWI para destacar rios, canais, lagoas e outros corpos hidricos.
- Calculo de NDVI para identificar vegetacao urbana.
- Mascara de agua aplicada sobre o NDVI para reduzir falso positivo em rios e lagoas.
- Filtro de vegetacao com limiar NDVI maior que `0.25`.
- Servidor Flask com cache das URLs de tiles geradas pelo GEE.
- Interface Leaflet com mapas base, camadas independentes, controle de opacidade e botao de atualizacao.

## Como Funciona

O fluxo principal esta em `servidor.py`.

1. O Flask inicia em `localhost:5000`.
2. Uma thread em segundo plano autentica no Google Earth Engine e executa o pipeline.
3. O frontend (`area_verde.html`) consulta `/api/tiles` ate as URLs estarem prontas.
4. O Leaflet carrega as camadas RGB, MNDWI e NDVI como tiles XYZ.
5. Ao clicar em **Atualizar Imagens GEE**, o frontend chama `/api/refresh`, o servidor reprocessa as imagens e substitui as camadas no mapa sem recarregar a pagina.

## Pipeline ETL

**Extracao:** a colecao `COPERNICUS/S2_SR_HARMONIZED` e filtrada por ponto de interesse no Rio de Janeiro, periodo de 2025 e cobertura de nuvens inferior a 10%. Os valores de reflectancia sao normalizados pela divisao por 10.000.

**Transformacao:** o sistema calcula a mediana temporal da colecao, gera os indices MNDWI e NDVI, remove areas classificadas como agua da camada de vegetacao e aplica o limiar de NDVI para destacar vegetacao urbana.

**Carga:** cada imagem processada e publicada pelo `getMapId()` do Google Earth Engine. As URLs autenticadas de tiles ficam em cache no Flask e sao consumidas diretamente pelo Leaflet.

## Indices Espectrais

| Indice | Formula | Bandas Sentinel-2 | Uso no projeto |
| --- | --- | --- | --- |
| MNDWI | `(Verde - SWIR) / (Verde + SWIR)` | `B3` e `B11` | Detectar corpos hidricos |
| NDVI | `(NIR - Vermelho) / (NIR + Vermelho)` | `B8` e `B4` | Identificar vigor da vegetacao |

## Stack Tecnologica

| Camada | Tecnologia | Funcao |
| --- | --- | --- |
| Linguagem | Python | Orquestracao do ETL e servidor local |
| Processamento geoespacial | Google Earth Engine API | Filtros, indices espectrais e tiles |
| Servidor web | Flask | Rotas, cache e entrega da interface |
| Mapa interativo | Leaflet.js | Renderizacao de tiles e controles do mapa |
| Interface | HTML, CSS e JavaScript | Painel lateral, sliders e polling assíncrono |
| Dados | Sentinel-2 SR Harmonized | Imagens multiespectrais com correcao atmosferica |

## Requisitos

- Python 3.10 ou superior.
- Conta com acesso ao Google Earth Engine.
- Projeto GEE configurado, caso sua conta exija um identificador de projeto.

## Instalacao

Clone o repositorio e entre na pasta:

```bash
git clone https://github.com/pedrohr2011/TCC.git
cd TCC
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Autentique o Google Earth Engine:

```bash
earthengine authenticate
```

Se for necessario informar o projeto do GEE, configure a variavel de ambiente antes de iniciar o servidor.

PowerShell:

```powershell
$env:GEE_PROJECT_ID="seu-projeto-gee"
```

CMD:

```bat
set GEE_PROJECT_ID=seu-projeto-gee
```

Linux/macOS:

```bash
export GEE_PROJECT_ID="seu-projeto-gee"
```

## Executando

Inicie o servidor:

```bash
python servidor.py
```

Depois acesse:

```text
http://localhost:5000
```

O navegador tambem e aberto automaticamente alguns segundos depois que o servidor sobe.

## Endpoints

| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/` | Serve a interface `area_verde.html` |
| GET | `/api/tiles` | Retorna as URLs de tiles em cache ou informa que o processamento ainda esta em andamento |
| GET | `/api/refresh` | Reexecuta o pipeline GEE e retorna novas URLs de tiles |

## Estrutura do Projeto

```text
.
├── servidor.py
├── area_verde.html
├── pipelineetl.py
├── requirements.txt
├── Documentação.pdf
├── README.md
└── Docs/
    ├── documentacao.html
    ├── manual_do_codigo.html
    ├── TCC_Pedro_Rainha-PF2.pdf
    ├── diagrama_arquitetura.png
    ├── diagrama_etl.png
    └── diagrama_stack.png
```

## Documentacao

A pasta `Docs/` contem materiais de apoio do TCC:

- `Docs/documentacao.html`: documentacao tecnica do pipeline, arquitetura, endpoints e bibliotecas.
- `Docs/manual_do_codigo.html`: explicacao detalhada do codigo e guia de manutencao.
- `Docs/TCC_Pedro_Rainha-PF2.pdf`: versao em PDF do trabalho.

## Observacoes Importantes

- As URLs de tiles do Google Earth Engine expiram depois de algumas horas.
- Quando o mapa ficar sem tiles, use **Atualizar Imagens GEE** para gerar novas URLs.
- Nao publique arquivos `.env`, chaves, tokens, contas de servico ou credenciais do Google no repositorio.
- O arquivo `pipelineetl.py` e uma versao de referencia com `geemap`; o fluxo principal do projeto usa `servidor.py`.

## Autor

Pedro Rainha
