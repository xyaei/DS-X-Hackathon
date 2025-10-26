"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Upload } from "lucide-react";
import heroVisual from "@/assets/hero-visual.jpg";
import { useToast } from "@/components/ui/use-toast";

const API_BASE = "http://localhost:8000/career";
const ACCEPTED_MIME = ["application/pdf", "image/jpeg", "image/png"];
const MAX_BYTES = 5 * 1024 * 1024; // 5MB

type UploadResumeResponse = {
  status: "success" | "error";
  filename: string;
  text_length: number;
  full_text?: string;             // <-- NEW from backend
  anonymized_preview: string;
  extracted_skills: string[];
  skill_count: number;
};

type RolesResponse = { status: "success"; roles: string[] };

type AnalyzeRequest = {
  resume_text: string;
  skills: string[];
  target_role: string;
  experience_level?: string;
  industry?: string;
};

type AnalyzeResponse = {
  status: "success";
  analysis: any;                 // depends on analyzer; fallback returns a known shape
  role: string;
  industry: string;
  analysis_source?: string;      // "fallback_analyzer" or "enhanced_analyzer"
};

const Hero = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const [roles, setRoles] = useState<string[]>([]);
  const [role, setRole] = useState<string>("Data Analyst");

  const [isLoadingRoles, setIsLoadingRoles] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [parsed, setParsed] = useState<{
    text: string;
    skills: string[];
    filename: string;
  } | null>(null);

  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const { toast } = useToast();

  // Load available roles once
  useEffect(() => {
    const loadRoles = async () => {
      try {
        setIsLoadingRoles(true);
        const res = await fetch(`${API_BASE}/roles`);
        if (!res.ok) throw new Error(`Failed to load roles (${res.status})`);
        const data: RolesResponse = await res.json();
        setRoles(data.roles || []);
        if (data.roles?.length && !data.roles.includes(role)) {
          setRole(data.roles[0]);
        }
      } catch (err: any) {
        toast({
          title: "Could not fetch roles",
          description: err?.message ?? "Please check the backend.",
          variant: "destructive",
        });
      } finally {
        setIsLoadingRoles(false);
      }
    };
    loadRoles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const openFilePicker = () => fileInputRef.current?.click();

  const validateFile = (file: File) => {
    if (!ACCEPTED_MIME.includes(file.type)) {
      toast({
        title: "Unsupported file",
        description: "Please upload a PDF, JPG, or PNG.",
        variant: "destructive",
      });
      return false;
    }
    if (file.size > MAX_BYTES) {
      toast({
        title: "File too large",
        description: "Max file size is 5MB.",
        variant: "destructive",
      });
      return false;
    }
    return true;
  };

  // Stage only; don’t upload yet
  const stageFile = (file: File) => {
    if (!validateFile(file)) return;
    setSelectedFile(file);
    setParsed(null);
    setAnalysis(null);

    if (file.type.startsWith("image/")) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }
  };

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) stageFile(file);
    e.currentTarget.value = ""; // allow re-selecting same file
  };

  const onDrop = (e: React.DragEvent<HTMLElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) stageFile(file);
  };
  const onDragOver = (e: React.DragEvent<HTMLElement>) => e.preventDefault();

  // Submit: upload resume, then analyze
  const onAnalyze = async () => {
    if (!selectedFile) {
      toast({ title: "No file selected", description: "Please choose a resume first." });
      return;
    }

    try {
      setIsAnalyzing(true);
      setParsed(null);
      setAnalysis(null);

      // 1) Upload to /career/upload-resume (field "file")
      const formData = new FormData();
      formData.append("file", selectedFile);

      const uploadRes = await fetch(`${API_BASE}/upload-resume`, {
        method: "POST",
        body: formData,
      });

      if (!uploadRes.ok) {
        const msg = await uploadRes.text().catch(() => "");
        throw new Error(msg || `Upload failed (${uploadRes.status})`);
      }

      const uploadJson: UploadResumeResponse = await uploadRes.json();
      const fullText =
        uploadJson.full_text ??
        uploadJson.anonymized_preview ??
        ""; // backend now returns full_text for PDFs and text files
      const skills = uploadJson.extracted_skills ?? [];

      setParsed({
        text: uploadJson.anonymized_preview ?? "",
        skills,
        filename: uploadJson.filename,
      });

      toast({
        title: "Resume processed",
        description: `Found ${skills.length} skill(s).`,
      });

      // 2) Analyze using full extracted text
      const analyzePayload: AnalyzeRequest = {
        resume_text: fullText,
        skills,
        target_role: role,
        experience_level: "Intermediate",
        industry: "Technology",
      };

      const analyzeRes = await fetch(`${API_BASE}/analyze-resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(analyzePayload),
      });

      if (analyzeRes.ok) {
        const analyzeJson: AnalyzeResponse = await analyzeRes.json();
        setAnalysis(analyzeJson);
        const srcLabel =
          analyzeJson.analysis_source === "fallback_analyzer"
            ? "Local baseline"
            : "Enhanced analyzer";
        toast({
          title: "Analysis ready",
          description: `Source: ${srcLabel}`,
        });
      } else {
        // Non-fatal: still show parsed preview/skills
        const msg = await analyzeRes.text().catch(() => "");
        toast({
          title: "Analyzer not available",
          description: msg || "Showing extracted skills only.",
        });
      }
    } catch (err: any) {
      toast({
        title: "Analysis failed",
        description: err?.message ?? "Something went wrong.",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

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

            {/* Controls: Role + Upload + Analyze */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start items-stretch">
              {/* Role dropdown */}
              <div className="min-w-[220px]">
                <label htmlFor="role" className="sr-only">Target role</label>
                <select
                  id="role"
                  className="w-full h-11 rounded-md border bg-background px-3 text-sm"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  disabled={isLoadingRoles || isAnalyzing}
                  aria-label="Select your target role"
                >
                  {roles.length === 0 ? (
                    <option value={role} disabled>
                      {isLoadingRoles ? "Loading roles..." : "No roles available"}
                    </option>
                  ) : (
                    roles.map((r) => (
                      <option key={r} value={r}>
                        {r}
                      </option>
                    ))
                  )}
                </select>
              </div>

              <Button
                variant="hero"
                size="lg"
                className="group"
                onClick={openFilePicker}
                disabled={isAnalyzing}
                aria-label="Upload your resume as PDF, JPG, or PNG"
              >
                {selectedFile ? "Change File" : "Upload Resume"}
                <Upload className="ml-2 h-5 w-5 group-hover:translate-y-1 transition-transform" />
              </Button>

              <Button
                variant="outline"
                size="lg"
                onClick={onAnalyze}
                disabled={!selectedFile || isAnalyzing}
                aria-label="Submit and analyze resume"
              >
                {isAnalyzing ? "Analyzing..." : "Submit & Analyze"}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>

              {/* Hidden file input */}
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

            {/* Parsed text + skills */}
            {parsed && (
              <div className="mt-4 text-left max-w-2xl mx-auto lg:mx-0 space-y-3">
                <div className="text-sm text-muted-foreground">
                  Anonymized preview:
                </div>
                <pre className="whitespace-pre-wrap text-sm border rounded p-3 max-h-60 overflow-auto">
                  {parsed.text || "(no text found)"}
                </pre>
                <div className="text-sm text-muted-foreground">
                  Extracted skills: {parsed.skills.length ? parsed.skills.join(", ") : "(none detected)"}
                </div>
              </div>
            )}

            {/* Analysis results (if available) */}
            {analysis && (
              <div className="mt-4 text-left max-w-2xl mx-auto lg:mx-0 space-y-2 border rounded p-4">
                <div className="font-semibold">Analysis for role: {analysis.role}</div>
                <div className="text-xs text-muted-foreground">
                  Source: {analysis.analysis_source === "fallback_analyzer" ? "Local baseline" : "Enhanced analyzer"}
                </div>
                <pre className="whitespace-pre-wrap text-sm overflow-auto">
                  {JSON.stringify(analysis.analysis, null, 2)}
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
