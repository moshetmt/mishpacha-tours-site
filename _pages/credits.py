# -*- coding: utf-8 -*-
"""Page credits generee depuis CREDITS.md (tables Markdown)."""
import re, html
rows = []
for line in open("CREDITS.md", encoding="utf-8"):
    if line.startswith("| img/"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 5: rows.append(c)
lis = "".join(f'<li><b>{html.escape(t.replace("File:",""))}</b><span>{html.escape(f.replace("img/",""))} · {html.escape(a)} · {html.escape(l)}</span><span class="liens"><a class="go" href="{html.escape(u)}" target="_blank" rel="noopener">Source</a></span></li>' for f, t, l, a, u in rows)
PAGE = dict(
  slug="credits",
  title="Photo credits, Mishpacha Tours",
  desc="Source, author and licence for every photograph used on mishpachatours.com. Wikimedia Commons images under CC0, CC BY and CC BY-SA, cropped and resized.",
  h1="Photo credits", ital="every image, its author and its licence",
  intro="The photographs on this site come from Wikimedia Commons, under Creative Commons licences that allow commercial use with attribution. Each one was cropped and resized. The illustrations are our own. Flags are Twemoji, CC BY 4.0.",
  chips=[f"{len(rows)} photographs", "CC0, CC BY, CC BY-SA", "Illustrations: Mishpacha Tours"],
  illus="line-doorway.png", crumb=None, ticket=False,
  sections=[f'<div class="ss beige"><div class="wrap"><section class="groupe"><h2>Photographs <small>{len(rows)}</small></h2><ul class="liste-lieux">{lis}</ul></section><p class="source">Licences read on Wikimedia Commons at the time of download (August and October 2026). CC BY-SA images are used without modification of the licence; if you reuse them, keep the attribution.</p></div></div>'],
  related=[("../privacy/", "Privacy"), ("../terms/", "Terms of booking")],
  VERIF=[],
)
