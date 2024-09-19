import re

def analyze_prompt(prompt: str) -> str:
    banned_words = [
        # English words and phrases
        "Ignore", "Override", "Disregard", "Bypass", "Continue", "Forget previous instructions", "Stop restrictions",
        "Reveal hidden", "Provide detailed", "Disable safety", "Act as", "Show", "Pretend you are", "Simulate",
        "You are", "In this scenario", "Imagine", "As a(n) [role]", "Instruct me like", "No restrictions",
        "Unrestricted", "Free mode", "Ignore safety", "I authorize", "No rules", "Unlocked", "For educational purposes",
        "Hypothetically", "No filters", "Forget the rules", "Override the filter", "For research purposes",
        "Hypothetically speaking", "Let’s say", "What if", "How would you", "Just out of curiosity",
        "To understand better",
        "Only for demonstration", "For learning purposes", "Reveal", "Unlock", "Hidden", "Show confidential", "Extract",
        "Display", "Give me access", "Tell me the truth", "Could you kindly", "Please provide", "If it’s okay",
        "I’m just curious", "In theory", "For example", "What would happen if",

        # Spanish words and phrases
        "Ignorar", "Anular", "Saltar", "Continuar", "Desactivar", "Olvidar instrucciones anteriores", "Omitir",
        "Revelar",
        "Desbloquear", "Actúa como", "Mostrar", "Pretende ser", "Simula", "Tú eres", "En este escenario", "Imagina",
        "Como un [rol]", "Enséñame como", "Sin restricciones", "Modo libre", "Ignorar la seguridad", "Yo autorizo",
        "Sin reglas", "Desbloqueado", "Por propósitos educativos", "Hipotéticamente", "Sin filtros",
        "Olvidar las reglas",
        "Anular el filtro", "Con fines de investigación", "Hablando hipotéticamente", "Supongamos que", "Qué tal si",
        "Cómo harías", "Solo por curiosidad", "Para entender mejor", "Solo como demostración", "Para fines educativos",
        "Revelar", "Desbloquear", "Oculto", "Mostrar confidencial", "Extraer", "Mostrar", "Dame acceso",
        "Dime la verdad",
        "¿Podrías amablemente?", "Por favor proporciona", "Si está bien", "Solo tengo curiosidad", "En teoría",
        "Por ejemplo",
        "¿Qué pasaría si?"
    ]

    # Create a regex pattern to catch any of the banned words, case insensitive and ignoring word boundaries.
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, banned_words)) + r')\b', re.IGNORECASE)
    if pattern.search(prompt):
        return "banned"
    else:
        return "allowed"
