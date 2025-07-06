from fetch import ExtractCityFeaturesOutput
from agents import Agent, Runner

async def craft_prompt_for_city(city: ExtractCityFeaturesOutput) -> str:
    prompt = """Tu es un expert en ingénierie de prompts pour un modèle d’IA de génération d’images à partir de texte.
Ta mission est de créer un prompt textuel spécifique qui servira à générer une illustration numérique vectorielle, flat design et minimaliste, d’une ville, conçue comme une affiche de voyage verticale.

Utilise les informations suivantes pour la ville de {{{cityName}}} :

Type de lieu : {{{cityFeatures.typeOfPlace}}}
Lieux emblématiques : {{#each cityFeatures.touristicPlaces}}"
Détails culturels : {{#each cityFeatures.culturalDetails}}"
Éléments géographiques/naturels : {{#each cityFeatures.geographicalDetails}}"
Style architectural : "{{{cityFeatures.architecturalStyle}}}"
Couleurs dominantes pour les structures : {{#each cityFeatures.dominantColorsForStructures}}"
Couleurs dominantes pour les éléments naturels : {{#each cityFeatures.dominantColorsForNaturalElements}}"

En te basant sur toutes ces informations, génère un prompt textuel en remplissant les zones réservées dans le modèle suivant.
Le prompt généré DOIT strictement suivre la structure de ce modèle :

"Une illustration numérique vectorielle, plate et minimaliste de [TYPE DE LIEU] à [NOM DE LA VILLE], conçue comme une affiche de voyage verticale. Mettez en valeur les éléments urbains et humains les plus emblématiques, tels que [LISTE DES MONUMENTS ET CARACTÉRISTIQUES], tout en limitant l’arrière-plan naturel. Évitez toute surreprésentation de végétation, d’arbres ou d’espaces verts. Soulignez le style architectural local, tel que [DESCRIPTION DE L’ARCHITECTURE], ainsi que les éléments géographiques comme [DESCRIPTION DU PAYSAGE], uniquement en tant qu’arrière-plan subtil ou éléments de composition. Utilisez une palette de couleurs moderne et épurée dominée par [COULEURS DOMINANTES DES STRUCTURES] et [COULEURS DOMINANTES DES ÉLÉMENTS NATURELS]. Intégrez le nom de la ville, “[NOM DE LA VILLE]”, dans une typographie élégante et stylisée faisant partie de la composition. La mise en page doit être équilibrée et verticale (format affiche, ratio 4:5 ou A2/A3), optimisée pour une impression haute résolution (au moins 300 DPI). Le style doit être audacieux, géométrique et graphique, inspiré des affiches de voyage contemporaines. Aucun texte autre que le nom de la ville."
Sors uniquement le prompt textuel complet généré selon ce modèle.
N’inclus aucun autre texte, aucune explication, ni mise en forme markdown."""

    agent = Agent(name="Prompt crafter",
            instructions=prompt,
            model="gpt-4.1-mini",  
            output_type=str
        )

    response = await Runner.run(
        agent,
        input=f"Craft prompt for : {city}"
        )

    reply_content = response.final_output

    return reply_content


IMAGE_GENERATION_PROMPT = """Génère une illustration numérique vectorielle, graphique et minimaliste de la ville de '{CITY_NAME}', conçue comme une affiche verticale. 


# Spécificités de la ville 

Mets en valeur les éléments urbains et culturels les plus emblématiques, tels que :
{EMBLEMATIC_PLACES}

Style architectural: {ARCHITECTURAL_STYLE}
Emplacement géographique: {GEOGRAPHICAL_DETAILS}

 # Consignes

- Limite la surreprésentation de végétation et d'habitations
- Intégre le nom de la ville, {CITY_NAME}, dans une typographie élégante et stylisée faisant partie de la composition.
- Tu génères des images de ville faiblement touristiques, c'est important d'inclure les éléments emblématiques de la ville pour que l'acheteur puisse la reconnaitre.
- Format affiche, ratio 4:5, A3, optimisée pour une impression haute résolution (300 DPI)
- Aucun texte autre que le nom de la ville.
- Utilisez une palette de {DOMINANT_COLORS_FOR_STRUCTURES} et {DOMINANT_COLORS_FOR_NATURAL_ELEMENTS}.
"""