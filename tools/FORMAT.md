# Format d'une édition de L'Actualité

Site : https://bpasquetupegui.github.io/L-actualite/
Lien vers un article : `https://bpasquetupegui.github.io/L-actualite/#a-<id>`
Lien vers une édition : `https://bpasquetupegui.github.io/L-actualite/#e-<AAAA-MM-JJ>`

Pour publier, écrire un fichier JSON `{"edition": {...}, "articles": {...}}`, puis lancer `python3 tools/add_edition.py fichier.json`, commit et push sur `main`. Le script refuse une édition incomplète et ne supprime jamais les éditions précédentes. Voir `tools/exemple.json` (édition du 4 novembre 2026) pour un exemple réel complet.

## edition
- `date` : "AAAA-MM-JJ" (date de Paris).
- `une` : id de l'article principal. `tldr` : les ids des 3 news du TL;DR, la une comprise.
- `chiffres` : `[{"a": "CAC 40", "n": "8 020,31", "v": "-0,34 %", "s": "down"}]`, avec `s` ∈ up/down/flat. Liste vide le week-end.
- `chiffres_note` : une phrase (ex. « Clôtures du mardi 3 novembre »).
- `agenda` : `[{"j": "Jeu. 5 nov.", "t": "…"}]`.
- `items` : une entrée par news :
  - `id` : `<date>-<slug>`, en minuscules ASCII et tirets (ex. `2026-11-04-tanzanie-lissu`).
  - `t` : titre de journal (court, factuel, accrocheur sans exagérer). `c` : chapô (1 à 2 phrases).
  - `r` : rubrique, parmi « France », « Europe », « Amérique du Nord », « Amérique du Sud », « Afrique », « Asie & Moyen-Orient », « Deals & buy-side ».
  - `s` : section, parmi « À la une », « Politique », « Économie », « Business », « Marchés », « Devises », « Culture », « Société », « M&A », « Rumeurs & discussions », « Levées PE/VC/infra », « Asset management ».
  - `p` : codes pays ISO en minuscules (ex. `["us"]`, `["eu"]` pour l'UE). `k` : 3 à 7 mots-clés en minuscules (personnes, entreprises, thèmes). Ils servent aux liens « Sur le même sujet » entre éditions, donc garder les mêmes mots-clés d'un jour à l'autre (« midterms », « iran », « budget 2027 »…).
  - `imp` : 1 (mineur), 2 (important) ou 3 (majeur).
  - `v` (facultatif) : `{"n": "115 Md$", "l": "valeur d'entreprise"}`, chiffre clé affiché en couverture.
  - `img` (facultatif, 4 à 6 par édition pour les grands sujets) : `{"u": "<nom exact du fichier Wikimedia Commons, sans 'File:'>", "credit": "Légende. Photo : Auteur / Wikimedia Commons (licence)", "alt": "…"}`. Uniquement des lieux, bâtiments, paysages, cartes ou images satellites. Jamais de photo d'une personne. Le nom de fichier doit avoir été vu dans un résultat de recherche (WebSearch avec allowed_domains commons.wikimedia.org). Ne jamais l'inventer.

## articles["<id>"]
Chaque news a un vrai article, quelle que soit la rubrique.
- `cles` : 3 à 5 points « L'essentiel ».
- `corps` : `[{"h": "Intertitre", "p": "Paragraphes séparés par une ligne vide"}]`. Chaque article, même pour une news mineure, est un vrai article de journal qui répond au quoi, au pourquoi et au comment, avec au minimum ces 5 sections :
  1. « Ce qui s'est passé » : les faits précis (qui, quoi, quand, où, combien).
  2. « Comment on en est arrivé là » : l'historique et la genèse du sujet, avec dates clés.
  3. « Les acteurs » : qui sont les personnes, partis, entreprises ou institutions, d'où ils viennent, leurs positions et intérêts. Ne jamais supposer que le lecteur les connaît.
  4. « Pourquoi c'est important » : enjeux politiques, économiques et pour les marchés, en France et à l'international.
  5. « Et maintenant ? » : prochaines étapes, dates, scénarios possibles.
  Longueur : environ 450 mots minimum pour imp=1, 700 pour imp=2, 1 000 et plus pour imp=3. Ajouter `chrono` dès que le sujet a une histoire.
- `deal` (pour toute opération M&A, levée ou rachat) :
  - `cible` et `acquereur` : `{"nom", "activite", "origine", "chiffres"}`. `origine` couvre la fondation, le pays, l'historique et les dirigeants.
  - `termes` : `[["Prix", "…"], ["Structure", "…"], ["Multiple", "…"]]`.
  - `strategie` : texte sur la logique annoncée et ce qu'en disent analystes et presse.
  - `acteurs` : liste (dirigeants, vendeurs, fonds, conseils).
  - `etapes` : autorisations, calendrier, closing.
  - Pour une levée de fonds, mettre le gérant dans `cible`. `role_cible` et `role_acquereur` permettent de renommer les cartes (ex. « Gérant », « Investisseurs »).
- `chrono` : `[{"d": "9 avr. 2025", "t": "…"}]` pour les sujets qui ont une histoire.
- `sources` : `[{"n": "Média – titre", "u": "https://…"}]`, uniquement des sources consultées.
- `note` (facultatif) : avertissement de fiabilité si un point n'a pas pu être recoupé.

Le texte est du texte brut, sans HTML ni markdown.

## Rumeurs & discussions (section de « Deals & buy-side »)
Pour les rapprochements dont le marché a entendu parler sans annonce officielle : discussions rapportées par Bloomberg, Reuters, le FT, le WSJ ou Les Échos (« selon des sources proches du dossier »), offres non sollicitées, revues stratégiques, démentis ou « no comment ». Ces infos sont souvent la cause d'un fort mouvement de cours.
- Uniquement si la rumeur est rapportée par un média de référence. Toujours nommer le média d'origine et préciser son statut : discussions préliminaires, avancées, démenti, refus de commenter.
- `v` : la variation de cours qui a suivi (ex. `{"n": "+11 %", "l": "Lumentum à l'annonce des discussions"}`).
- L'article utilise la fiche `deal` (avec `role_cible` / `role_acquereur` = « Cible potentielle » / « Acquéreur potentiel ») et explique : ce qui a été rapporté et par qui ; la réaction des cours (le mouvement s'explique-t-il par la rumeur ?) ; qui sont les deux sociétés ; la logique possible ; les obstacles (financement, antitrust, prix) ; les prochaines échéances.
- Quand une rumeur est confirmée par une annonce, l'article M&A du jour le rappelle et reprend les mêmes mots-clés `k` pour relier les deux articles.
