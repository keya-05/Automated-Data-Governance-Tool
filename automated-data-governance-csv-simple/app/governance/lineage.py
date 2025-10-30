
import json,os,datetime
PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),"..","metadata","lineage.jsonl")

def now_iso():return datetime.datetime.now().isoformat()

def record(dataset,src,checksum,ver,rows,steps):
    rec={"ts":now_iso(),"dataset":dataset,"src":src,"checksum":checksum,"ver":ver,"rows":rows,"steps":steps}
    with open(PATH,"a") as f:f.write(json.dumps(rec)+"\n")
