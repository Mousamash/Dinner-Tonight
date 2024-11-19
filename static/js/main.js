document.getElementById('bioForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        career: document.getElementById('career').value,
        personality: document.getElementById('personality').value,
        interests: document.getElementById('interests').value,
        relationship_goals: document.getElementById('relationship_goals').value
    };

    // Show loading state
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');

    try {
        const response = await fetch('/generate-bio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('generatedBio').textContent = data.bio;
            document.getElementById('result').classList.remove('hidden');
            document.getElementById('regenerateBtn').classList.remove('hidden');
        } else {
            alert('Error generating bio: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
});

document.getElementById('regenerateBtn').addEventListener('click', () => {
    document.getElementById('bioForm').dispatchEvent(new Event('submit'));
}); 