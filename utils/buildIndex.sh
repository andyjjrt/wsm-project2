rm -r data/indexes/
python -m pyserini.index.lucene \
  --collection JsonCollection  \
  --input data/collection \
  --index data/indexes/raw/porterStemming \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
python -m pyserini.index.lucene \
  --collection JsonCollection  \
  --input data/collection \
  --index data/indexes/raw/noStemming \
  --generator DefaultLuceneDocumentGenerator \
  --stemmer none \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
python -m pyserini.index.lucene \
  --collection TrecwebCollection  \
  --input data/WT2G \
  --index data/indexes/trec/porterStemming \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw
python -m pyserini.index.lucene \
  --collection TrecwebCollection  \
  --input data/WT2G \
  --index data/indexes/trec/noStemming \
  --generator DefaultLuceneDocumentGenerator \
  --stemmer none \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw