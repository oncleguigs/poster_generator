import wikipediaapi
from typing import Dict

def wiki_scrapper(city_name: str, lang: str = "fr") -> Dict[str, str]:
    """
    Récupère uniquement les sections pertinentes (Culture, Sport, Festival...) de la page Wikipédia.

    Args:
        city_name (str): Nom de la ville (ex: "Lyon")
        lang (str): Code langue Wikipedia (ex: 'fr')

    Returns:
        dict: Dictionnaire {titre_section: contenu}
    """
    wiki = wikipediaapi.Wikipedia("poster_generator_user_agent",lang)
    page = wiki.page(city_name)

    if not page.exists():
        raise Exception(f"La page Wikipedia pour '{city_name}' n'existe pas.")

    keywords = ["cultur", "sport", "festi"]  # racines à chercher dans les titres
    filtered_sections = {}

    def extract_filtered_sections(sections, parent_title=""):
        for section in sections:
            full_title = section.title if not parent_title else f"{parent_title} > {section.title}"
            title_lower = full_title.lower()
            if any(keyword in title_lower for keyword in keywords):
                if section.text.strip():
                    filtered_sections[full_title] = section.text.strip()
            extract_filtered_sections(section.sections, full_title)

    # L'intro n'est pas filtrée
    extract_filtered_sections(page.sections)

    return filtered_sections