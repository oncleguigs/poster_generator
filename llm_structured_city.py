from typing import List, Optional
from pydantic import BaseModel
from agents import Agent, Runner
from fetch import  ExtractCityFeaturesOutput, ExtractedCityFeatures

from dotenv import load_dotenv

from wiki_scrapper import wiki_scrapper

load_dotenv()

async def extract_city_features_via_ai(city_name: str) -> ExtractedCityFeatures:
    wiki_infos = wiki_scrapper(city_name, lang="fr")

    prompt = f"""
Tu es une IA chargée d’extraire des informations détaillées et structurées sur une ville afin d’inspirer une illustration numérique vectorielle de style minimaliste.
Étant donné le nom de la ville, cherche sa page Wikipédia et utilise également tes connaissances générales. Extrais les informations suivantes et présente-les dans le format structuré spécifié :

Fournis les éléments suivants :

typeOfPlace : Une courte phrase descriptive du type de lieu (par ex. : « métropole animée », « ville côtière historique », « charmant village de montagne », « paisible bourg au bord d’une rivière »).
touristicPlaces : Une liste de 3 lieux ou monuments emblématiques et touristiques. Fournir uniquement les noms ou de très brèves descriptions. (par ex. : ["Tour Eiffel", "Musée du Louvre", "Cathédrale Notre-Dame"])
geographicalDetails : Une liste de 2 caractéristiques géographiques clés (par ex. : rivières, montagnes, littoral, paysages naturels dominants, configuration urbaine si pertinent) (par ex. : ["Située sur les rives de la Seine", "Présente des collines marquées comme Montmartre"])
cultralDetails:  Liste de 2 éléments culturels très spécifiques, propres à la ville, qui peuvent être identifiés par un nom précis et représentés visuellement.
    Évite absolument les formulations génériques comme « marché local », « festival culturel », « gastronomie régionale ».
    Les informations doivent etre exactes, base toi sur les sections pertinentes de la page Wikipédia de la ville fournises à la fin du prompt.
    Préfère :
        Des événements ou fêtes avec un nom propre et une date régulière (ex. : Carnaval de Limoux, Festival de l’Épine),
        Des traditions artisanales uniques (ex. : faïences de Moustiers, tissage de soie à Lyon),
        Des spécialités culinaires précises et typiquement associées à la ville (ex. : pogne de Romans, gratin dauphinois si le nom de la ville est Grenoble ou Romans),
        Des pratiques culturelles ou rituels locaux distinctifs (ex. : illuminations du 8 décembre à Lyon, combat naval fleuri à Villefranche-sur-Mer).
architecturalStyle : Une brève description du ou des styles architecturaux dominants de la ville. (par ex. : "Principalement haussmannien avec des influences gothiques et Art nouveau")
dominantColorsForStructures : Une liste de 1 à 3 couleurs dominantes pour les structures/bâtiments construits par l’homme. (par ex. : ["Pierre calcaire crème", "Toits en zinc gris", "Terracotta"])
dominantColorsForNaturalElements : Une liste de 1 à 3 couleurs dominantes pour les éléments naturels comme le ciel, l’eau, la flore. (par ex. : ["Bleu profond (Seine)", "Vert luxuriant (parcs)", "Bleu pâle (ciel)"])


❌ Éviter absolument les descriptions trop vagues comme :« Fête locale avec animations », « Région agricole », ou « Patrimoine religieux important ».

wikipedia infos: ${wiki_infos}
"""

    try:

        agent = Agent(name="city feature",
            instructions=prompt,
            model="gpt-4.1-mini",  
            output_type=ExtractedCityFeatures
        )

        response = await Runner.run(
            agent,
            input="Generate structured city features for the city: " + city_name,
            )

        reply_content = response.final_output

        return reply_content

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        raise
