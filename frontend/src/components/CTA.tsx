import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const CTA = () => {
  return (
    <section className="py-24 px-4 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-primary/10 via-secondary/10 to-primary/10 pointer-events-none" />
      
      <div className="container mx-auto relative z-10">
        <div className="glass-card rounded-3xl p-12 md:p-16 text-center border-primary/30 relative overflow-hidden">
          {/* Background effects */}
          <div className="absolute top-0 left-1/4 w-64 h-64 bg-primary/20 rounded-full blur-[100px] -z-10" />
          <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-secondary/20 rounded-full blur-[100px] -z-10" />
          
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-4xl md:text-5xl lg:text-6xl">
              Ready to Transform Your{" "}
              <span className="gradient-text">Career?</span>
            </h2>
            
            <p className="text-xl text-muted-foreground">
              Join thousands of professionals who have already discovered their optimal career path. Start your journey today with a free profile analysis.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="hero" size="lg" className="group">
                Get Started Free
                <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="outline" size="lg">
                Schedule a Demo
              </Button>
            </div>
            
            <p className="text-sm text-muted-foreground">
              No credit card required • Full analysis in minutes • Cancel anytime
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
