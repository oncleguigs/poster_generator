

from fetch import ExtractedCityFeatures


IMAGE_GENERATION_PROMPT = """Génère une illustration numérique **vectorielle, graphique, moderne et minimaliste** dans le style de **marcel travel posters** de la ville de **{CITY_NAME}**, conçue comme une affiche verticale au format 4:5.

# CONTENU À METTRE EN VALEUR

Mets en scène les éléments **emblématiques** et **distinctifs** de la ville :
- **Architecture locale représentative** : {ARCHITECTURAL_STYLE}
- **Lieux urbains majeurs** : {EMBLEMATIC_PLACES}
- **Éléments culturels identitaires (festivals, marchés, sports locaux...)** : {EMBLEMATIC_CULTURE}
- **Caractéristiques géographiques situées en arrière-plan ou en périphérie** : {GEOGRAPHICAL_DETAILS}

# DIRECTIVES STYLISTIQUES

- La **ville doit être clairement identifiable** et occuper le centre de la composition.
- **Évite la surreprésentation de la végétation** (arbres, parcs, nature) : elle ne doit pas masquer les éléments urbains.
- **Inclure des éléments de vie** : silhouettes de personnes en interaction (dans un style **flat** sans ombrage, en aplats de couleurs).
- **Ne te limite pas aux monuments connus** : représente aussi des éléments du quotidien (terrasses, places, événements, activités humaines…).
- **Respecte l’échelle et la perspective** pour que la ville soit réaliste et équilibrée.
- Intègre **uniquement le nom de la ville** ("{CITY_NAME}") dans une typographie élégante et cohérente avec le style graphique.
- N’ajoute **aucun autre texte** dans l’image.
- Format affiche vertical A3, ratio 4:5, haute résolution (300 DPI).
- Palette :
  - Structures & architecture : {DOMINANT_COLORS_FOR_STRUCTURES}
  - Nature & arrière-plan : {DOMINANT_COLORS_FOR_NATURAL_ELEMENTS}
- Les images jointes servent d'inspiration:
  - **satelliteView.jpg** et **panoramaView.jpg** qui définissent la structure de la composition et **cityView.jpg** pour la vue de la ville.
  - Les autres images sont les representations des lieux emblématiques et culturels de la ville, à intégrer dans l'illustration.

# STYLE VISUEL

- Illustration **à plat (flat design)** : pas d’ombres, pas de dégradés.
- Approche **graphique et stylisée**, avec des formes simples, couleurs franches et contrastées.
- L’ensemble doit être **lisible, épuré et reconnaissable**, même à distance.

"""

def build_prompt(city:ExtractedCityFeatures) -> str:
    """
    Build the prompt for image generation based on the city features.
    
    Args:
        city (ExtractedCityFeatures): The features of the city to be used in the prompt.
        
    Returns:
        str: The formatted prompt string.
    """
    
    return IMAGE_GENERATION_PROMPT.format(
        CITY_NAME=city.cityName,
        EMBLEMATIC_PLACES="\n- ".join(city.touristicPlaces),
        EMBLEMATIC_CULTURE="\n- ".join(city.cultralDetails),
        ARCHITECTURAL_STYLE=city.architecturalStyle,
        GEOGRAPHICAL_DETAILS="\n- ".join(city.geographicalDetails),
        DOMINANT_COLORS_FOR_STRUCTURES=", " .join(city.dominantColorsForStructures),
        DOMINANT_COLORS_FOR_NATURAL_ELEMENTS=",  ".join(city.dominantColorsForNaturalElements)
    )