"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Upload } from "lucide-react";
import heroVisual from "@/assets/hero-visual.jpg";
import { useToast } from "@/components/ui/use-toast";

const ACCEPTED_MIME = ["application/pdf", "image/jpeg", "image/png"];
const MAX_BYTES = 5 * 1024 * 1024; // 5MB

const Hero = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [parsed, setParsed] = useState<{ pages: number; text: string } | null>(null);
  const { toast } = useToast();

  const openFilePicker = () => fileInputRef.current?.click();

  const validateFile = (file: File) => {
    if (!ACCEPTED_MIME.includes(file.type)) {
      toast({ title: "Unsupported file", description: "Please upload a PDF, JPG, or PNG.", variant: "destructive" });
      return false;
    }
    if (file.size > MAX_BYTES) {
      toast({ title: "File too large", description: "Max file size is 5MB.", variant: "destructive" });
      return false;
    }
    return true;
  };

  const handleFile = async (file: File) => {
    if (!validateFile(file)) return;

    setSelectedFile(file);
    setParsed(null); // reset previous parse result

    // Image preview (PDFs won't preview here)
    if (file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }

    // Parse PDFs via FastAPI
    const isPdf = file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
    if (!isPdf) {
      toast({ title: "Image selected", description: "Preview shown. Parsing runs for PDFs only." });
      return;
    }

    try {
      setIsUploading(true);
      const formData = new FormData();
      formData.append("resume", file); // must match FastAPI param name

      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const msg = await res.text().catch(() => "");
        throw new Error(msg || `Upload failed with status ${res.status}`);
      }

      const data: {
        ok: boolean;
        filename: string;
        pages: number;
        first_page_text: string;
      } = await res.json();

      setParsed({ pages: data.pages ?? 0, text: data.first_page_text ?? "" });
      toast({ title: "Parsed resume", description: `Detected ${data.pages ?? 0} page(s).` });
    } catch (err: any) {
      toast({ title: "Upload failed", description: err?.message ?? "Something went wrong.", variant: "destructive" });
    } finally {
      setIsUploading(false);
    }
  };

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    e.currentTarget.value = ""; // allow re-selecting same file
  };

  const onDrop = (e: React.DragEvent<HTMLElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };
  const onDragOver = (e: React.DragEvent<HTMLElement>) => e.preventDefault();

  return (
    <section
      className="relative min-h-screen flex items-center justify-center overflow-hidden px-4 py-20"
      onDrop={onDrop}
      onDragOver={onDragOver}
      aria-label="Hero section. Drag and drop your resume here, or use the upload button."
    >
      {/* Background gradient effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary/10 via-transparent to-secondary/10 pointer-events-none" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[120px] animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-[120px] animate-pulse" />

      <div className="container mx-auto relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left content */}
          <div className="space-y-8 text-center lg:text-left">
            <div className="inline-block px-4 py-2 rounded-full bg-primary/10 border border-primary/20 backdrop-blur-sm">
              <span className="text-sm font-medium gradient-text">Career Intelligence Platform</span>
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl leading-tight">
              Transform Your Career <span className="gradient-text">Trajectory</span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto lg:mx-0">
              Benchmark your resume against anonymized peer data, identify skill gaps, and discover your optimal career path with AI-powered insights.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button
                variant="hero"
                size="lg"
                className="group"
                onClick={openFilePicker}
                disabled={isUploading}
                aria-label="Upload your resume as PDF, JPG, or PNG"
              >
                {isUploading ? "Uploading..." : "Upload Resume"}
                <Upload className="ml-2 h-5 w-5 group-hover:translate-y-1 transition-transform" />
              </Button>

              <Button variant="outline" size="lg">
                See How It Works
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>

              {/* Hidden file input, triggered by the button */}
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".pdf,image/jpeg,image/png,application/pdf"
                onChange={onInputChange}
              />
            </div>

            {/* Selected file details / preview */}
            {selectedFile && (
              <div className="mt-4 flex items-center gap-4 justify-center lg:justify-start">
                {previewUrl ? (
                  <img src={previewUrl} alt="Resume preview" className="w-16 h-16 rounded-md object-cover border" />
                ) : (
                  <div className="w-16 h-16 rounded-md border flex items-center justify-center text-xs text-muted-foreground">
                    PDF
                  </div>
                )}
                <div className="text-sm">
                  <div className="font-medium">{selectedFile.name}</div>
                  <div className="text-muted-foreground">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </div>
                </div>
              </div>
            )}

            {/* Parsed text (first page) */}
            {parsed && (
              <div className="mt-4 text-left max-w-2xl mx-auto lg:mx-0">
                <div className="text-sm text-muted-foreground mb-1">
                  {parsed.pages} page(s) detected — first page text:
                </div>
                <pre className="whitespace-pre-wrap text-sm border rounded p-3 max-h-60 overflow-auto">
                  {parsed.text || "(no text found)"}
                </pre>
              </div>
            )}

            <div className="flex items-center gap-8 justify-center lg:justify-start text-sm">
              <div>
                <div className="text-2xl font-bold gradient-text">10K+</div>
                <div className="text-muted-foreground">Profiles Analyzed</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div>
                <div className="text-2xl font-bold gradient-text">500+</div>
                <div className="text-muted-foreground">Career Paths</div>
              </div>
              <div className="w-px h-12 bg-border" />
              <div>
                <div className="text-2xl font-bold gradient-text">95%</div>
                <div className="text-muted-foreground">Success Rate</div>
              </div>
            </div>
          </div>

          {/* Right visual */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden border border-primary/20 shadow-2xl glow-primary">
              <img
                src={heroVisual}
                alt="Career growth visualization showing upward trajectory and network connections"
                className="w-full h-auto"
              />
            </div>
            <div className="absolute -bottom-6 -right-6 w-72 h-72 bg-secondary/30 rounded-full blur-3xl -z-10" />
            <div className="absolute -top-6 -left-6 w-72 h-72 bg-primary/30 rounded-full blur-3xl -z-10" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
