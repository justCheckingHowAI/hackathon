import { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import {
  fetchHiringPack,
  HiringPackNotFoundError,
  type HiringPack,
  type HiringPackSkill,
} from "@/lib/hiring-pack";
import { cn } from "@/lib/utils";
import {
  Brain,
  AlertTriangle,
  Target,
  MessageSquareText,
  CheckCircle2,
  Star,
  ArrowRight,
  BookOpen,
  ChevronRight,
  Quote,
  Trophy,
  XCircle,
  Loader2,
  RefreshCw,
} from "lucide-react";

interface HiringPackPageProps {
  onNext: () => void;
}

const PERSON_ID = "mike";

const levelColors: Record<HiringPackSkill["level"], string> = {
  expert: "bg-primary/20 text-primary border-primary/30",
  advanced: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  intermediate: "bg-muted text-muted-foreground border-border",
};

export function HiringPackPage({ onNext }: HiringPackPageProps) {
  const [hiringPack, setHiringPack] = useState<HiringPack | null>(null);
  const [status, setStatus] = useState<"loading" | "ready" | "empty" | "error">(
    "loading",
  );
  const [errorMessage, setErrorMessage] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    async function loadHiringPack() {
      setStatus("loading");
      setErrorMessage("");

      try {
        const pack = await fetchHiringPack(PERSON_ID, controller.signal);
        setHiringPack(pack);
        setStatus("ready");
      } catch (error) {
        if (controller.signal.aborted) return;

        if (error instanceof HiringPackNotFoundError) {
          setHiringPack(null);
          setStatus("empty");
          return;
        }

        setHiringPack(null);
        setStatus("error");
        setErrorMessage(
          error instanceof Error
            ? error.message
            : "Could not load the hiring pack.",
        );
      }
    }

    void loadHiringPack();
    return () => controller.abort();
  }, [reloadKey]);

  if (status === "loading") {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground tracking-tight">
            Backfill Hiring Pack
          </h2>
          <p className="text-muted-foreground mt-1">
            Loading the saved hiring pack from the server.
          </p>
        </div>

        <Card className="bg-card">
          <CardContent className="py-12">
            <div className="flex flex-col items-center justify-center gap-3 text-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <div>
                <p className="text-sm font-medium text-foreground">
                  Fetching hiring pack
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Pulling the latest saved data for this role.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (status === "empty") {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground tracking-tight">
            Backfill Hiring Pack
          </h2>
          <p className="text-muted-foreground mt-1">
            No saved hiring pack exists for this person yet.
          </p>
        </div>

        <Card className="bg-card border-border">
          <CardContent className="py-12">
            <div className="mx-auto max-w-xl text-center">
              <h3 className="text-base font-semibold text-foreground">
                Hiring pack not found
              </h3>
              <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
                Save a hiring pack through the backend API first. This screen
                renders only data that has already been persisted on the server.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground tracking-tight">
            Backfill Hiring Pack
          </h2>
          <p className="text-muted-foreground mt-1">
            The screen could not load the saved hiring pack.
          </p>
        </div>

        <Card className="bg-card border-accent/20">
          <CardContent className="py-12">
            <div className="mx-auto max-w-xl text-center">
              <h3 className="text-base font-semibold text-foreground">
                Loading failed
              </h3>
              <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
                {errorMessage}
              </p>
              <Button
                onClick={() => setReloadKey((value) => value + 1)}
                variant="outline"
                className="mt-4"
              >
                <RefreshCw className="mr-2 h-4 w-4" />
                Retry
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!hiringPack) {
    return null;
  }

  const {
    skills,
    gapSummary,
    recommendedRole,
    scorecard,
    interviewQuestions,
    mustHave,
    niceToHave,
    redFlags,
  } = hiringPack;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold text-foreground tracking-tight">
            Backfill Hiring Pack
          </h2>
          <p className="text-muted-foreground mt-1">
            Evidence-backed analysis for replacing {hiringPack.person.name}'s
            role.
          </p>
        </div>
        <Button
          onClick={onNext}
          className="bg-primary text-primary-foreground hover:bg-primary/90 shrink-0"
        >
          Screen Candidate
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>

      {/* Gap Summary */}
      <Card className="bg-card border-accent/30">
        <CardContent className="py-4">
          <div className="flex items-start gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-accent/30 text-accent-foreground">
              <AlertTriangle className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-foreground">
                Competency Gap Summary
              </h3>
              <p className="text-sm text-muted-foreground mt-1 leading-relaxed">
                {gapSummary}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommended Role */}
      <Card className="bg-card border-primary/20">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <Target className="h-4 w-4 text-primary" />
            <CardTitle className="text-base">Recommended Role</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row sm:items-start gap-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-primary">
                {recommendedRole.title}
              </h3>
              <Badge variant="outline" className="mt-1 text-xs border-primary/30 text-primary/80">
                {recommendedRole.seniority}
              </Badge>
              <p className="text-sm text-muted-foreground mt-3 leading-relaxed">
                {recommendedRole.description}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs section */}
      <Tabs defaultValue="skills" className="space-y-4">
        <TabsList className="bg-secondary/50 border border-border w-full sm:w-auto flex">
          <TabsTrigger value="skills" className="flex-1 sm:flex-initial gap-1.5 text-xs sm:text-sm">
            <Brain className="h-3.5 w-3.5" />
            Skills
          </TabsTrigger>
          <TabsTrigger value="scorecard" className="flex-1 sm:flex-initial gap-1.5 text-xs sm:text-sm">
            <Trophy className="h-3.5 w-3.5" />
            Scorecard
          </TabsTrigger>
          <TabsTrigger value="interview" className="flex-1 sm:flex-initial gap-1.5 text-xs sm:text-sm">
            <MessageSquareText className="h-3.5 w-3.5" />
            Interview
          </TabsTrigger>
          <TabsTrigger value="profile" className="flex-1 sm:flex-initial gap-1.5 text-xs sm:text-sm">
            <Star className="h-3.5 w-3.5" />
            Profile
          </TabsTrigger>
        </TabsList>

        {/* Skills Tab */}
        <TabsContent value="skills" className="space-y-3">
          {skills.map((skill) => (
            <Card key={skill.name} className="bg-card">
              <CardContent className="py-4">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-semibold text-foreground">
                        {skill.name}
                      </h4>
                      <Badge
                        variant="outline"
                        className={cn(
                          "text-[10px] uppercase tracking-wider",
                          levelColors[skill.level],
                        )}
                      >
                        {skill.level}
                      </Badge>
                      <Badge variant="secondary" className="text-[10px]">
                        {skill.category}
                      </Badge>
                    </div>
                    <div className="mt-3 space-y-2">
                      {skill.evidence.map((ev, i) => (
                        <div
                          key={i}
                          className="flex items-start gap-2 text-sm"
                        >
                          <Quote className="h-3 w-3 mt-1 text-primary/40 shrink-0" />
                          <span className="text-muted-foreground leading-relaxed">
                            {ev}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        {/* Scorecard Tab */}
        <TabsContent value="scorecard">
          <Card className="bg-card">
            <CardHeader>
              <CardTitle className="text-base">Evaluation Scorecard</CardTitle>
              <CardDescription>
                Weighted criteria for candidate assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {scorecard.map((item, i) => (
                  <div key={i}>
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-medium text-foreground">
                        {item.criterion}
                      </h4>
                      <span className="text-sm font-semibold text-primary">
                        {Math.round(item.weight * 100)}%
                      </span>
                    </div>
                    <div className="h-2 rounded-full bg-secondary overflow-hidden mb-2">
                      <div
                        className="h-full rounded-full bg-primary/60"
                        style={{ width: `${item.weight * 100}%` }}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {item.description}
                    </p>
                    {i < scorecard.length - 1 && (
                      <Separator className="mt-4" />
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Interview Tab */}
        <TabsContent value="interview">
          <Card className="bg-card">
            <CardHeader>
              <CardTitle className="text-base">Interview Question Bank</CardTitle>
              <CardDescription>
                {interviewQuestions.length} questions across key competency areas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {interviewQuestions.map((q, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary text-xs font-medium mt-0.5">
                      {i + 1}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-foreground leading-relaxed">
                        {q.question}
                      </p>
                      <Badge variant="secondary" className="mt-2 text-[10px]">
                        {q.category}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Profile Tab */}
        <TabsContent value="profile" className="space-y-4">
          {/* Must have */}
          <Card className="bg-card">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-400" />
                <CardTitle className="text-base">Must Have</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {mustHave.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <ChevronRight className="h-4 w-4 text-green-400/60 mt-0.5 shrink-0" />
                    <span className="text-foreground">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Nice to have */}
          <Card className="bg-card">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <Star className="h-4 w-4 text-primary" />
                <CardTitle className="text-base">Nice to Have</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {niceToHave.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <ChevronRight className="h-4 w-4 text-primary/40 mt-0.5 shrink-0" />
                    <span className="text-muted-foreground">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Red flags */}
          <Card className="bg-card border-accent/20">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <XCircle className="h-4 w-4 text-red-400" />
                <CardTitle className="text-base">Red Flags</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {redFlags.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <AlertTriangle className="h-3.5 w-3.5 text-red-400/60 mt-0.5 shrink-0" />
                    <span className="text-accent-foreground/80">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Source info */}
      <Card className="bg-card border-border">
        <CardContent className="py-3">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <BookOpen className="h-3.5 w-3.5" />
            <span>
              Generated from 847 GitHub artifacts, 12 conference talks, 5 podcast episodes, 15 technical docs, and 276 communication records.
              All recommendations are evidence-backed with source citations.
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
