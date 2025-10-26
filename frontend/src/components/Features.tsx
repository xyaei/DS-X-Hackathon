import { Target, TrendingUp, Lightbulb, Users } from "lucide-react";
import skillsVisual from "@/assets/skills-visual.jpg";
import pathwayVisual from "@/assets/pathway-visual.jpg";

const features = [
  {
    icon: Target,
    title: "Skill Gap Analysis",
    description: "Identify critical competencies you need to develop based on industry benchmarks and peer comparisons.",
    visual: skillsVisual,
    alt: "Circular skill analysis dashboard showing competency gaps",
  },
  {
    icon: TrendingUp,
    title: "Career Path Mapping",
    description: "Visualize your potential career trajectories with clear milestones, transitions, and growth opportunities.",
    visual: pathwayVisual,
    alt: "Career pathway map showing multiple professional routes",
  },
  {
    icon: Lightbulb,
    title: "Learning Recommendations",
    description: "Get curated learning modules tailored to close your skill gaps and accelerate your career progression.",
  },
  {
    icon: Users,
    title: "Peer Benchmarking",
    description: "Compare your career trajectory against thousands of anonymized professionals in your field.",
  },
];

const Features = () => {
  return (
    <section className="py-24 px-4">
      <div className="container mx-auto">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl">
            Powerful <span className="gradient-text">Features</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Everything you need to navigate your career with confidence
          </p>
        </div>
        
        <div className="grid gap-12">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`grid lg:grid-cols-2 gap-8 items-center ${
                index % 2 === 1 ? "lg:flex-row-reverse" : ""
              }`}
            >
              <div className={`space-y-6 ${index % 2 === 1 ? "lg:order-2" : ""}`}>
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br from-primary to-secondary">
                  <feature.icon className="w-7 h-7 text-primary-foreground" />
                </div>
                
                <h3 className="text-3xl font-semibold">{feature.title}</h3>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
              
              <div className={`${index % 2 === 1 ? "lg:order-1" : ""}`}>
                {feature.visual ? (
                  <div className="relative rounded-2xl overflow-hidden border border-primary/20 shadow-xl">
                    <img
                      src={feature.visual}
                      alt={feature.alt}
                      className="w-full h-auto"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent" />
                  </div>
                ) : (
                  <div className="glass-card p-12 rounded-2xl border-primary/20">
                    <div className="space-y-4">
                      <div className="h-2 bg-gradient-to-r from-primary to-secondary rounded-full" />
                      <div className="h-2 bg-muted rounded-full w-3/4" />
                      <div className="h-2 bg-muted rounded-full w-5/6" />
                      <div className="h-2 bg-muted rounded-full w-2/3" />
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
