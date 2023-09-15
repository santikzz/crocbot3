import httpx
import json

def pb_check():
    url = "https://tpb.re/api.php?url=/q.php?q=Oppenheimer"
    data = httpx.get(url).text
    data = json.loads(data)
    f = open("pb_lastID.txt", "r")
    lastId = f.read()
    f.close()
    id = data[0]["id"]
    name = data[0]["name"]
    if (id != lastId):
        with open("pb_lastID.txt", "w") as f:
            f.write(id)
        return {"id":id, "name":name}
    else:
        return False
    