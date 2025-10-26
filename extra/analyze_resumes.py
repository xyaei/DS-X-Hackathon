from openai import OpenAI
import pandas as pd

# -------------------------------
# Step 1: Load cleaned dataset
# -------------------------------
df = pd.read_csv("cleaned_resumes.csv")

# -------------------------------
# Step 2: Initialize OpenAI client
# -------------------------------
client = OpenAI(api_key="sk-your-api-key-here")  # replace with your key

# -------------------------------
# Step 3: Pick a resume to analyze
# -------------------------------
user_resume = df["resume_text"].iloc[0]  # you can replace this with any row or your own input

# -------------------------------
# Step 4: Create a prompt
# -------------------------------
prompt = f"""
You are a helpful career advisor AI.
Compare this user's resume to other professionals in the dataset and identify:
1. Missing or trending skills they should learn
2. Recommended next steps for career growth
3. Learning paths or certifications that help bridge gaps

User resume:
{user_resume[:1500]}  # truncate if too long
"""

# -------------------------------
# Step 5: Get LLM response
# -------------------------------
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

# -------------------------------
# Step 6: Print insights
# -------------------------------
print("💡 Career advice:\n", response.choices[0].message.content)
