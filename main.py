import os, shutil, subprocess, json
from tqdm import tqdm
from searcher.Searcher import Searcher
from utils import generateQueries
from sklearn.linear_model import LogisticRegression

# If results sir doesn't exist, create it to store the result
if os.path.exists("data/results"):
  shutil.rmtree("data/results")
os.mkdir("data/results")

def search(indexPrefix="data/indexes", indexesFolder="raw/noStemming", searchType="bm25", query="", k=1000):
  searcher = Searcher(os.path.join(indexPrefix, indexesFolder))
  if searchType == "bm25":
    searcher.set_bm25(2, 0.75)
  elif searchType == "laplace":
    searcher.set_qld()
  elif searchType == "jm":
    searcher.set_jm(0.2)
  else:
    raise ValueError("searchType should be one of the followings: bm25, laplace, jm")
  
  hits = searcher.search(query, k=searcher.num_docs if k == -1 else k)

  del searcher
  return hits

def generateSearchResult(indexPrefix="data/indexes", indexesFolder="raw/noStemming", searchType="bm25", queriesRange="401-440"):
  queries = generateQueries(os.path.join("data/queries", f"topics.{queriesRange}.txt"))
  result = dict()

  for (id, query) in tqdm(queries, desc=f"{indexesFolder}/{searchType}", leave=False):
    hits = search(indexPrefix, indexesFolder, searchType, query, 1000)
    result[id] = hits

  if not os.path.exists("data/results/raw"):
    os.mkdir("data/results/raw")
  with open(os.path.join("data/results/raw", f"query.{queriesRange}-{indexesFolder.replace('/', '-')}-{searchType}.txt"), "w") as f:
    for id in result:
      for (i, hit) in [r for r in enumerate(result[id]) if r[1].score > 0]:
        f.write(f"{id} Q0 {hit.docid} {i + 1} {hit.score:.5f} {searchType}\n")
  
  if not os.path.exists("data/results/json"):
    os.mkdir("data/results/json")
  res = subprocess.run(['perl', 'trec_eval.pl', f"data/qrels/qrels.{queriesRange}.txt", os.path.join("data/results/raw", f"query.{queriesRange}-{indexesFolder.replace('/', '-')}-{searchType}.txt")], capture_output=True)
  with open(os.path.join("data/results/json", f"query.{queriesRange}-{indexesFolder.replace('/', '-')}-{searchType}.json"), "w") as f:
    f.write(res.stdout.decode())
  
  return {
    "json": json.loads(res.stdout.decode()),
    "result": {res: {doc.docid: doc.score for doc in result[res]} for res in result}
  }
  
def learningToRank(indexPrefix="data/indexes", indexesFolder="raw/noStemming",learningMaterials=None, trainingRange="401-440", testingRange="441-450"):
  queries = generateQueries(os.path.join("data/queries", f"topics.{trainingRange}.txt"))
  scoreData = dict()
  searchTypes = ["bm25", "laplace", "jm"]

  for (id, query) in tqdm(queries, desc=f"{indexesFolder}", leave=False):
    for searchType in searchTypes:
      hits = search(indexPrefix, indexesFolder, searchType, query, -1)
      for hit in hits:
        if not f"{id}.{hit.docid}" in scoreData:
          scoreData[f"{id}.{hit.docid}"] = dict()
        scoreData[f"{id}.{hit.docid}"][searchType] = hit.score
    
  trainingData = list()
  with open(f"data/qrels/qrels.{trainingRange}.txt", "r") as f:
    lines = f.readlines()
    for _line in lines:
      line = _line.strip("\n").split(" ")
      if f"{line[0]}.{line[2]}" in scoreData:
        if "bm25" in scoreData[f"{line[0]}.{line[2]}"] and "laplace" in scoreData[f"{line[0]}.{line[2]}"] and "jm" in scoreData[f"{line[0]}.{line[2]}"]:
          trainingData.append(([scoreData[f"{line[0]}.{line[2]}"]["bm25"], scoreData[f"{line[0]}.{line[2]}"]["laplace"], scoreData[f"{line[0]}.{line[2]}"]["jm"]], int(line[3])))
          
  cls = LogisticRegression()
  cls.fit([data[0] for data in trainingData], [data[1] for data in trainingData])
  
  queries = generateQueries(os.path.join("data/queries", f"topics.{testingRange}.txt"))
  
  if not os.path.exists("data/results/raw"):
    os.mkdir("data/results/raw")
  results = dict()
  for (id, query) in tqdm(queries, desc=f"{indexesFolder}", leave=False):
    scoreData = dict()
    for searchType in searchTypes:
      hits = search(indexPrefix, indexesFolder, searchType, query, -1)
      for hit in hits:
        if not f"{id}.{hit.docid}" in scoreData:
          scoreData[f"{id}.{hit.docid}"] = dict()
        scoreData[f"{id}.{hit.docid}"][searchType] = hit.score
  
      predictData = dict()
      for doc in scoreData:
        if "bm25" in scoreData[doc] and "laplace" in scoreData[doc] and "jm" in scoreData[doc]:
          predictData[doc] = cls.predict_proba([[scoreData[doc]["bm25"], scoreData[doc]["laplace"], scoreData[doc]["jm"]]])
  
    results[id] = sorted(predictData.items(), key=lambda x:x[1][0][1], reverse=True)
    
  with open(os.path.join("data/results/raw", f"query.{testingRange}-{indexesFolder.replace('/', '-')}-LTR.txt"), "w") as f:
    for id in results:
      for i, item in enumerate([r for i, r in enumerate(results[id]) if i < 1000]):
        queryId = item[0].split(".")[0]
        id = item[0].split(".")[1]
        f.write(f"{queryId} Q0 {id} {i + 1} {item[1][0][1]:.5f} LTR\n")

  if not os.path.exists("data/results/json"):
    os.mkdir("data/results/json")
  res = subprocess.run(['perl', 'trec_eval.pl', f"data/qrels/qrels.{testingRange}.txt", os.path.join("data/results/raw", f"query.{testingRange}-{indexesFolder.replace('/', '-')}-LTR.txt")], capture_output=True)
  with open(os.path.join("data/results/json", f"query.{testingRange}-{indexesFolder.replace('/', '-')}-LTR.json"), "w") as f:
    f.write(res.stdout.decode())
          
  return json.loads(res.stdout.decode())


if __name__ == "__main__":
  jsonResults = dict()
  for indexType in ["raw", "trec"]:
    for stemming in ["noStemming", "porterStemming"]:
      for searchType in ["bm25", "laplace", "jm"]:
        result = generateSearchResult("data/indexes/", f"{indexType}/{stemming}", searchType)
        jsonResults[f"{indexType}-{stemming}-{searchType}"] = result["json"]

  for indexType in ["raw", "trec"]:
    for stemming in ["noStemming", "porterStemming"]:
      results = dict()
      for searchType in ["bm25", "laplace", "jm"]:
        result = generateSearchResult("data/indexes/", f"{indexType}/{stemming}", searchType, queriesRange="441-450")
        jsonResults[f"{indexType}-{stemming}-{searchType}-441-450"] = result["json"]
        results[searchType] = result["result"]
      result = learningToRank("data/indexes/", f"{indexType}/{stemming}", results)
      jsonResults[f"{indexType}-{stemming}-LTR-441-450"] = result

  with open(os.path.join("data/results/json", "query.json"), "w") as f:
    f.write(json.dumps(jsonResults))