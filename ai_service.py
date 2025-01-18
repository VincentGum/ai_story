from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_story(character_type, story_length, story_theme):
    try:
        prompt = f"""Create a children's story with the following parameters:
        - Main character: {character_type}
        - Length: {story_length}
        - Theme: {story_theme}
        
        Make it engaging, educational, and appropriate for children.
        Include a moral lesson related to the theme.
        Use simple language and short paragraphs.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative children's story writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        return "Sorry, there was an error generating your story. Please try again." 