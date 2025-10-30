
import json,os
REG_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),"..","metadata","schema_registry.json")

def load_registry():
    if os.path.exists(REG_PATH):
        return json.load(open(REG_PATH))
    return {}

def save_registry(d):
    os.makedirs(os.path.dirname(REG_PATH), exist_ok=True)
    with open(REG_PATH, "w") as f:
        json.dump(d, f, indent=2)


def bump(v):
    a,b,c=(v or "0.0.0").split(".");return f"{a}.{b}.{int(c)+1}"

def upsert_schema(name,schema):
    reg=load_registry();entry=reg.get(name,{"version":"0.0.0"})
    newv=bump(entry["version"]) if entry.get("schema")!=schema else entry["version"]
    reg[name]={"schema":schema,"version":newv}
    save_registry(reg);return newv
