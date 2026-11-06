import json, os, time, requests, sys
MODEL="gpt-5.5-2026-04-23"
for name,tag in [(a,a.split('_')[3]) for a in sys.argv[1:]]:
    prompt=open(name).read(); t=time.time()
    r=requests.post("https://api.openai.com/v1/responses",timeout=1500,headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"]},json={"model":MODEL,"input":prompt,"reasoning":{"effort":"high"}})
    d=r.json(); json.dump(d,open(f"openai_v2_3_raw_{tag}.json","w"),indent=1)
    print(name,tag,r.status_code,d.get("model"),round(time.time()-t),d.get("error"))
