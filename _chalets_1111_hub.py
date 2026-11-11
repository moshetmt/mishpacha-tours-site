# -*- coding: utf-8 -*-
"""4e passage (11/11/2026) : page des chalets (kosher-chalets/, 4 langues). Met à jour, par remplacement ciblé de chaînes exactes,
le sous-titre du héros, la méta description (og, JSON-LD), l'introduction, la FAQ « Quel chalet choisir ? » (HTML et JSON-LD) et la FAQ
cacherout (formule du certificat Beth Habad de Grenoble-Alpes, comme sur les fiches). Idempotent : une chaîne déjà remplacée est ignorée.
Ne lance PAS _build_hub.py. Lancer depuis site-v5 : python _chalets_1111_hub.py"""
import pathlib
import re

ICI = pathlib.Path(__file__).resolve().parent
BH = "בית חב״ד גרנובל-אלפים"   # graphie des fiches (gershayim)

R = {
 "": [  # EN
  ("in Les Deux Alpes, Courchevel, Megève, Val Thorens and Les Ménuires", "in Les Deux Alpes, Courchevel, Megève, Saint-Gervais Mont-Blanc, Les Houches, Val Thorens and Les Ménuires"),
  ("Our kosher chalets in the Alps, in Les Deux Alpes, Courchevel, Megève and Val Thorens: a private chef, Shabbat and a minyan in the chalet. One request, one written quote.",
   "Kosher chalets in the Alps: Les Deux Alpes, Courchevel, Val Thorens, Saint-Gervais Mont-Blanc, Les Houches. Private chef, Shabbat, minyan, one quote."),
  ("Les Deux Alpes, Courchevel and near Megève.</p></div>", "Les Deux Alpes, Courchevel, near Megève, Saint-Gervais Mont-Blanc and Les Houches.</p></div>"),
  ("with a ski path at the door, also in the 3 Valleys.", "with a ski path at the door, also in the 3 Valleys. Chalet Neige Éternelle in Les Deux Alpes, Chalet Crystal in Saint-Gervais Mont-Blanc and Chalet Althéa in Les Houches, in the Chamonix Valley, each have a heated indoor pool."),
  ("The supervision details come in writing with your quote.", "The kitchen is certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
 ],
 "fr/": [
  ("<i>Deux Alpes, Courchevel, Megève, Val Thorens, Ménuires</i>", "<i>Deux Alpes, Courchevel, Megève, Saint-Gervais Mont-Blanc, Les Houches, Val Thorens, Ménuires</i>"),
  ("Des chalets strictement casher dans les Alpes, aux Deux Alpes, à Courchevel, près de Megève et à Val Thorens : chef privé, Chabbat et minyan au chalet. Une demande, un devis écrit.",
   "Chalets casher dans les Alpes : Deux Alpes, Courchevel, Val Thorens, Saint-Gervais Mont-Blanc, Les Houches. Chef privé, Chabbat, minyan, un devis."),
  ("aux Deux Alpes, à Courchevel et près de Megève.</p></div>", "aux Deux Alpes, à Courchevel, près de Megève, à Saint-Gervais Mont-Blanc et aux Houches.</p></div>"),
  ("avec un chemin skieur à la porte, dans Les 3 Vallées aussi.", "avec un chemin skieur à la porte, dans Les 3 Vallées aussi. Le Chalet Neige Éternelle aux Deux Alpes, le Chalet Crystal à Saint-Gervais Mont-Blanc et le Chalet Althéa aux Houches, dans la vallée de Chamonix, ont chacun une piscine intérieure chauffée."),
  ("Les détails de la surveillance figurent par écrit dans votre devis.", "La cuisine est certifiée cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany."),
 ],
 "es/": [
  ("<i>Les Deux Alpes, Courchevel, Megève</i>", "<i>Les Deux Alpes, Courchevel, Megève, Saint-Gervais Mont-Blanc, Les Houches</i>"),
  ("Nuestros chalés kosher en los Alpes, en Les Deux Alpes, Courchevel, cerca de Megève y en Val Thorens: chef privado, Shabat y minyan en el chalé. Una solicitud, un presupuesto por escrito.",
   "Chalés kosher en los Alpes: Les Deux Alpes, Courchevel, Val Thorens, Saint-Gervais Mont-Blanc, Les Houches. Chef privado, Shabat, minyán, un presupuesto."),
  ("Les Deux Alpes, Courchevel, cerca de Megève y Val Thorens.</p></div>", "Les Deux Alpes, Courchevel, cerca de Megève, Saint-Gervais Mont-Blanc, Les Houches y Val Thorens.</p></div>"),
  ("con una pista de esquí en la puerta, también en Les 3 Vallées.", "con una pista de esquí en la puerta, también en Les 3 Vallées. El Chalet Neige Éternelle en Les Deux Alpes, el Chalet Crystal en Saint-Gervais Mont-Blanc y el Chalet Althéa en Les Houches, en el valle de Chamonix, tienen cada uno una piscina interior climatizada."),
  ("Los detalles de la supervisión se entregan por escrito con el presupuesto.", "La cocina está certificada kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany."),
 ],
 "he/": [
  ("<i>בלה דז אלפ, בקורשבל, ליד מג'ב, בוואל טורנס ובלה מנואר</i>", "<i>בלה דז אלפ, בקורשבל, ליד מג'ב, בסן ז'רווה מון בלאן, בלה אוש, בוואל טורנס ובלה מנואר</i>"),
  ("צ'אלות כשרות באלפים, בלה דז אלפ, בקורשבל, ליד מג'ב ובואל טורנס: שף פרטי, שבת ומניין בצ'אלה. בקשה אחת, הצעת מחיר אחת בכתב.",
   "צ'אלות כשרות באלפים: בלה דז אלפ, בקורשבל, בסן ז'רווה מון בלאן, בלה אוש ובואל טורנס. שף פרטי, שבת ומניין, הצעת מחיר בכתב."),
  ("בלה דז אלפ, בקורשבל, ליד מג'ב ובואל טורנס, עם שביל סקי ליד הדלת.</p></div>", "בלה דז אלפ, בקורשבל, ליד מג'ב, בסן ז'רווה מון בלאן, בלה אוש ובואל טורנס, עם שביל סקי ליד הדלת.</p></div>"),
  ("עם שביל סקי ליד הדלת, גם כן בשלושת העמקים.", "עם שביל סקי ליד הדלת, גם כן בשלושת העמקים. בריכה מקורה מחוממת יש בצ'אלה נז' אטרנל בלה דז אלפ, בצ'אלה קריסטל בסן ז'רווה מון בלאן ובצ'אלה אלתיאה בלה אוש, בעמק שמוני."),
  ("פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר.", "המטבח בהשגחת " + BH + "."),
 ],
}


def main():
    total = 0
    for pre, paires in R.items():
        for f in ("index.html", "index.md"):
            p = ICI / (pre + "kosher-chalets") / f
            s = p.read_text(encoding="utf-8"); o = s
            for old, new in paires:
                if new in s:
                    continue
                if old in s:
                    s = s.replace(old, new)
                elif f == "index.html":
                    raise SystemExit(f"introuvable : {p.relative_to(ICI)} :: {old[:60]}")
            if s != o:
                p.write_bytes(s.encode("utf-8")); total += 1
                print("maj", p.relative_to(ICI))
    return total


if __name__ == "__main__":
    main()
