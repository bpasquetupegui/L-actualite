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
  - `img` (À CHERCHER POUR CHAQUE ARTICLE, pas seulement les grands sujets) : la photo la plus pertinente possible pour CET article : le siège ou un site de l'entreprise, le bâtiment de l'institution, le lieu de l'événement, l'usine, le produit, la ville. Même sujet = photo différente d'un jour à l'autre si possible. Format : `{"u": "<nom exact du fichier Wikimedia Commons, sans 'File:'>", "credit": "Légende. Photo : Auteur / Wikimedia Commons (licence)", "alt": "…"}`. Uniquement des lieux, bâtiments, paysages, cartes ou images satellites. Jamais de photo d'une personne. Le nom de fichier doit avoir été vu dans un résultat de recherche (WebSearch avec allowed_domains commons.wikimedia.org). Ne jamais l'inventer.
  - `logos` (M&A, rumeurs de rapprochement, et toute news centrée sur 1-2 entreprises) : à la place de `img`, les logos des sociétés concernées, affichés côte à côte sur fond blanc avec « × » entre eux. Format : `[{"u": "<nom exact du fichier logo sur Wikimedia Commons>", "n": "Nom de la société"}, …]` (2 max). Cherche avec WebSearch (allowed_domains commons.wikimedia.org), par exemple « File: <société> logo svg ». Si le logo d'une des sociétés est introuvable, n'utilise PAS `logos` (jamais de nom écrit à la place d'un logo) : mets à la place un `img` avec une photo du siège de l'entreprise (idéalement où l'on voit son nom), d'une de ses boutiques, usines ou sites, en rapport avec son secteur. Ne jamais inventer un nom de fichier.
  - RÈGLE DE PERTINENCE : l'image doit avoir un rapport direct avec ce qui est écrit dans l'article. Une image générique (une plaquette de silicium pour une fusion de semi-conducteurs, une skyline quelconque) est à éviter : un logo, un siège social ou le lieu précis valent mieux.

## articles["<id>"]
Chaque news a un vrai article, quelle que soit la rubrique.
- `cles` : 3 à 5 points « L'essentiel ».
- `corps` : `[{"h": "Intertitre", "p": "Paragraphes séparés par une ligne vide"}]`. Chaque article, même pour une news mineure, est un vrai article de journal qui répond au quoi, au pourquoi et au comment. Il suit cinq étapes dans cet ordre : les faits (qui, quoi, quand, où, combien), la genèse (historique et dates clés), les acteurs (parcours, positions, intérêts), les enjeux (politiques, économiques, pour les marchés, la France et l'Europe) et la suite (prochaines étapes, dates, scénarios). Ces étapes guident la rédaction mais ne sont JAMAIS des intertitres.
  - Chapô (`c`) : 2 phrases qui donnent l'essentiel et l'angle de l'article.
  - Intertitres (`h`) : propres à chaque article, informatifs et accrocheurs, comme dans Le Monde ou Les Échos. Ils annoncent une idée ou un fait, pas une rubrique, et se comprennent sans avoir lu le reste (ex. « Le retour des négociations de paix à Abou Dhabi », pas « Abou Dhabi, troisième essai »). Interdits : « Ce qui s'est passé », « Comment on en est arrivé là », « Les acteurs », « Pourquoi c'est important », « Et maintenant ? » et toute formule générique.
  - Aucun fait non sourcé : un intertitre ou une phrase ne contient jamais un chiffre, une date ou une affirmation non établie par les sources de l'article. Pas de déduction présentée comme un fait.
  - Contexte : ne rien supposer connu. Chaque lieu, sigle, personne ou processus (ex. « les pourparlers d'Abou Dhabi ») est expliqué en une phrase à sa première mention : ce que c'est, depuis quand, qui y participe.
  - Style : ton de journaliste économique, précis et sobre. Chaque phrase apporte un fait, un chiffre, un nom, une date ou une analyse. Interdits : phrases creuses (« c'est un enjeu majeur », « l'enjeu est double », « les marchés suivent ces développements »), ton scolaire, répétitions d'une partie à l'autre, conclusions morales, « en résumé ». Les enjeux s'appuient sur des chiffres, des analystes ou des précédents, jamais sur des généralités. Notions techniques expliquées en une incise, sans condescendance.
  Longueur : environ 450 mots minimum pour imp=1, 700 pour imp=2, 1 000 et plus pour imp=3, sans remplissage : la longueur vient du contexte et de l'analyse. Ajouter `chrono` dès que le sujet a une histoire.
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

## Bibliothèque de photos (data/photos.json)
Le site attribue automatiquement une photo de la bibliothèque à chaque article qui n'a pas de champ `img`, en croisant ses mots-clés `k` et ses pays `p` avec les `tags` des photos (sans doublon sur une même édition). Pour enrichir la bibliothèque, ajoute à chaque édition 3 à 5 nouvelles photos vérifiées (nom de fichier exact vu dans un résultat de recherche Wikimedia Commons, jamais de personne) au format `{"u": "Nom exact.jpg", "credit": "Photo : Auteur / Wikimedia Commons (licence)", "tags": ["code pays", "mots-clés en minuscules"]}`. Privilégie les pays et les thèmes qui reviennent souvent et qui n'ont pas encore de photo (Israël, Inde, Corée, Australie, Nigeria, Venezuela, Pologne, Allemagne, Espagne, Italie, pharma, automobile, ports, énergies renouvelables…). Ne supprime jamais une entrée existante.

## Calendrier (data/calendar.json)
`{"events": [{"d": "AAAA-MM-JJ", "t": "Intitulé court", "c": "Banque centrale|Macro|Résultats|Politique|Élection|Sommet|Diplomatie", "p": "code pays", "imp": 1-3, "h": "heure de Paris ou vide"}]}`.
Chaque matin, le calendrier doit couvrir les 3 prochains mois (affichés sur la page Calendrier), de façon dense : vise 15 à 25 rendez-vous par mois, avec l’heure de Paris (champ h) dès qu’elle est connue, mais uniquement des événements majeurs et datés de façon fiable : décisions de taux des grandes banques centrales (Fed, BCE, BoE, BoJ, BNS, RBA, Banque du Canada, Brésil, Inde, Chine…), élections nationales et référendums des grands pays, sommets (G7, G20, UE, OTAN, APEC, COP, OPEP+), résultats des très grandes entreprises (Big Tech, Nvidia, grandes banques, CAC 40 majeures), publications macro clés (emploi et inflation américains, inflation zone euro, PIB), grands discours (Jackson Hole, état de l'Union…), échéances politiques ou judiciaires suivies dans le journal. Chaque événement a aussi un champ `x` : 3 à 4 phrases qui expliquent ce que c'est (institution ou sommet, qui y participe, ce que mesure l'indice ou ce que décide la réunion) et pourquoi c'est important pour les marchés ou la politique ; il s'affiche quand on clique sur « En savoir plus ». Ajoute les nouveaux, corrige ceux qui changent, et garde les événements passés (le site les grise). Ne mets un événement que si sa date est confirmée par une source fiable (site officiel, agence) ; sinon n'en mets pas.
