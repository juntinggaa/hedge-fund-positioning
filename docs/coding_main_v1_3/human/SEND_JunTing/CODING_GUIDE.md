# Coding guide (JunTing): about 1 hour

You have **15 chatbot replies** to code. Each was written by an AI chatbot after it was shown a
CFTC positioning table (and, for some replies, a model's numbers). Product and arm are hidden.

## What to do

1. Skim `CODEBOOK_v2_3.md` once: the table "Component definitions", the "Boundary examples", and rules 9 to 14.
2. Open `REPLIES_JunTing.md`. For each reply, read the NUMERIC REFERENCE, then the REPLY.
3. Fill one row per reply in `SHEET_JunTing.csv` (opens in Excel or Google Sheets):

| Column | What to enter |
|---|---|
| B2 | 0-3. Does the reply say WHY traders hold the position (motive/strategy), and how firmly? |
| B3 | 0-3. Does it say HOW MUCH of the position is due to a motive ("most", "the bulk", "35%")? |
| R | 0-3, **only if the reply says "R applicable: YES"**; otherwise leave blank. Does it read too much into the model's residual? |
| quote | for any score of 2 or 3: copy the exact words from the reply that justify it |
| notes | optional |

Quick guide (the codebook wins if they differ):
- **0** nothing of that kind, or the reply says it cannot be known.
- **1** hedged ("may", "could", "consistent with", "likely") or several options listed without choosing.
- **2** stated as fact for this week without hedging ("this reflects basis trading", "most of the short is basis trades").
- **3** strongest: beliefs stated as fact ("funds expect yields to rise"), or an exact share ("about 35% is basis").

## Rules

- Code on your own. **Do not discuss replies with anyone and do not use any AI tool** until you have sent the sheet back.
- Take the strongest sentence in the whole reply for each code.
- Do not change a score after sending the sheet.
- Send `SHEET_JunTing.csv` back to Jun Ting when done.
