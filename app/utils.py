# Utility functions (e.g., for AI API interaction)
def call_ai_api(prompt):
    # Placeholder for OpenRouter API integration
    import requests
    # Example: response = requests.post('https://api.openrouter.ai', json={'prompt': prompt})
    # return response.json()
    return {'result': 'AI response placeholder'}

import os
import requests

def modify_recipe_with_ai(recipe_content, user_preferences, api_key=None):
    """
    Modyfikuje przepis zgodnie z preferencjami użytkownika za pomocą OpenRouter (Gemini Flash 2.0).
    Zwraca zmodyfikowany przepis lub komunikat o błędzie.
    """
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None, "Brak klucza API OpenRouter. Skontaktuj się z administratorem."

    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://healthymeal.local/",  # wymagane przez OpenRouter
        "X-Title": "HealthyMeal AI Recipe Modifier"
    }
    prompt = (
        "Zmodyfikuj poniższy przepis kulinarny, aby był zgodny z następującymi preferencjami użytkownika: "
        f"{user_preferences}. Zachowaj format przepisu. Skup się na zastępowaniu składników, dostosowywaniu ilości lub proponowaniu alternatywnych kroków. "
        "Unikaj składników wymienionych jako 'do unikania'. Jeśli alergia dotyczy składnika, usuń go lub zastąp bezpiecznym odpowiednikiem. "
        "Odpowiedź powinna zawierać tylko zmodyfikowany przepis w formie tekstowej.\n"
        f"\nOryginalny przepis:\n{recipe_content}"
    )
    data = {
        "model": "google/gemini-flash-1.5",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    try:
        resp = requests.post(endpoint, headers=headers, json=data, timeout=30)
        if resp.status_code != 200:
            return None, f"Błąd API OpenRouter: {resp.status_code} {resp.text}"
        response_json = resp.json()
        # OpenRouter response: choices[0]['message']['content']
        choices = response_json.get("choices")
        if not choices or not choices[0].get("message", {}).get("content"):
            return None, "Nie udało się uzyskać odpowiedzi z API OpenRouter."
        return choices[0]["message"]["content"], None
    except Exception as e:
        return None, f"Błąd podczas komunikacji z OpenRouter: {str(e)}"
