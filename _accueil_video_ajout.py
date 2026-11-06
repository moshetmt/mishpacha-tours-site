# -*- coding: utf-8 -*-
"""Ajoute deux plans (skieur sous ciel bleu, poulet rôti sur plateau tournant) à la vidéo d'accueil, sans retirer aucun plan
existant (Moshé 05/11/2026 : « tout est bien, ajoute juste »). Les plans existants sont recoupés dans leurs parties stables
(les fondus d'origine sont remplacés par les nouveaux) puis les deux plans sont insérés : skieur entre village et chalet,
repas entre feu de bois et motoneiges. Sources Pexels 854877 (skieur) et 6162075 (repas), originaux hors git dans
00-brief/2026-11-05-videos-pexels-ajout/ et 00-brief/2026-10-27-videos-pexels/.
    python _accueil_video_ajout.py <ancien_dossier_video> <sortie> [--apercu]      (ancien = copie de l'avant, jamais écrite)"""
import subprocess, sys, os
A, OUT = sys.argv[1], sys.argv[2]; APERCU = "--apercu" in sys.argv
B = "E:/projet site/ads-os/clients/mishpacha-tours/00-brief/"
SKI = B + "2026-10-27-videos-pexels/854877-hd_1920_1080_25fps.mp4"
REPAS = B + "2026-11-05-videos-pexels-ajout/6162075-hd_1920_1080_30fps.mp4"
X = .5; D = 3.0   # fondu et durée de chaque nouveau plan
CUTS = {"pc": (4.8, 5.5, 12.6, 13.2, 18.0, 1920, 1080, "crop=1920:1080"),
        "tel": (4.8, 5.5, 12.15, 12.9, 17.6, 720, 1280, "crop=608:1080:600:0")}
CAL = {"pc": (9.0, 6.0), "tel": (9.0, 6.0)}
for fmt in ("pc", "tel"):
    t1, t2, t3, t4, fin, W, H, crop = CUTS[fmt]
    ski0, rep0 = CAL[fmt]
    rep_crop = crop if fmt == "pc" else "crop=608:1080:560:0"
    f = (f"[0:v]trim=0:{t1},setpts=PTS-STARTPTS,fps=30[a];[0:v]trim={t2}:{t3},setpts=PTS-STARTPTS,fps=30[b];[0:v]trim={t4}:{fin},setpts=PTS-STARTPTS,fps=30[c];"
         f"[1:v]trim={ski0}:{ski0+D},setpts=PTS-STARTPTS,fps=30,{crop},scale={W}:{H},setsar=1[s];"
         f"[2:v]trim={rep0}:{rep0+D},setpts=PTS-STARTPTS,fps=30,{rep_crop},scale={W}:{H},setsar=1[k];")
    L1 = t1; L2 = L1 + D - X; L3 = L2 + (t3 - t2) - X + 0  # longueurs cumulées après chaque fondu
    f += f"[a][s]xfade=transition=fade:duration={X}:offset={L1-X}[x1];"
    f += f"[x1][b]xfade=transition=fade:duration={X}:offset={L2-X+0}[x2];"
    L3 = L2 + (t3 - t2) - X
    f += f"[x2][k]xfade=transition=fade:duration={X}:offset={L3-X+0}[x3];"
    L4 = L3 + D - X
    f += f"[x3][c]xfade=transition=fade:duration={X}:offset={L4-X}[x4]"
    if APERCU:
        f += f";[x4]scale=-2:360[v]"; enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"]
        dst = OUT.replace(".mp4", f"-apercu-{fmt}.mp4")
    else:
        f += ";[x4]null[v]"; enc = ["-c:v", "libx264", "-preset", "slow", "-crf", sys.argv[sys.argv.index("--crf")+1] if "--crf" in sys.argv else "23", "-threads", "0", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
        dst = os.path.join(OUT, f"accueil-{fmt}.mp4")
    base = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(A, f"accueil-{fmt}.mp4"), "-i", SKI, "-i", REPAS, "-filter_complex", f, "-map", "[v]", "-an"]
    if APERCU: r = subprocess.run(base + enc + [dst])
    else:   # deux passes au débit visé (--vb pc,tel en kbit/s) : poids sous 4,5 Mo ordinateur et 3,5 Mo téléphone
        vb = sys.argv[sys.argv.index("--vb") + 1].split(",")[0 if fmt == "pc" else 1]
        e2 = [x for x in enc if x not in ("-crf", sys.argv[sys.argv.index("--crf")+1] if "--crf" in sys.argv else "23")]
        e2 = e2 + ["-b:v", vb + "k"]
        subprocess.run(base + e2 + ["-pass", "1", "-passlogfile", "E:/taches/wtv/pl" + fmt, "-f", "mp4", os.devnull])
        r = subprocess.run(base + e2 + ["-pass", "2", "-passlogfile", "E:/taches/wtv/pl" + fmt, dst])
    print(fmt, "ok" if r.returncode == 0 else "ERREUR", dst)
