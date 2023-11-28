from pyserini.search.lucene import LuceneSearcher
from pyserini.index import IndexReader
from jnius import JavaClass, MetaJavaClass, JavaMultipleMethod, JavaField, JavaMethod, java_method
from pyserini.pyclass import autoclass

JIndexSearcher = autoclass("org.apache.lucene.search.IndexSearcher")
JLMJelinekMercerSimilarity = autoclass("org.apache.lucene.search.similarities.LMJelinekMercerSimilarity")

class SimpleSearcher(JavaClass, metaclass=MetaJavaClass):
  __javaclass__ = "io/anserini/search/SimpleSearcher"
  __javaconstructor__ = (
    ('(Ljava/lang/String;Lorg/apache/lucene/analysis/Analyzer;)V', False),
    ('(Ljava/lang/String;)V', False)
  )
  
  reader = JavaField("Lorg/apache/lucene/index/IndexReader;")
  
  set_bm25 = JavaMethod("(FF)V")
  set_qld = JavaMethod("(F)V")
  get_similarity = JavaMethod("()Lorg/apache/lucene/search/similarities/Similarity;")
  search = JavaMultipleMethod([
    ("(Ljava/lang/String;)[Lio/anserini/search/SimpleSearcher$Result;", False, False),
    ("(Ljava/lang/String;I)[Lio/anserini/search/SimpleSearcher$Result;", False, False),
    ("(Lorg/apache/lucene/search/Query;I)[Lio/anserini/search/SimpleSearcher$Result;", False, False),
    ("(Lio/anserini/search/query/QueryGenerator;Ljava/lang/String;I)[Lio/anserini/search/SimpleSearcher$Result;", False, False)
  ])
  
  @java_method('(F)V')
  def set_jm(self, _lambda: float):
    self.similarity = JLMJelinekMercerSimilarity(_lambda)
    self.searcher = JIndexSearcher(self.reader)
    self.searcher.setSimilarity(self.similarity)

class Searcher(LuceneSearcher):
  def __init__(self, index_dir: str, prebuilt_index_name=None):
    super().__init__(index_dir, prebuilt_index_name)
    self.object = SimpleSearcher(index_dir)
    self.indexReader = IndexReader(index_dir)
    self.stats = self.indexReader.stats()
  
  def set_qld(self):
    """Configure query likelihood with Dirichlet smoothing as the scoring function.

    Parameters
    ----------
    mu : float
        Dirichlet smoothing parameter mu.
    """
    self.object.set_qld(float(self.stats["total_terms"] / self.stats["unique_terms"]))
    
  def set_jm(self, _lambda):
    self.object.set_jm(float(_lambda))