import { Upload, Brain, Map, Sparkles } from "lucide-react";

const steps = [
  {
    icon: Upload,
    title: "Upload Your Resume",
    description: "Securely upload your resume and let our AI parse your career history, skills, and achievements.",
  },
  {
    icon: Brain,
    title: "Benchmark Analysis",
    description: "Your profile is compared against thousands of anonymized peer trajectories to identify your position.",
  },
  {
    icon: Map,
    title: "Discover Pathways",
    description: "Visualize emerging career paths, skill gaps, and optimal role transitions on an interactive map.",
  },
  {
    icon: Sparkles,
    title: "Personalized Blueprint",
    description: "Receive a tailored roadmap with learning modules and actionable steps to achieve your goals.",
  },
];

const HowItWorks = () => {
  return (
    <section className="py-24 px-4 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent pointer-events-none" />
      
      <div className="container mx-auto relative z-10">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl">
            How It <span className="gradient-text">Works</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Four simple steps to unlock your career intelligence
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div
              key={index}
              className="relative group"
            >
              <div className="glass-card p-6 rounded-2xl h-full transition-all duration-300 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="relative">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <step.icon className="w-8 h-8 text-primary-foreground" />
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-background border-2 border-primary flex items-center justify-center text-xs font-bold">
                      {index + 1}
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-semibold">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                </div>
              </div>
              
              {/* Connector line */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-4 w-8 h-0.5 bg-gradient-to-r from-primary to-transparent" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
