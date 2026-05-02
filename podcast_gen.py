import os
import time
import google.generativeai as genai
from typing import Optional

# --- Configuration ---
# The API key is provided by the environment at runtime
API_KEY = ""
genai.configure(api_key=API_KEY)

class AIPodcastEngine:
    def __init__(self, model_name: str = "gemini-2.5-flash-preview-09-2025"):
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=(
                "You are a world-class Podcast Scriptwriter. Your goal is to transform "
                "input text into an engaging, high-energy, two-person podcast script "
                "between 'Host' (curious, relatable) and 'Expert' (knowledgeable, insightful). "
                "Include scene markers like [Music Intro], [Short Pause], [Laughter], "
                "and [Music Outro]. Ensure the dialogue feels natural with interruptions, "
                "agreement, and conversational filler."
            )
        )

    def generate_script(self, content: str, tone: str = "Informative") -> Optional[str]:
        """
        Generates a podcast script based on input content and chosen tone.
        Includes exponential backoff for API reliability.
        """
        prompt = f"""
        TONE: {tone}
        CONTENT TO TRANSFORM:
        {content}

        INSTRUCTIONS:
        1. Create a dialogue between 'Host' and 'Expert'.
        2. Format it clearly as 'Host: [Speech]' and 'Expert: [Speech]'.
        3. Use the requested tone: {tone}.
        4. Insert audio cues in brackets.
        """

        # Exponential Backoff Implementation
        retries = 5
        for i in range(retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                if i == retries - 1:
                    print(f"Error: All {retries} retries failed. {str(e)}")
                    return None
                wait_time = 2**i
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
        return None

def main():
    print("🎙️ AI-Podcast-Engine | Hammad Virk")
    print("-" * 30)
    
    engine = AIPodcastEngine()
    
    # Example Usage
    user_content = input("Paste your article/text content here: ")
    print("\nSelect Tone: [1] Informative [2] Funny [3] Debate")
    tone_choice = input("Choice (1-3): ")
    
    tones = {"1": "Informative", "2": "Funny", "3": "Debate"}
    selected_tone = tones.get(tone_choice, "Informative")
    
    print(f"\n✨ Generating your {selected_tone} podcast script...\n")
    
    script = engine.generate_script(user_content, selected_tone)
    
    if script:
        print("="*50)
        print(script)
        print("="*50)
        
        # Save to file
        with open("generated_script.txt", "w", encoding="utf-8") as f:
            f.write(script)
        print("\n✅ Script saved to 'generated_script.txt'")
    else:
        print("❌ Failed to generate script. Please check your connection or API status.")

if __name__ == "__main__":
    main()
