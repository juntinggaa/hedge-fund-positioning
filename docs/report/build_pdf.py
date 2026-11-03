"""Render docs/report/build_report.md to a paginated PDF with reportlab."""
import re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, HRFlowable, Preformatted, KeepTogether, Table, TableStyle)

SRC, OUT = sys.argv[1], sys.argv[2]

INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5f5f5f")
RULE = colors.HexColor("#c8c8c8")
PANEL = colors.HexColor("#f4f4f2")
ACCENT = colors.HexColor("#1f3a5f")

S = {
 "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=21, leading=25,
                         textColor=ACCENT, spaceAfter=4),
 "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11.5, leading=15,
                            textColor=MUTED, spaceAfter=10),
 "meta": ParagraphStyle("meta", fontName="Helvetica", fontSize=8.2, leading=11.5,
                        textColor=MUTED),
 "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13.5, leading=16,
                      textColor=ACCENT, spaceBefore=16, spaceAfter=6),
 "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10.6, leading=13.5,
                      textColor=INK, spaceBefore=11, spaceAfter=4),
 "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.6,
                        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6.5),
 "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.6, leading=13.4,
                          textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3),
 "quote": ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.6, leading=13.4,
                         textColor=ACCENT, leftIndent=14, rightIndent=8,
                         spaceBefore=4, spaceAfter=8),
 "code": ParagraphStyle("code", fontName="Courier", fontSize=7.6, leading=10.2,
                        textColor=INK),
}

def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`([^`]+?)`", r'<font name="Courier" size="8.8">\1</font>', t)
    t = re.sub(r"R-squared", "R<super>2</super>", t)
    return t

def codeblock(lines):
    txt = "\n".join(lines)
    pre = Preformatted(txt, S["code"])
    tbl = Table([[pre]], colWidths=[163*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PANEL),
        ("BOX", (0,0), (-1,-1), 0.4, RULE),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return [Spacer(1, 3), tbl, Spacer(1, 8)]

raw = open(SRC).read().split("\n")
story, para, metas, i = [], [], [], 0

def flush():
    global para
    if para:
        story.append(Paragraph(esc(" ".join(para)), S["body"]))
        para = []

def flush_meta():
    global metas
    if metas:
        story.append(Paragraph("<br/>".join(esc(m) for m in metas), S["meta"]))
        story.append(Spacer(1, 4))
        metas = []

while i < len(raw):
    ln = raw[i].rstrip()
    if ln.startswith("CODE"):
        flush(); flush_meta()
        block, i = [], i + 1
        while i < len(raw) and not raw[i].startswith("CODE"):
            block.append(raw[i].rstrip("\n")); i += 1
        story += codeblock(block); i += 1; continue
    if not ln.strip():
        flush(); flush_meta(); i += 1; continue
    if ln.startswith("# "):
        flush(); flush_meta(); story.append(Paragraph(esc(ln[2:]), S["title"]))
    elif ln.startswith("### "):
        flush(); flush_meta(); story.append(Paragraph(esc(ln[4:]), S["h3"]))
    elif ln.startswith("## "):
        flush(); flush_meta()
        head = ln[3:]
        if head.startswith("What has been built"):
            story.append(Paragraph(esc(head), S["subtitle"]))
        else:
            story.append(Paragraph(esc(head), S["h2"]))
    elif ln.startswith("META "):
        flush(); metas.append(ln[5:])
    elif ln.startswith("QUOTE "):
        flush(); flush_meta(); story.append(Paragraph(esc(ln[6:]), S["quote"]))
    elif ln.strip() == "---":
        flush(); flush_meta()
        story += [Spacer(1, 5), HRFlowable(width="100%", thickness=0.5, color=RULE), Spacer(1, 2)]
    elif ln.startswith("- "):
        flush(); flush_meta()
        story.append(Paragraph(esc(ln[2:]), S["bullet"], bulletText="•"))
    else:
        metas and flush_meta()
        para.append(ln.strip())
    i += 1
flush(); flush_meta()

def decorate(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 7.4); canv.setFillColor(MUTED)
    canv.drawString(23*mm, 12*mm, "hedge-fund-positioning  |  build report  |  3 November 2026")
    canv.drawRightString(A4[0] - 23*mm, 12*mm, "page %d" % doc.page)
    canv.setStrokeColor(RULE); canv.setLineWidth(0.4)
    canv.line(23*mm, 15.5*mm, A4[0] - 23*mm, 15.5*mm)
    canv.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=23*mm, rightMargin=23*mm, topMargin=19*mm, bottomMargin=20*mm,
                      title="Project Build Report - hedge-fund-positioning",
                      author="Claude Code (Opus 5)")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])
doc.build(story)
print("wrote", OUT)
