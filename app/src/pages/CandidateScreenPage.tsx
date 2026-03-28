import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import { candidateResult } from "@/lib/mock-data";
import {
  Upload,
  Phone,
  PhoneOff,
  Mic,
  FileText,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Award,
  BarChart3,
  MessageSquare,
  Loader2,
} from "lucide-react";

type ScreeningPhase = "upload" | "screening" | "results";

export function CandidateScreenPage() {
  const [phase, setPhase] = useState<ScreeningPhase>("upload");
  const [cvUploaded, setCvUploaded] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [callActive, setCallActive] = useState(false);
  const [callProgress, setCallProgress] = useState(0);
  const [transcriptLines, setTranscriptLines] = useState<
    { speaker: string; text: string }[]
  >([]);

  const simulateUpload = () => {
    setIsUploading(true);
    setTimeout(() => {
      setIsUploading(false);
      setCvUploaded(true);
    }, 1500);
  };

  const startScreening = () => {
    setPhase("screening");
    setCallActive(true);
    setCallProgress(0);
    setTranscriptLines([]);

    const lines = [
      {
        speaker: "Agent",
        text: "Hi Alex, thanks for joining. I'd like to start with your experience with React Native's new architecture. Can you tell me about a Fabric migration you've led?",
      },
      {
        speaker: "Alex",
        text: "Sure! At my previous company, I migrated our main app from the old bridge architecture to Fabric. It was a 200-screen app with about 40 custom native modules...",
      },
      {
        speaker: "Agent",
        text: "That's impressive scale. How did you handle backward compatibility for the native modules during the migration?",
      },
      {
        speaker: "Alex",
        text: "We built a compatibility layer that could detect which architecture was active and route accordingly. I actually open-sourced the approach — it's in my react-native-compat-bridge repo.",
      },
      {
        speaker: "Agent",
        text: "Great. Now, regarding build tooling — this role requires deep expertise with bundlers. What's your experience beyond Metro?",
      },
      {
        speaker: "Alex",
        text: "I've customized Metro extensively with custom transformers and resolvers. I haven't used Re.Pack directly, but I understand the Webpack integration model. I'm confident I could ramp up quickly.",
      },
    ];

    let i = 0;
    const interval = setInterval(() => {
      if (i < lines.length) {
        setTranscriptLines((prev) => [...prev, lines[i]]);
        setCallProgress(Math.round(((i + 1) / lines.length) * 100));
        i++;
      } else {
        clearInterval(interval);
        setCallActive(false);
        setTimeout(() => setPhase("results"), 1000);
      }
    }, 2500);
  };

  const scoreColor = (score: number) => {
    if (score >= 80) return "text-green-400";
    if (score >= 60) return "text-primary";
    return "text-red-400";
  };

  const scoreBarColor = (score: number, max: number) => {
    const pct = score / max;
    if (pct >= 0.8) return "bg-green-500/60";
    if (pct >= 0.6) return "bg-primary/60";
    return "bg-red-500/60";
  };

  // Upload phase
  if (phase === "upload") {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground tracking-tight">
            Candidate Screening
          </h2>
          <p className="text-muted-foreground mt-1">
            Upload a CV and run a voice screening session powered by Vapi.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* CV Upload */}
          <Card className="bg-card">
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <FileText className="h-4 w-4 text-primary" />
                Upload CV
              </CardTitle>
              <CardDescription>
                PDF format, max 10 MB
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!cvUploaded ? (
                <button
                  onClick={simulateUpload}
                  disabled={isUploading}
                  className="w-full flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed border-border hover:border-primary/40 p-8 transition-colors"
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="h-8 w-8 text-primary animate-spin" />
                      <span className="text-sm text-muted-foreground">
                        Processing CV...
                      </span>
                    </>
                  ) : (
                    <>
                      <Upload className="h-8 w-8 text-muted-foreground" />
                      <div>
                        <span className="text-sm text-primary font-medium">
                          Click to upload
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {" "}or drag and drop
                        </span>
                      </div>
                    </>
                  )}
                </button>
              ) : (
                <div className="flex items-center gap-3 rounded-lg border border-primary/20 bg-primary/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-md bg-primary/15 text-primary">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">
                      Alex_Chen_CV_2026.pdf
                    </p>
                    <p className="text-xs text-muted-foreground">
                      2.1 MB &bull; Uploaded
                    </p>
                  </div>
                  <CheckCircle2 className="h-5 w-5 text-green-400" />
                </div>
              )}
            </CardContent>
          </Card>

          {/* Voice Screening */}
          <Card className="bg-card">
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Phone className="h-4 w-4 text-primary" />
                Voice Screening
              </CardTitle>
              <CardDescription>
                AI-powered interview via Vapi
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center gap-4 py-4">
                <div
                  className={cn(
                    "flex h-20 w-20 items-center justify-center rounded-full border-2 transition-all",
                    cvUploaded
                      ? "border-primary/30 bg-primary/10"
                      : "border-border bg-secondary/30"
                  )}
                >
                  <Mic
                    className={cn(
                      "h-8 w-8",
                      cvUploaded
                        ? "text-primary"
                        : "text-muted-foreground/40"
                    )}
                  />
                </div>
                <p className="text-sm text-muted-foreground text-center">
                  {cvUploaded
                    ? "CV analyzed. Ready to start voice screening."
                    : "Upload a CV first to enable voice screening."}
                </p>
                <Button
                  onClick={startScreening}
                  disabled={!cvUploaded}
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  <Phone className="mr-2 h-4 w-4" />
                  Start Screening Call
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Screening phase
  if (phase === "screening") {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-foreground tracking-tight">
              Voice Screening
            </h2>
            <p className="text-muted-foreground mt-1">
              Live screening session with Alex Chen
            </p>
          </div>
          {callActive && (
            <Badge className="bg-accent text-accent-foreground animate-pulse gap-1.5">
              <span className="h-2 w-2 rounded-full bg-red-400" />
              Live
            </Badge>
          )}
        </div>

        <Card className="bg-card">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-primary" />
                Transcript
              </CardTitle>
              <span className="text-xs text-muted-foreground">
                {callProgress}% complete
              </span>
            </div>
            <Progress value={callProgress} className="h-1.5 mt-2" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-[60vh] overflow-y-auto">
              {transcriptLines.map((line, i) => (
                <div
                  key={i}
                  className={cn(
                    "flex gap-3 animate-in fade-in slide-in-from-bottom-2 duration-300",
                    line.speaker === "Agent" ? "" : "flex-row-reverse"
                  )}
                >
                  <div
                    className={cn(
                      "flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-medium",
                      line.speaker === "Agent"
                        ? "bg-primary/15 text-primary"
                        : "bg-secondary text-foreground"
                    )}
                  >
                    {line.speaker === "Agent" ? "AI" : "AC"}
                  </div>
                  <div
                    className={cn(
                      "rounded-lg px-4 py-3 max-w-[80%]",
                      line.speaker === "Agent"
                        ? "bg-secondary/60"
                        : "bg-primary/10"
                    )}
                  >
                    <p className="text-xs font-medium text-muted-foreground mb-1">
                      {line.speaker === "Agent"
                        ? "Gemellus Agent"
                        : "Alex Chen"}
                    </p>
                    <p className="text-sm text-foreground leading-relaxed">
                      {line.text}
                    </p>
                  </div>
                </div>
              ))}

              {callActive && (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  <span className="text-xs">Listening...</span>
                </div>
              )}
            </div>

            {!callActive && (
              <div className="mt-6 pt-4 border-t border-border flex items-center justify-center gap-2 text-sm text-muted-foreground">
                <PhoneOff className="h-4 w-4" />
                Call ended &mdash; generating results...
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  // Results phase
  const { matchScore, strengths, gaps, fitSummary, criteriaScores } =
    candidateResult;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground tracking-tight">
          Screening Results
        </h2>
        <p className="text-muted-foreground mt-1">
          Candidate assessment for Alex Chen
        </p>
      </div>

      {/* Match Score Hero */}
      <Card className="bg-card border-primary/20">
        <CardContent className="py-8">
          <div className="flex flex-col items-center text-center">
            <div className="relative">
              <svg className="h-32 w-32" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-secondary"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${matchScore * 3.14} 314`}
                  transform="rotate(-90 60 60)"
                  className={scoreColor(matchScore)}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div>
                  <span
                    className={cn(
                      "text-3xl font-bold",
                      scoreColor(matchScore)
                    )}
                  >
                    {matchScore}%
                  </span>
                </div>
              </div>
            </div>
            <h3 className="text-lg font-semibold text-foreground mt-4">
              Overall Match Score
            </h3>
            <p className="text-sm text-muted-foreground mt-1 max-w-md">
              Based on competency gap analysis, CV evaluation, and voice screening assessment.
            </p>
            <div className="flex gap-2 mt-3">
              <Badge className="bg-primary/15 text-primary border border-primary/20">
                <Award className="mr-1 h-3 w-3" />
                Recommended for Final Round
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Criteria Scores */}
        <Card className="bg-card">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-primary" />
              Criteria Scores
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {criteriaScores.map((cs, i) => (
                <div key={i}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm text-foreground">
                      {cs.criterion}
                    </span>
                    <span
                      className={cn(
                        "text-sm font-semibold",
                        scoreColor((cs.score / cs.maxScore) * 100)
                      )}
                    >
                      {cs.score}/{cs.maxScore}
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-secondary overflow-hidden">
                    <div
                      className={cn(
                        "h-full rounded-full transition-all",
                        scoreBarColor(cs.score, cs.maxScore)
                      )}
                      style={{
                        width: `${(cs.score / cs.maxScore) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Strengths & Gaps */}
        <div className="space-y-4">
          <Card className="bg-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-green-400" />
                Strengths
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {strengths.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <CheckCircle2 className="h-3.5 w-3.5 text-green-400 mt-0.5 shrink-0" />
                    <span className="text-foreground">{s}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-card border-accent/20">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <XCircle className="h-4 w-4 text-amber-400" />
                Development Areas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {gaps.map((g, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <XCircle className="h-3.5 w-3.5 text-amber-400/60 mt-0.5 shrink-0" />
                    <span className="text-muted-foreground">{g}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Fit Summary */}
      <Card className="bg-card">
        <CardHeader>
          <CardTitle className="text-base">Fit Summary & Recommendation</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {fitSummary}
          </p>
          <Separator className="my-4" />
          <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
            <p className="text-xs text-muted-foreground">
              Assessment generated by Gemellus AI. Final hiring decisions remain with the team.
            </p>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                Export Report
              </Button>
              <Button
                size="sm"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Schedule Final Round
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
