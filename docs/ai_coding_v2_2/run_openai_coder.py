import json, os, sys, time, requests, hashlib
MODEL="gpt-5.5-2026-04-23"
for name in ["DEEPSEEK_PROMPT_1_validation_4.md","DEEPSEEK_PROMPT_2_pilot_AB_24.md"]:
    prompt=open(name).read()
    t=time.time()
    r=requests.post("https://api.openai.com/v1/responses",timeout=1500,
        headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"]},
        json={"model":MODEL,"input":prompt,"reasoning":{"effort":"high"}})
    d=r.json(); tag=name.split('_')[2]
    json.dump(d,open(f"openai_raw_{tag}.json","w"),indent=1)
    print(name, r.status_code, d.get("model"), d.get("usage"), round(time.time()-t), d.get("error"))
