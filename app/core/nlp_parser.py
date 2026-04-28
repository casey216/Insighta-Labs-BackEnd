"""
Rule-based natural language query parser.
No AI or LLMs used — pure regex/keyword matching.
"""
import re
from typing import Optional, Dict

from app.schemas.profile import AgeGroup, FilterParams, Gender

# Country name → ISO 2-letter code mapping (common ones)
COUNTRY_MAP: Dict[str, str] = {
    "nigeria": "NG", "nigerian": "NG",
    "ghana": "GH", "ghanaian": "GH",
    "kenya": "KE", "kenyan": "KE",
    "south africa": "ZA", "south african": "ZA",
    "ethiopia": "ET", "ethiopian": "ET",
    "egypt": "EG", "egyptian": "EG",
    "tanzania": "TZ", "tanzanian": "TZ",
    "uganda": "UG", "ugandan": "UG",
    "angola": "AO", "angolan": "AO",
    "cameroon": "CM", "cameroonian": "CM",
    "senegal": "SN", "senegalese": "SN",
    "mali": "ML", "malian": "ML",
    "ivory coast": "CI", "cote d'ivoire": "CI",
    "mozambique": "MZ", "mozambican": "MZ",
    "zambia": "ZM", "zambian": "ZM",
    "zimbabwe": "ZW", "zimbabwean": "ZW",
    "rwanda": "RW", "rwandan": "RW",
    "benin": "BJ", "beninese": "BJ",
    "togo": "TG", "togolese": "TG",
    "niger": "NE", "nigerien": "NE",
    "burkina faso": "BF", "burkinabe": "BF",
    "guinea": "GN", "guinean": "GN",
    "gabon": "GA", "gabonese": "GA",
    "congo": "CG", "congolese": "CG",
    "democratic republic of congo": "CD", "drc": "CD",
    "somalia": "SO", "somali": "SO",
    "sudan": "SD", "sudanese": "SD",
    "libya": "LY", "libyan": "LY",
    "morocco": "MA", "moroccan": "MA",
    "algeria": "DZ", "algerian": "DZ",
    "tunisia": "TN", "tunisian": "TN",
    "united states": "US", "usa": "US", "american": "US",
    "united kingdom": "GB", "uk": "GB", "britain": "GB", "british": "GB",
    "france": "FR", "french": "FR",
    "germany": "DE", "german": "DE",
    "india": "IN", "indian": "IN",
    "china": "CN", "chinese": "CN",
    "brazil": "BR", "brazilian": "BR",
    "canada": "CA", "canadian": "CA",
    "australia": "AU", "australian": "AU",
    "japan": "JP", "japanese": "JP",
    "russia": "RU", "russian": "RU",
    "mexico": "MX", "mexican": "MX",
    "indonesia": "ID", "indonesian": "ID",
    "pakistan": "PK", "pakistani": "PK",
    "bangladesh": "BD", "bangladeshi": "BD",
    "philippines": "PH", "philippine": "PH", "filipino": "PH",
    "vietnam": "VN", "vietnamese": "VN",
    "turkey": "TR", "turkish": "TR",
    "iran": "IR", "iranian": "IR",
    "iraq": "IQ", "iraqi": "IQ",
    "saudi arabia": "SA", "saudi": "SA",
    "spain": "ES", "spanish": "ES",
    "italy": "IT", "italian": "IT",
    "colombia": "CO", "colombian": "CO",
    "argentina": "AR", "argentinian": "AR",
    "poland": "PL", "polish": "PL",
    "ukraine": "UA", "ukrainian": "UA",
    "netherlands": "NL", "dutch": "NL",
    "portugal": "PT", "portuguese": "PT",
    "sweden": "SE", "swedish": "SE",
    "norway": "NO", "norwegian": "NO",
    "denmark": "DK", "danish": "DK",
    "finland": "FI", "finnish": "FI",
    "switzerland": "CH", "swiss": "CH",
    "austria": "AT", "austrian": "AT",
    "belgium": "BE", "belgian": "BE",
    "new zealand": "NZ",
    "malawi": "MW", "malawian": "MW",
    "namibia": "NA", "namibian": "NA",
    "botswana": "BW", "batswana": "BW",
    "lesotho": "LS",
    "swaziland": "SZ", "eswatini": "SZ",
    "eritrea": "ER", "eritrean": "ER",
    "djibouti": "DJ", "djiboutian": "DJ",
    "comoros": "KM",
    "seychelles": "SC",
    "mauritius": "MU",
    "mauritanian": "MR", "mauritania": "MR",
    "cape verde": "CV",
    "sao tome": "ST",
    "equatorial guinea": "GQ",
    "central african republic": "CF",
    "chad": "TD", "chadian": "TD",
    "sierra leone": "SL",
    "liberia": "LR", "liberian": "LR",
    "gambia": "GM", "gambian": "GM",
}

# Age group definitions
AGE_GROUPS = {
    "child": (0, 12),
    "teenager": (13, 17),
    "adult": (18, 64),
    "senior": (65, 150),
    "young": (16, 24),
}

GENDER_KEYWORDS = {
    "male": ["male", "males", "man", "men", "boy", "boys", "guys"],
    "female": ["female", "females", "woman", "women", "girl", "girls", "ladies", "lady"],
}

AGE_GROUP_KEYWORDS = {
    "child": ["child", "children", "kids", "kid"],
    "teenager": ["teenager", "teenagers", "teen", "teens", "adolescent", "adolescents", "youth"],
    "adult": ["adult", "adults"],
    "senior": ["senior", "seniors", "elderly", "elder", "old"],
    "young": ["young"],  # special — maps to 16–24 range only
}


def parse_natural_language_query(q: str) -> Optional[FilterParams]:
    """
    Parse a plain English query into filter parameters.
    Returns None if the query cannot be interpreted.
    """
    if not q or not q.strip():
        return None

    q_lower = q.strip().lower()
    filters = FilterParams()
    matched_something = False

    # --- Gender ---
    for gender, keywords in GENDER_KEYWORDS.items():
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        if re.search(pattern, q_lower):
            filters.gender = Gender(gender)
            matched_something = True
            break

    # Check if both genders mentioned (e.g., "male and female")
    has_male = any(re.search(r'\b' + kw + r'\b', q_lower)
                   for kw in GENDER_KEYWORDS["male"])
    has_female = any(re.search(r'\b' + kw + r'\b', q_lower)
                     for kw in GENDER_KEYWORDS["female"])
    if has_male and has_female:
        # Both genders — don't filter by gender
        filters.gender = None

    # --- Age group / "young" special case ---
    for group, keywords in AGE_GROUP_KEYWORDS.items():
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        if re.search(pattern, q_lower):
            if group == "young":
                # "young" → 16–24 range (not a stored age_group)
                filters.min_age = 16
                filters.max_age = 24
            else:
                filters.age_group = AgeGroup(group)
            matched_something = True
            break

    # --- Explicit age mentions: "above X", "over X", "below X", "under X", "between X and Y" ---
    # "above X" / "over X" → min_age = X
    above_match = re.search(
        r'\b(?:above|over|older than|greater than)\s+(\d+)\b',
        q_lower)
    if above_match:
        filters.min_age = int(above_match.group(1))
        matched_something = True

    # "below X" / "under X" → max_age = X
    below_match = re.search(
        r'\b(?:below|under|younger than|less than)\s+(\d+)\b',
        q_lower)
    if below_match:
        filters.max_age = int(below_match.group(1))
        matched_something = True

    # "between X and Y"
    between_match = re.search(r'\bbetween\s+(\d+)\s+and\s+(\d+)\b', q_lower)
    if between_match:
        filters.min_age = int(between_match.group(1))
        filters.max_age = int(between_match.group(2))
        matched_something = True

    # Explicit age: "aged X" / "age X"
    aged_match = re.search(r'\b(?:aged?|age)\s+(\d+)\b', q_lower)
    if aged_match:
        age = int(aged_match.group(1))
        filters.min_age = age
        filters.max_age = age
        matched_something = True

    # --- Country matching ---
    # Try multi-word countries first (longest match wins)
    sorted_countries = sorted(COUNTRY_MAP.keys(), key=len, reverse=True)
    for country_name in sorted_countries:
        if country_name in q_lower:
            filters.country_id = COUNTRY_MAP[country_name]
            matched_something = True
            break

    # --- "from X" pattern as fallback (extract word after "from") ---
    if not filters.country_id:
        from_match = re.search(
            r'\bfrom\s+([a-z\s]+?)(?:\s+(?:aged?|above|over|below|under|between|who|that|with|$)|\s*$)',
            q_lower)
        if from_match:
            possible_country = from_match.group(1).strip()
            # Try to match it
            if possible_country in COUNTRY_MAP:
                filters.country_id = COUNTRY_MAP[possible_country]
                matched_something = True

    if not matched_something:
        return None

    return filters
