import re

def deobfuscate_name(name):
    name = re.sub(r"\s*\([^)]*(?:Europe|USA|Japan|World|Asia|Korea|China|Australia|France|Germany|Spain|Italy|UK|En|Eu|Eur|Fr|De|Es|It|Pt|Ru|Ja|Ko|Zh)\s*[^)]*\)", "", name, flags=re.IGNORECASE)

    name = re.sub(r"\s*\([A-Z][a-z](?:,[A-Z][a-z])*\)", "", name)

    name = re.sub(r"\s*\((?:Rev|v|Ver)[\s\d.]+\)", "", name, flags=re.IGNORECASE)

    name = re.sub(r"\s*\([^)]*\)", "", name)
    
    name = re.sub(r"\s*\[[^\]]*\]", "", name)
    
    name = re.sub(r"\s*\{[^}]*\}", "", name)
    
    name = re.sub(r"\s{2,}", " ", name)

    name = re.sub(r"\.+$", "", name)
    
    name = name.strip()
    
    return name
