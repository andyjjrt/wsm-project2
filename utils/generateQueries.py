def generateQueries(queryPath: str) -> list[tuple[str, str]]:
  with open(queryPath, "r") as f:
    lines = f.readlines()
    topDepth = 0
    number = ""
    title = ""
    query = []
    for line in lines:
      if line.startswith("<top>"):
        topDepth += 1
      elif line.startswith("</top>"):
        topDepth -= 1
        query.append((number, f"{title}"))
        
      if topDepth == 1:
        if line.startswith("<num>"):
          number = line.replace("<num>", "").replace("Number: ", "").strip()
        if line.startswith("<title>"):
          title = line.replace("<title>", "").strip().lower()
    return query