import base64
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
import openai
from typing import Dict
from agents import Agent, Runner

HEADERS = {
    'User-Agent': 'CityscapeCanvas/1.0 (Python Port)'
}


class ExtractedCityFeatures(BaseModel):
    cityName: str = Field(..., description="Name of the city")
    typeOfPlace: str = Field(..., description="Type of place, e.g., city, town, village")
    touristicPlaces: List[str] = Field(..., description="List of popular touristic places in the city")
    geographicalDetails: List[str] = Field(..., description="List of key geographical features, e.g., rivers, mountains in the background, coastal areas")
    cultralDetails: List[str] = Field(..., description="List of cultural details and what's happening, e.g., festivals, traditions, cuisines..")
    architecturalStyle: str = Field(..., description="Dominant architectural style of the city")
    dominantColorsForStructures: List[str] = Field(..., description="List of dominant colors for man-made structures in the city")
    dominantColorsForNaturalElements: List[str] = Field(..., description="List of dominant colors for natural elements in the city")

    @property
    def combinedPointsOfInterest(self) -> List[str]:
        """Returns touristic places and cultural details combined into a single list."""
        return self.touristicPlaces + self.cultralDetails


class ExtractCityFeaturesOutput(BaseModel):
    cityName: str
    features: ExtractedCityFeatures
    wikipediaImageUrl: Optional[str]
    firstGoogleImageUrl: Optional[str]
    satelliteImageUrl: Optional[str]
    panoramaImageUrl: Optional[str]
    otherImageUrls: List[Tuple[str, str]] 


def fetch_image_as_data_uri(image_url: str, source_name: str, query: str) -> Optional[str]:
    try:
        if not image_url.startswith("http"):
            if image_url.startswith("data:image"):
                return image_url
            print(f"Skipping potentially invalid image URL from {source_name} for query '{query}': {image_url}")
            return None

        response = requests.get(image_url, headers=HEADERS)
        if not response.ok:
            print(f"Failed to fetch image from {image_url} (source: {source_name}): {response.status_code}")
            return None

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            if image_url.endswith(".png"):
                content_type = "image/png"
            elif image_url.endswith(".jpg") or image_url.endswith(".jpeg"):
                content_type = "image/jpeg"
            elif image_url.endswith(".gif"):
                content_type = "image/gif"
            elif image_url.endswith(".webp"):
                content_type = "image/webp"
            else:
                content_type = "image/jpeg"

        b64 = response.content.encode("base64") if hasattr(response.content, "encode") else base64.b64encode(response.content).decode()
        return f"data:{content_type};base64,{b64}"

    except Exception as e:
        print(f"Error fetching image from {image_url} (source: {source_name}): {e}")
        return None


def get_wikipedia_image_as_data_uri(city_name: str) -> Optional[str]:
    try:
        search_name = city_name.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{search_name}"
        response = requests.get(url, headers=HEADERS)
        if not response.ok:
            print(f"Failed to fetch Wikipedia page for {city_name}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        image_url = None

        infobox_img = soup.select_one('table.infobox img')
        if infobox_img:
            image_url = infobox_img.get('src')

        if not image_url:
            og_image = soup.select_one('meta[property="og:image"]')
            if og_image:
                image_url = og_image.get('content')

        if not image_url:
            thumb_img = soup.select_one('#mw-content-text .thumbimage')
            if thumb_img:
                image_url = thumb_img.get('src')

        if image_url:
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = 'https://en.wikipedia.org' + image_url
            return fetch_image_as_data_uri(image_url, "Wikipedia", city_name)

    except Exception as e:
        print(f"Error getting Wikipedia image for {city_name}: {e}")
    return None


def get_google_image_search_first_result_as_data_uri(query: str) -> Optional[str]:
    search_url = f"https://www.google.com/search?tbm=isch&q={requests.utils.quote(query)}"
    response = requests.get(search_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
    if not response.ok:
        print(f"Failed to fetch Google Images for query: {query}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.find_all("img", class_="DS1iW")[0]
    if img_tag:
        image_url = img_tag.get("src") or img_tag.get("data-src")
        if image_url and (image_url.startswith("http") or image_url.startswith("data:image")):
            return fetch_image_as_data_uri(image_url, "Google Images", query)

    return None


