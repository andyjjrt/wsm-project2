import os, re, json
from tqdm import tqdm

def convertTrecToJsonl(collectionFolder="collection"):
  if not os.path.exists(collectionFolder):
    os.mkdir(collectionFolder)
  with open(os.path.join(collectionFolder, "collections.jsonl"), 'w', encoding='utf-8') as jsonl_file:
    for root, dirs, files in tqdm(os.walk('WT2G'), desc='Processing files', unit='files'):
      for file_name in files:
        file_path = os.path.join(root, file_name)
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
          content = file.read()
          
          doc_infos = re.findall(r'<DOC>(.*?)</DOC>', content, re.DOTALL)
          for index, doc_info in enumerate(doc_infos, start=1):

            docno_match = re.search(r'<DOCNO>(.*?)</DOCNO>', doc_info, re.DOTALL)
            dochdr_match = re.search(r'<DOCHDR>(.*?)</DOCHDR>', doc_info, re.DOTALL)
            if docno_match:
              docno = docno_match.group(1).strip()

              doc_dict = {
                "id": docno,
                "contents": str(doc_info).replace("\n", " ")
              }
              
              json.dump(doc_dict, jsonl_file, ensure_ascii=False)
              jsonl_file.write('\n')

if __name__ == "__main__":
  convertTrecToJsonl()