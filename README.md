# wsm-project2

109703040 洪晙宸

## Requirement
- python3, using 3.11.4
- perl

## Installation
```sh
pip install -r requirements.txt
```
Then create a data folder, and put `WT2G` into it, qrels into `qrels` folder, and queries into `queries` folder, which looks loke this:
```md
.
├── WT2G
│   ├── Wt01
│   ├── Wt02
│   ├── ...
├── qrels
│   ├── qrels.401-440.txt
│   └── qrels.441-450.txt
└── queries
    ├── topics.401-440.txt
    └── topics.441-450.txt
```
Other files will automatically generate.

## Run
First build index using `utils/buildIndex.py`
```sh
python utils/buildIndex.py
python convert.py
```
Then, run the queries
```sh
python main.py
```