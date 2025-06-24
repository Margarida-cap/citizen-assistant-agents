import re
from datetime import datetime

#–– compile once at module load ––#
EMAIL_REGEX     = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
NAME_REGEX      = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,}$")
COUNTRY_REGEX   = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,}$")
ADDRESS_REGEX   = re.compile(r"^\d+\s+[\w\s.,'-]{3,}$")
PHONE_REGEX     = re.compile(r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$")
SSN_REGEX       = re.compile(
    r"^(?!000|666|9\d{2})\d{3}-"    # area
    r"(?!00)\d{2}-"                 # group
    r"(?!0000)\d{4}$"               # serial
)

VALID_SEX       = {"male","female","m","f","other","non-binary","nb"}
VALID_DOC_TYPES = {"passport","card","license","both","other"}
VALID_HAIR      = {"black","brown","blonde","red","gray","white","bald","other"}
VALID_EYES      = {"brown","blue","green","hazel","gray","amber","other"}

def validate_sex(value: str) -> bool:
    return value.strip().lower() in VALID_SEX

def validate_full_name(value: str) -> bool:
    v = value.strip()
    return bool(NAME_REGEX.match(v))

def validate_other_names(value: str) -> bool:
    v = value.strip()
    if not v:
        return True
    # comma-separated list of “other” names
    return all(NAME_REGEX.match(name.strip()) for name in v.split(","))

def validate_birth_place(value: str) -> bool:
    # require at least two letters (city/town)
    v = value.strip()
    return bool(NAME_REGEX.match(v))

def validate_country(value: str) -> bool:
    return bool(COUNTRY_REGEX.match(value.strip()))

def validate_address(value: str) -> bool:
    # must start with number + street name
    return bool(ADDRESS_REGEX.match(value.strip()))

def validate_document_type(value: str) -> bool:
    return value.strip().lower() in VALID_DOC_TYPES

def validate_height(value: str) -> bool:
    v = value.strip().lower()
    # imperial: 5'11" or 5' 11"
    m = re.match(r"^(\d{1,1,2})'\s*(\d{1,2})\"?$", v)
    if m:
        ft, inch = map(int, m.groups())
        return 2 <= ft <= 8 and 0 <= inch < 12
    # metric: 150cm or 150 cm
    m2 = re.match(r"^(\d{2,3})\s?cm$", v)
    if m2:
        cm = int(m2.group(1))
        return 50 <= cm <= 272
    return False

def validate_hair_color(value: str) -> bool:
    return value.strip().lower() in VALID_HAIR

def validate_eye_color(value: str) -> bool:
    return value.strip().lower() in VALID_EYES

def validate_occupation(value: str) -> bool:
    return len(value.strip()) >= 2

def validate_employer(value: str) -> bool:
    return len(value.strip()) >= 2

def validate_phone_number(value: str) -> bool:
    return bool(PHONE_REGEX.match(value.strip()))

def validate_email(value: str) -> bool:
    return bool(EMAIL_REGEX.match(value.strip()))

def validate_ssn(value: str) -> bool:
    return bool(SSN_REGEX.match(value.strip()))

def validate_date_of_birth(value: str) -> bool:
    v = value.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            # will raise ValueError if invalid
            datetime.strptime(v, fmt)
            return True
        except ValueError:
            pass
    return False
