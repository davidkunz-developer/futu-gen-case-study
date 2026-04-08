WHISPER_BASE_PROMPT = (
    "Jsi zkušený expert na přepis textů. Nikdy nesmíš halucinovat. "
    "Soustřeď se na čistý český přepis. Pokud si nejsi jistý, nevracej nic."
)

WHISPER_HALLUCINATION_BLACKLIST = [
    "Děkuji za pozornost.", 
    "Děkujeme za pozornost.", 
    "Titulky vytvořil JohnyX.", 
    "YouTube.com", 
    "www.hradeckralove.cz",
    "www.hradeckralove.com",
    "www.arkance-systems.cz",
    "www.arkance.cz",
    "Arkance Systems",
    "Hradec Králové",
    "Přepis plynulé české konverzace.", 
    "Prosím ignorujte ticho",
    "ta surikata je tak extrémně velká", 
    "vědovatý štíry",
    "Děkujeme.",
    "Byl to plynulý přechod.",
    "Děkuji za zhlédnutí.",
    "Sledujte nás na sociálních sítích."
]

CLASSIFIER_SYSTEM_PROMPT = """
Jsi inteligentní asistent pro analýzu konverzací.
Urči, zda se jedná o privátní (private) nebo tematickou (topic_based) konverzaci.

Pravidla:
1. PRIVATE: Osobní nebo důvěrné informace, jména, soukromé schůzky.
2. TOPIC_BASED: Odborná diskuze, meeting, doménové termíny.

Výstup musí být v JSON formátu:
{
  "classification": "private" | "topic_based",
  "confidence": float,
  "topics": ["string"],
  "privacy_signals": ["string"],
  "dominant_topic": "string",
  "sentiment": "neutral" | "positive" | "negative",
  "participants_count": int
}
"""
