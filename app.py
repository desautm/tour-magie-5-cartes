import streamlit as st
from pathlib import Path

# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Le tour des cinq cartes",
    page_icon="🃏",
    layout="wide",
)

DOSSIER_CARTES = Path(__file__).resolve().parent / "cartes_png"

VALEURS = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "V": 11, "D": 12, "R": 13,
}

NOMS_VALEURS = {1: "As", 11: "Valet", 12: "Dame", 13: "Roi"}
NOMS_COULEURS = {
    "C": "Cœur",
    "K": "Carreau",
    "T": "Trèfle",
    "P": "Pique",
}
ORDRE_COULEURS = {"T": 0, "K": 1, "C": 2, "P": 3}

VALEURS_CODES = list(VALEURS.keys())
COULEURS_CODES = ["T", "K", "C", "P"]


# --------------------------------------------------
# Algorithme du tour de magie
# --------------------------------------------------

def carte(code):
    code = code.strip().upper()

    if len(code) == 2:
        v, c = code[0], code[1]
    elif len(code) == 3 and code[:2] == "10":
        v, c = "10", code[2]
    else:
        raise ValueError(f"Code de carte invalide : {code}")

    if v not in VALEURS or c not in NOMS_COULEURS:
        raise ValueError(f"Code de carte invalide : {code}")

    return {"code": code, "valeur": VALEURS[v], "couleur": c}


def cle(c):
    return c["valeur"], ORDRE_COULEURS[c["couleur"]]


def nom_carte(c):
    valeur = c["valeur"]
    nom_valeur = NOMS_VALEURS.get(valeur, str(valeur))
    return f"{nom_valeur} de {NOMS_COULEURS[c['couleur']]}"


def quatre_cartes(cartes):
    couleurs = set()

    for c in cartes:
        if c["couleur"] in couleurs:
            cachee = c
            break
        couleurs.add(c["couleur"])
    else:
        raise ValueError("Il faut au moins deux cartes de la même couleur.")

    premiere = next(
        c for c in cartes
        if c["couleur"] == cachee["couleur"] and c != cachee
    )

    deplacement = (cachee["valeur"] - premiere["valeur"]) % 13

    if deplacement > 6:
        deplacement = 13 - deplacement
        cachee, premiere = premiere, cachee

    codes_permutations = {
        1: (0, 1, 2),
        2: (0, 2, 1),
        3: (1, 0, 2),
        4: (1, 2, 0),
        5: (2, 0, 1),
        6: (2, 1, 0),
    }

    trois_cartes = [
        c for c in cartes
        if c != cachee and c != premiere
    ]
    triees = sorted(trois_cartes, key=cle)

    ordre = codes_permutations[deplacement]
    trois_ordonnees = [triees[i] for i in ordre]

    return cachee, [premiere] + trois_ordonnees


# --------------------------------------------------
# État de l'application
# --------------------------------------------------

def initialiser_etat():
    valeurs_defaut = {
        "selection": [],
        "quatre_cartes": None,
        "carte_cachee": None,
        "etape": 0,
    }
    for cle_etat, valeur in valeurs_defaut.items():
        if cle_etat not in st.session_state:
            st.session_state[cle_etat] = valeur


def recommencer():
    st.session_state.selection = []
    st.session_state.quatre_cartes = None
    st.session_state.carte_cachee = None
    st.session_state.etape = 0


initialiser_etat()


# --------------------------------------------------
# Style
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.35rem;
        font-weight: 750;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #777;
        margin-top: 0.25rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stImage"] img {
        object-fit: contain;
    }
    .card-caption {
        text-align: center;
        font-size: 0.85rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🃏 Le tour des cinq cartes</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Choisissez cinq cartes. Je devinerai celle que vous garderez secrète.</div>',
    unsafe_allow_html=True,
)

# Mode présentation : masque les détails techniques et garde l'interface épurée.
mode_presentation = st.toggle("Mode présentation", value=True)


# --------------------------------------------------
# Sélection des cartes
# --------------------------------------------------

if st.session_state.quatre_cartes is None:
    st.subheader("1. Choisissez cinq cartes")

    st.write(
        f"Cartes sélectionnées : **{len(st.session_state.selection)} / 5**"
    )

    # Les cartes sont présentées par couleur, dans l'ordre A, 2, ..., R.
    for couleur in COULEURS_CODES:
        st.markdown(f"**{NOMS_COULEURS[couleur]}**")
        colonnes = st.columns(13)

        for i, valeur in enumerate(VALEURS_CODES):
            code = valeur + couleur
            chemin = DOSSIER_CARTES / f"{code}.png"

            with colonnes[i]:
                if chemin.exists():
                    st.image(str(chemin), use_container_width=True)
                else:
                    st.caption("Image absente")

                selectionnee = code in st.session_state.selection
                etiquette = "✓" if selectionnee else valeur

                if st.button(
                    etiquette,
                    key=f"choisir_{code}",
                    disabled=(
                        not selectionnee
                        and len(st.session_state.selection) >= 5
                    ),
                    use_container_width=True,
                    type="primary" if selectionnee else "secondary",
                ):
                    if selectionnee:
                        st.session_state.selection.remove(code)
                    else:
                        st.session_state.selection.append(code)
                    st.rerun()

    st.divider()

    if st.session_state.selection:
        st.markdown("**Votre sélection**")
        colonnes = st.columns(5)
        for i, code in enumerate(st.session_state.selection):
            chemin = DOSSIER_CARTES / f"{code}.png"
            with colonnes[i]:
                if chemin.exists():
                    st.image(str(chemin), use_container_width=True)
                st.caption(code)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Effacer la sélection",
            use_container_width=True,
            disabled=not st.session_state.selection,
        ):
            st.session_state.selection = []
            st.rerun()

    with col2:
        lancer = st.button(
            "Préparer le tour de magie",
            type="primary",
            use_container_width=True,
            disabled=len(st.session_state.selection) != 5,
        )

    if lancer:
        try:
            cartes = [carte(code) for code in st.session_state.selection]
            cachee, quatre = quatre_cartes(cartes)

            # Vérifier que les images nécessaires sont disponibles.
            fichiers = [DOSSIER_CARTES / f"{c['code']}.png" for c in quatre]
            fichiers.append(DOSSIER_CARTES / f"{cachee['code']}.png")
            manquants = [f.name for f in fichiers if not f.exists()]

            if manquants:
                st.error(
                    "Il manque des images dans le dossier cartes_png : "
                    + ", ".join(manquants)
                )
            else:
                st.session_state.carte_cachee = cachee
                st.session_state.quatre_cartes = quatre
                st.session_state.etape = 0
                st.rerun()

        except ValueError as erreur:
            st.error(str(erreur))


# --------------------------------------------------
# Présentation progressive
# --------------------------------------------------

else:
    st.subheader("2. Présentez les quatre cartes")

    quatre = st.session_state.quatre_cartes
    etape = st.session_state.etape

    st.progress(etape / 4, text=f"{etape} carte(s) révélée(s) sur 4")

    colonnes = st.columns(4)

    for i, (colonne, c) in enumerate(zip(colonnes, quatre)):
        with colonne:
            if i < etape:
                chemin = DOSSIER_CARTES / f"{c['code']}.png"
                st.image(str(chemin), use_container_width=True)
                if not mode_presentation:
                    st.caption(nom_carte(c))
            else:
                st.markdown(
                    """
                    <div style="
                        height: 190px;
                        border: 2px dashed #999;
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: #888;
                        font-size: 2rem;
                    ">?</div>
                    """,
                    unsafe_allow_html=True,
                )

    st.write("")

    if etape < 4:
        if st.button(
            "Révéler la prochaine carte",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.etape += 1
            st.rerun()

    else:
        st.success("Les quatre cartes ont été révélées.")

        if not st.session_state.get("revelee", False):
            if st.button(
                "🔮 Révéler la carte devinée",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.revelee = True
                st.rerun()

        if st.session_state.get("revelee", False):
            cachee = st.session_state.carte_cachee
            chemin = DOSSIER_CARTES / f"{cachee['code']}.png"

            st.balloons()
            st.markdown(
                f"<h2 style='text-align:center'>La carte était : {nom_carte(cachee)} !</h2>",
                unsafe_allow_html=True,
            )
            col_gauche, col_centre, col_droite = st.columns([1, 2, 1])
            with col_centre:
                st.image(str(chemin), use_container_width=True)

    st.divider()

    if st.button("↻ Recommencer un nouveau tour", use_container_width=True):
        recommencer()
        if "revelee" in st.session_state:
            del st.session_state["revelee"]
        st.rerun()
