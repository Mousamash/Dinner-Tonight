from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import random
import gc  # For garbage collection

app = Flask(__name__)

# Initialize with a smaller model
generator = pipeline('text-generation', model='distilgpt2', device=-1)  # device=-1 forces CPU usage

# Clear memory after model load
gc.collect()

PREFERENCE_OPTIONS = {
    'career': [
        'Software Engineer', 'Artist', 'Entrepreneur', 'Chef', 
        'Teacher', 'Musician', 'Doctor', 'Writer'
    ],
    'personality': [
        'Adventurous', 'Creative', 'Compassionate', 'Outgoing', 
        'Introverted', 'Analytical', 'Free-spirited'
    ],
    'interests': [
        'Cooking', 'Traveling', 'Fitness', 'Music', 'Literature', 
        'Technology', 'Gaming', 'Photography'
    ],
    'relationship_goals': [
        'Casual Dating', 'Long-term Relationship', 'Adventure Partner',
        'Deep Connection', 'Friendship First'
    ]
}

# Enhanced prompt templates for GPT-Neo
PROMPT_TEMPLATES = {
    'Casual Dating': 
        "Dating Profile: A {personality} {career} who loves {interests}. They're looking for casual dating and fun connections. Bio:",
    'Long-term Relationship':
        "Dating Profile: A {personality} {career} with a passion for {interests}, seeking a meaningful long-term relationship. Bio:",
    'Adventure Partner':
        "Dating Profile: An adventurous {personality} {career} who's passionate about {interests}, looking for someone to share exciting experiences. Bio:",
    'Deep Connection':
        "Dating Profile: A thoughtful {personality} {career} who finds joy in {interests}, seeking someone for deep, meaningful connection. Bio:",
    'Friendship First':
        "Dating Profile: A genuine {personality} {career} who enjoys {interests}, believing the best relationships start as friendships. Bio:"
}

@app.route('/')
def index():
    return render_template('index.html', preferences=PREFERENCE_OPTIONS)

@app.route('/generate-bio', methods=['POST'])
def generate_bio():
    data = request.json
    
    try:
        # Get the appropriate prompt template
        prompt_template = PROMPT_TEMPLATES[data['relationship_goals']]
        
        # Create the full prompt
        prompt = prompt_template.format(
            personality=data['personality'].lower(),
            career=data['career'].lower(),
            interests=data['interests'].lower()
        )
        
        # Generate text using GPT-Neo with tuned parameters
        result = generator(
            prompt,
            max_length=150,
            min_length=75,
            num_return_sequences=1,
            temperature=0.8,  # Slightly lower for more focused outputs
            top_k=50,        # Added for better word selection
            top_p=0.95,      # Adjusted for better coherence
            repetition_penalty=1.3,
            do_sample=True,  # Enable sampling for more creative outputs
            pad_token_id=50256
        )
        
        # Clean up the generated text
        generated_text = result[0]['generated_text']
        
        # Remove the prompt and "Bio:" from the output
        if "Bio:" in generated_text:
            generated_text = generated_text.split("Bio:")[1].strip()
        
        # Clean up and format the bio
        sentences = [s.strip() for s in generated_text.split('.') if s.strip()][:2]
        final_bio = '. '.join(sentences) + '.'
        
        # Additional cleanup for better formatting
        final_bio = final_bio.replace('..', '.')
        final_bio = final_bio.replace('  ', ' ')
        final_bio = ' '.join(final_bio.split())  # Remove extra whitespace
        
        # Ensure the bio starts with a capital letter
        final_bio = final_bio[0].upper() + final_bio[1:]
        
        return jsonify({"bio": final_bio})
        
    except Exception as e:
        # Enhanced fallback template
        personality_phrases = {
            'Creative': 'bringing artistic vision to',
            'Adventurous': 'always ready to explore',
            'Compassionate': 'bringing warmth to',
            'Outgoing': 'energetically pursuing',
            'Introverted': 'finding quiet joy in',
            'Analytical': 'thoughtfully approaching',
            'Free-spirited': 'bringing spontaneity to'
        }
        
        phrase = personality_phrases.get(data['personality'], 'passionate about')
        fallback_bio = f"{data['personality']} {data['career']} {phrase} {data['interests']}. "
        fallback_bio += f"Seeking {data['relationship_goals'].lower()} with someone who shares my enthusiasm."
        return jsonify({"bio": fallback_bio})

if __name__ == '__main__':
    app.run(debug=True) 