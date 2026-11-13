import enum


class UserRole(str, enum.Enum):
    CANDIDATE = "CANDIDATE"
    COMPANY = "COMPANY"


class SkillCategory(str, enum.Enum):
    LANGUAGE = "LANGUAGE"
    FRAMEWORK = "FRAMEWORK"
    TOOL = "TOOL"
    SOFT_SKILL = "SOFT_SKILL"
    OTHER = "OTHER"


class SkillLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    EXPERT = "EXPERT"


class ContractType(str, enum.Enum):
    CDI = "CDI"
    CDD = "CDD"
    INTERNSHIP = "INTERNSHIP"
    FREELANCE = "FREELANCE"


class JobOfferStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    FILLED = "FILLED"


class SkillImportance(str, enum.Enum):
    REQUIRED = "REQUIRED"
    PREFERRED = "PREFERRED"


class ApplicationStatus(str, enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    VUE = "VUE"
    ACCEPTEE = "ACCEPTEE"
    REFUSEE = "REFUSEE"
