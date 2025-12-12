import re

def deobfuscate_name(name):
    
    name = re.sub(r"\s*\([^)]*(?:Europe|EUR|USA|US|Japan|JPN|JP|World|Asia|Korea|KOR|China|CHN|Australia|AUS|France|FRA|Germany|GER|DEU|Spain|SPA|Italy|ITA|UK|Britain|English|En|Fr|De|Es|It|Pt|Ru|Ja|Ko|Zh|Nordic|Scandinavia|Brazil|Latin America)\s*[^)]*\)", "", name, flags=re.IGNORECASE)
    
    name = re.sub(r"\s*\([A-Z][a-z](?:,[A-Z][a-z])*\)", "", name)
    
    name = re.sub(r"\s*\((?:Rev|Revision|v|Ver|Version)[\s\d.]+\)", "", name, flags=re.IGNORECASE)
    
    name = re.sub(r"\s*\((?:NDSi Enhanced|DSi|NDS|Dump|Decrypted|Encrypted|Clean)\)", "", name, flags=re.IGNORECASE)
    
    name = re.sub(r"\s*\(\d{4}\)", "", name)
    
    name = re.sub(r"\s*\([^)]*\)", "", name)

    name = re.sub(r"\s*\[[^\]]*\]", "", name)

    name = re.sub(r"\s*\{[^}]*\}", "", name)

    name = re.sub(r"\s{2,}", " ", name)

    name = re.sub(r"^[\s.]+|[\s.]+$", "", name)

    if name.endswith('.nds'):
        name = name[:-4]
    if name.endswith('.srl'):
        name = name[:-4]
    if name.endswith('.dsi'):
        name = name[:-4]
    if name.endswith('.gba'):
        name = name[:-4]
    
    return name.strip()