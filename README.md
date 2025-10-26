# Career Compass 🧭

**Your Data-Driven Roadmap for Career Growth**

Career Compass transforms career confusion into clarity by providing personalized, AI-powered career navigation. Upload your resume and receive a strategic blueprint showing exactly what skills to learn next and how to advance your career.

## 🚀 Features

- **AI-Powered Resume Analysis**: Upload your PDF resume and get instant skill extraction and benchmarking
- **Strategic Skill Gap Identification**: Discover exactly which skills are holding you back from your target roles
- **Personalized Career Roadmap**: Receive tailored learning recommendations and career progression paths
- **Market-Aligned Insights**: Get recommendations grounded in current industry demands and trends
- **Privacy-First Design**: Your data is anonymized and protected throughout the process

## 🛠️ Built With

### AI & Machine Learning
- **Google Gemini API 2.5 Flash** - Advanced reasoning for career recommendations
- **Sentence Transformers** - Semantic skill understanding and matching
- **KMeans Clustering** - Skill categorization and pattern recognition
- **Prompt Engineering** - Custom templates for actionable insights

### Backend & API
- **FastAPI** - High-performance backend framework
- **Python** - Core programming language
- **JavaScript** - Frontend functionality
- **pdfplumber** - PDF text extraction
- **JSON APIs** - Data communication

### Frontend & Visualization
- **Loveable** - Intuitive user interface
- **JavaScript** - Interactive elements
- **Matplotlib** - Data visualization

### Data Processing & Analysis
- **Pandas & NumPy** - Data manipulation and analysis
- **Jupyter Notebook** - Data exploration and prototyping
- **Semantic Search Algorithms** - Intelligent skill matching

## 🎯 How It Works

1. **Upload**: Securely upload your resume PDF
2. **Analyze**: Our AI extracts and benchmarks your skills against market patterns
3. **Identify**: Discover critical skill gaps and growth opportunities
4. **Plan**: Receive your personalized career roadmap with specific next steps

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/career-compass.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Google Gemini API key to .env

# Run the application
python main.py
```

## 🚀 Quick Start

1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Add it to your environment variables:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```
3. Launch the application and upload your resume to get started!

## 💡 Usage Examples

```python
# Example of generating career insights
from career_compass import CareerAnalyzer

analyzer = CareerAnalyzer()
results = analyzer.analyze_resume("path/to/your/resume.pdf")

print(f"Missing skills: {results.missing_skills}")
print(f"Learning path: {results.learning_recommendations}")
print(f"Career progression: {results.career_path}")
```

## 🏆 Why Career Compass?

### For Job Seekers
- **Stop guessing** what skills to learn next
- **Save time** by focusing on high-impact learning
- **Gain confidence** with a clear career strategy

### For Career Changers
- **Identify transferable skills**
- **Discover viable transition paths**
- **Build a targeted learning plan**

### For Students
- **Understand market demands**
- **Build relevant skill portfolios**
- **Plan your career from day one**

## 🔧 API Documentation

### Analyze Resume
```http
POST /api/analyze
Content-Type: multipart/form-data

{
  "resume": "file.pdf",
  "target_role": "Data Scientist"
}
```

Response:
```json
{
  "skills_found": ["Python", "SQL", "Excel"],
  "skills_missing": ["Machine Learning", "Docker"],
  "learning_path": [
    "Complete Kaggle ML course",
    "Learn containerization basics"
  ],
  "readiness_score": 65
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built during the DS + X Hackathon 2025
- Thanks to Google for the Gemini API
- Inspired by the challenges of modern career navigation

## 📞 Contact

Have questions or want to collaborate?

- **Team**: Verna Lin, Sheryl Yang, Aaron Huang, Mahad Ahmed
- **Email**: team@careercompass.dev
- **Project Link**: [https://github.com/your-username/career-compass](https://github.com/your-username/career-compass)

## 🚀 Future Roadmap

- [ ] Real-time job market integration
- [ ] Personalized learning platform partnerships
- [ ] Career progression simulation
- [ ] Mobile application
- [ ] Enterprise platform for universities and companies

---

<div align="center">

**Stop guessing, start navigating your career with confidence.** 🧭

</div>