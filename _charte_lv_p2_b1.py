"""Phase 2 lot B1 (03/11) : lance les 6 scripts dans l'ordre. Relancer = aucun changement."""
import importlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
for nom in ("_charte_lv_p2_stations", "_charte_lv_p2_entete", "_charte_lv_p2_chalets_he", "_charte_lv_p2_404",
            "_charte_lv_p2_form_accueils", "_charte_lv_p2_og_espace"):
    importlib.import_module(nom).main()
