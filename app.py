from flask import Flask, render_template, request, jsonify
import markovify
import random

app = Flask(__name__)

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

# Training data for different relationship goals
TRAINING_DATA = {
    'Casual Dating': """
        Fun-loving person who enjoys spontaneous adventures and casual hangouts.
        Easy-going individual seeking someone to share laughs and good times.
        Laid-back soul looking for casual connections and memorable moments.
        Free spirit who loves exploring new places and meeting new people.
        Adventurous heart seeking someone for casual fun and exciting experiences.
    """,
    'Long-term Relationship': """
        Genuine person seeking a meaningful long-term connection with someone special.
        Looking for that special someone to build a future together.
        Seeking a partner to share life's beautiful moments and create lasting memories.
        Ready to find that special connection that grows deeper with time.
        Searching for a meaningful relationship built on trust and understanding.
    """,
    'Adventure Partner': """
        Thrill-seeker ready to explore the world with an adventurous partner.
        Looking for someone who shares my wanderlust and zest for life.
        Adventure enthusiast seeking a partner for life's exciting journeys.
        Ready to embark on new adventures with someone special.
        Seeking a fellow explorer for life's grand adventures.
    """,
    'Deep Connection': """
        Seeking someone who values deep conversations and genuine connections.
        Looking for a profound connection based on understanding and growth.
        Searching for someone who appreciates meaningful discussions and authentic bonds.
        Seeking a deep connection with someone who values genuine relationships.
        Looking for someone who understands the importance of emotional depth.
    """,
    'Friendship First': """
        Believing the best relationships start as friendships and grow naturally.
        Looking to build a connection that starts with genuine friendship.
        Seeking someone who values friendship as the foundation of a relationship.
        Hoping to find a friend first, and see where things lead naturally.
        Building meaningful connections starting with authentic friendship.
    """
}

# Create Markov models for each relationship goal
text_models = {
    goal: markovify.Text(text) for goal, text in TRAINING_DATA.items()
}

@app.route('/')
def index():
    return render_template('index.html', preferences=PREFERENCE_OPTIONS)

@app.route('/generate-bio', methods=['POST'])
def generate_bio():
    data = request.json
    
    try:
        # Get the model for the selected relationship goal
        model = text_models[data['relationship_goals']]
        
        # Generate base text using Markov chain
        generated_text = model.make_short_sentence(100)
        
        # Create personalized first line
        first_line = f"{data['personality']} {data['career']} passionate about {data['interests']}."
        
        # Combine with generated text
        bio = f"{first_line} {generated_text}"
        
        return jsonify({"bio": bio})
        
    except Exception as e:
        # Fallback template if something goes wrong
        fallback_bio = f"{data['personality']} {data['career']} passionate about {data['interests']}. "
        fallback_bio += f"Seeking {data['relationship_goals'].lower()} with someone who shares my enthusiasm."
        return jsonify({"bio": fallback_bio})

if __name__ == '__main__':
    app.run(debug=True) 