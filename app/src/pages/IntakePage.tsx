import { useState, useRef, useEffect, useCallback, type DragEvent, type ChangeEvent } from "react";
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
import { mike, artifacts, type Artifact } from "@/lib/mock-data";
import {
  GitBranch,
  Mic,
  FileText,
  MessageSquare,
  Database,
  CheckCircle2,
  Play,
  Loader2,
  User,
  Briefcase,
  Calendar,
  FolderGit2,
  Upload,
  X,
  Plus,
  GitFork,
  Link,
  Trash2,
  FileUp,
  FileArchive,
  FileSpreadsheet,
  FileImage,
} from "lucide-react";

const artifactIcons: Record<Artifact["type"], typeof GitBranch> = {
  github: GitBranch,
  transcript: Mic,
  documentation: FileText,
  slack: MessageSquare,
  synthetic: Database,
};

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: "uploading" | "done" | "error";
  progress: number;
  errorMessage?: string;
  ragFileId?: string;
}

interface GithubRepo {
  id: string;
  url: string;
  owner: string;
  name: string;
  status: "pending" | "scraping" | "done" | "error";
  progress: number;
}

const API_URL = import.meta.env.VITE_API_URL;
const PERSON_ID = "mike";

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getFileIcon(type: string) {
  if (type.includes("pdf")) return FileText;
  if (type.includes("zip") || type.includes("tar") || type.includes("gz"))
    return FileArchive;
  if (type.includes("csv") || type.includes("sheet") || type.includes("excel"))
    return FileSpreadsheet;
  if (type.includes("image")) return FileImage;
  return FileUp;
}

function parseGithubUrl(input: string): { owner: string; name: string } | null {
  const trimmed = input.trim();

  // owner/repo format
  const slashMatch = trimmed.match(/^([a-zA-Z0-9_.-]+)\/([a-zA-Z0-9_.-]+)$/);
  if (slashMatch) return { owner: slashMatch[1], name: slashMatch[2] };

  // Full GitHub URL
  const urlMatch = trimmed.match(
    /github\.com\/([a-zA-Z0-9_.-]+)\/([a-zA-Z0-9_.-]+)/
  );
  if (urlMatch) return { owner: urlMatch[1], name: urlMatch[2] };

  return null;
}

interface IntakePageProps {
  onAnalysisComplete: () => void;
}

export function IntakePage({ onAnalysisComplete }: IntakePageProps) {
  const [selectedArtifacts, setSelectedArtifacts] = useState<Set<string>>(
    new Set(artifacts.map((a) => a.id))
  );
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [analysisStage, setAnalysisStage] = useState("");

  // File upload state
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // GitHub repo state
  const [githubRepos, setGithubRepos] = useState<GithubRepo[]>([]);
  const [repoInput, setRepoInput] = useState("");
  const [repoInputError, setRepoInputError] = useState("");

  // Fetch already-vectorized files on mount
  const fetchVectorizedFiles = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/vectorize/files`);
      if (!res.ok) return;
      const files: { name: string | null; display_name: string | null; state: string | null; size_bytes: string | null }[] = await res.json();
      const existing: UploadedFile[] = files.map((f, i) => ({
        id: `existing-${i}-${f.name ?? ""}`,
        name: f.display_name ?? f.name ?? "Unknown",
        size: f.size_bytes ? parseInt(f.size_bytes, 10) : 0,
        type: "application/octet-stream",
        status: "done" as const,
        progress: 100,
        ragFileId: f.name ?? undefined,
      }));
      setUploadedFiles((prev) => {
        // Merge: keep any currently-uploading files, add existing ones that aren't already present
        const existingIds = new Set(prev.map((p) => p.ragFileId).filter(Boolean));
        const newExisting = existing.filter((e) => !existingIds.has(e.ragFileId));
        return [...prev, ...newExisting];
      });
    } catch {
      // Silently ignore — API may not be running
    }
  }, []);

  useEffect(() => {
    fetchVectorizedFiles();
  }, [fetchVectorizedFiles]);

  const toggleArtifact = (id: string) => {
    setSelectedArtifacts((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // --- File upload handlers ---
  const uploadFileToApi = async (file: File) => {
    const id = `file-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
    const newFile: UploadedFile = {
      id,
      name: file.name,
      size: file.size,
      type: file.type || "application/octet-stream",
      status: "uploading",
      progress: 0,
    };
    setUploadedFiles((prev) => [...prev, newFile]);

    // Simulate progress while uploading (real XHR progress would require XMLHttpRequest)
    let prog = 0;
    const progressInterval = setInterval(() => {
      prog += Math.random() * 15 + 5;
      if (prog >= 90) {
        prog = 90;
        clearInterval(progressInterval);
      }
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === id ? { ...f, progress: Math.min(prog, 90) } : f
        )
      );
    }, 400);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(
        `${API_URL}/vectorize/upload`,
        { method: "POST", body: formData }
      );

      clearInterval(progressInterval);

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: "Upload failed" }));
        setUploadedFiles((prev) =>
          prev.map((f) =>
            f.id === id
              ? { ...f, status: "error", progress: 0, errorMessage: errorData.detail || "Upload failed" }
              : f
          )
        );
        return;
      }

      const result = await res.json();
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === id
            ? { ...f, status: "done", progress: 100, ragFileId: result.rag_file_id }
            : f
        )
      );
    } catch {
      clearInterval(progressInterval);
      setUploadedFiles((prev) =>
        prev.map((f) =>
          f.id === id
            ? { ...f, status: "error", progress: 0, errorMessage: "Network error — is the API running?" }
            : f
        )
      );
    }
  };

  const handleFiles = (files: FileList | File[]) => {
    Array.from(files).forEach(uploadFileToApi);
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
      e.target.value = "";
    }
  };

  const removeFile = (id: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== id));
  };

  // --- GitHub repo handlers ---
  const addGithubRepo = () => {
    setRepoInputError("");
    const parsed = parseGithubUrl(repoInput);

    if (!parsed) {
      setRepoInputError(
        "Enter a valid GitHub URL or owner/repo format (e.g. facebook/react-native)"
      );
      return;
    }

    const fullName = `${parsed.owner}/${parsed.name}`;
    if (githubRepos.some((r) => `${r.owner}/${r.name}` === fullName)) {
      setRepoInputError("This repository has already been added.");
      return;
    }

    const id = `repo-${Date.now()}`;
    const newRepo: GithubRepo = {
      id,
      url: `https://github.com/${parsed.owner}/${parsed.name}`,
      owner: parsed.owner,
      name: parsed.name,
      status: "pending",
      progress: 0,
    };
    setGithubRepos((prev) => [...prev, newRepo]);
    setRepoInput("");

    // Simulate scraping
    setTimeout(() => {
      setGithubRepos((prev) =>
        prev.map((r) => (r.id === id ? { ...r, status: "scraping" } : r))
      );

      let prog = 0;
      const interval = setInterval(() => {
        prog += Math.random() * 15 + 5;
        if (prog >= 100) {
          prog = 100;
          clearInterval(interval);
          setGithubRepos((prev) =>
            prev.map((r) =>
              r.id === id ? { ...r, status: "done", progress: 100 } : r
            )
          );
        } else {
          setGithubRepos((prev) =>
            prev.map((r) =>
              r.id === id ? { ...r, progress: Math.min(prog, 99) } : r
            )
          );
        }
      }, 500);
    }, 400);
  };

  const removeRepo = (id: string) => {
    setGithubRepos((prev) => prev.filter((r) => r.id !== id));
  };

  const runAnalysis = () => {
    setIsAnalyzing(true);
    setProgress(0);

    const stages = [
      { label: "Loading knowledge artifacts...", target: 15 },
      { label: "Processing uploaded files...", target: 30 },
      { label: "Extracting competencies from GitHub data...", target: 45 },
      { label: "Analyzing conference talks & podcasts...", target: 60 },
      { label: "Mapping skill dependencies...", target: 80 },
      { label: "Generating hiring pack...", target: 95 },
      { label: "Complete!", target: 100 },
    ];

    let i = 0;
    const interval = setInterval(() => {
      if (i < stages.length) {
        setAnalysisStage(stages[i].label);
        setProgress(stages[i].target);
        i++;
      } else {
        clearInterval(interval);
        setTimeout(onAnalysisComplete, 400);
      }
    }, 800);
  };

  const totalSources =
    selectedArtifacts.size +
    uploadedFiles.filter((f) => f.status === "done").length +
    githubRepos.filter((r) => r.status === "done").length;

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h2 className="text-2xl font-semibold text-foreground tracking-tight">
          Knowledge Intake
        </h2>
        <p className="text-muted-foreground mt-1">
          Select the departing team member, upload files, add GitHub repos, and
          select knowledge artifacts to analyze.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Person card */}
        <Card className="lg:col-span-1 border-primary/20 bg-card">
          <CardHeader>
            <CardTitle className="text-base">Departing Team Member</CardTitle>
            <CardDescription>Knowledge clone source</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center text-center">
              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-primary/10 border-2 border-primary/30 mb-4">
                <span className="text-2xl font-semibold text-primary">
                  {mike.avatar}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-foreground">
                {mike.name}
              </h3>
              <p className="text-sm text-muted-foreground mt-0.5">
                {mike.role}
              </p>

              <div className="mt-4 w-full space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Briefcase className="h-3.5 w-3.5 text-primary/60" />
                  <span>{mike.department}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-3.5 w-3.5 text-primary/60" />
                  <span>{mike.yearsAtCompany} years at company</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <FolderGit2 className="h-3.5 w-3.5 text-primary/60" />
                  <span>{mike.keyProjects.length} key projects</span>
                </div>
              </div>

              <div className="mt-4 flex flex-wrap gap-1.5 justify-center">
                {mike.keyProjects.map((project) => (
                  <Badge
                    key={project}
                    variant="secondary"
                    className="text-xs"
                  >
                    {project}
                  </Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Right column */}
        <div className="lg:col-span-2 space-y-6">
          {/* File Upload */}
          <Card className="bg-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Upload className="h-4 w-4 text-primary" />
                    Upload Files
                  </CardTitle>
                  <CardDescription>
                    Upload documents, transcripts, notes, or any knowledge
                    artifacts (PDF, MD, TXT, JSON, CSV)
                  </CardDescription>
                </div>
                {uploadedFiles.length > 0 && (
                  <Badge
                    variant="outline"
                    className="text-primary border-primary/30"
                  >
                    {uploadedFiles.filter((f) => f.status === "done").length}{" "}
                    file{uploadedFiles.filter((f) => f.status === "done").length !== 1 ? "s" : ""}
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {/* Drop zone */}
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                disabled={isAnalyzing}
                className={cn(
                  "w-full flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed p-6 transition-all cursor-pointer",
                  isDragOver
                    ? "border-primary bg-primary/10"
                    : "border-border hover:border-primary/40 hover:bg-primary/5",
                  isAnalyzing && "opacity-50 cursor-not-allowed"
                )}
              >
                <Upload
                  className={cn(
                    "h-6 w-6",
                    isDragOver ? "text-primary" : "text-muted-foreground"
                  )}
                />
                <div className="text-center">
                  <span className="text-sm text-primary font-medium">
                    Click to upload
                  </span>
                  <span className="text-sm text-muted-foreground">
                    {" "}
                    or drag and drop
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  PDF, MD, TXT, JSON, CSV, DOCX &mdash; up to 50 MB each
                </span>
              </button>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf,.md,.txt,.json,.csv,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.zip,.tar.gz"
                onChange={handleFileInput}
                className="hidden"
              />

              {/* Uploaded files list */}
              {uploadedFiles.length > 0 && (
                <div className="mt-4 space-y-2">
                  {uploadedFiles.map((file) => {
                    const Icon = getFileIcon(file.type);
                    return (
                      <div
                        key={file.id}
                        className="flex items-center gap-3 rounded-lg border border-border bg-secondary/20 p-3"
                      >
                        <div
                          className={cn(
                            "flex h-8 w-8 shrink-0 items-center justify-center rounded-md",
                            file.status === "done"
                              ? "bg-primary/15 text-primary"
                              : "bg-secondary text-muted-foreground"
                          )}
                        >
                          <Icon className="h-4 w-4" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between gap-2">
                            <span className="text-sm font-medium text-foreground truncate">
                              {file.name}
                            </span>
                            <div className="flex items-center gap-2 shrink-0">
                              {file.status === "uploading" && (
                                <span className="text-xs text-muted-foreground">
                                  {Math.round(file.progress)}%
                                </span>
                              )}
                              {file.status === "done" && (
                                <CheckCircle2 className="h-4 w-4 text-green-400" />
                              )}
                              <button
                                onClick={() => removeFile(file.id)}
                                className="text-muted-foreground hover:text-foreground transition-colors"
                              >
                                <X className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </div>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-xs text-muted-foreground">
                              {formatFileSize(file.size)}
                            </span>
                            {file.status === "uploading" && (
                              <div className="flex-1 h-1 rounded-full bg-secondary overflow-hidden max-w-[120px]">
                                <div
                                  className="h-full rounded-full bg-primary/60 transition-all"
                                  style={{ width: `${file.progress}%` }}
                                />
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          {/* GitHub Repos */}
          <Card className="bg-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base flex items-center gap-2">
                    <GitFork className="h-4 w-4 text-primary" />
                    GitHub Repositories
                  </CardTitle>
                  <CardDescription>
                    Add repositories to scrape PRs, commits, issues, and code
                    reviews
                  </CardDescription>
                </div>
                {githubRepos.length > 0 && (
                  <Badge
                    variant="outline"
                    className="text-primary border-primary/30"
                  >
                    {githubRepos.filter((r) => r.status === "done").length}{" "}
                    repo{githubRepos.filter((r) => r.status === "done").length !== 1 ? "s" : ""}
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {/* Input */}
              <div className="flex gap-2">
                <div className="flex-1 relative">
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                    <Link className="h-4 w-4" />
                  </div>
                  <input
                    type="text"
                    value={repoInput}
                    onChange={(e) => {
                      setRepoInput(e.target.value);
                      setRepoInputError("");
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault();
                        addGithubRepo();
                      }
                    }}
                    placeholder="facebook/react-native or https://github.com/owner/repo"
                    disabled={isAnalyzing}
                    className={cn(
                      "w-full rounded-lg border bg-secondary/30 px-3 py-2.5 pl-9 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring/30 focus:border-primary/40 transition-all",
                      repoInputError ? "border-red-500/50" : "border-border"
                    )}
                  />
                </div>
                <Button
                  onClick={addGithubRepo}
                  disabled={!repoInput.trim() || isAnalyzing}
                  variant="outline"
                  className="shrink-0 border-primary/30 text-primary hover:bg-primary/10 hover:text-primary"
                >
                  <Plus className="mr-1.5 h-4 w-4" />
                  Add
                </Button>
              </div>
              {repoInputError && (
                <p className="text-xs text-red-400 mt-1.5">{repoInputError}</p>
              )}

              {/* Repos list */}
              {githubRepos.length > 0 && (
                <div className="mt-4 space-y-2">
                  {githubRepos.map((repo) => (
                    <div
                      key={repo.id}
                      className="flex items-center gap-3 rounded-lg border border-border bg-secondary/20 p-3"
                    >
                      <div
                        className={cn(
                          "flex h-8 w-8 shrink-0 items-center justify-center rounded-md",
                          repo.status === "done"
                            ? "bg-primary/15 text-primary"
                            : repo.status === "scraping"
                              ? "bg-primary/10 text-primary"
                              : "bg-secondary text-muted-foreground"
                        )}
                      >
                        <GitBranch className="h-4 w-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <div className="flex items-center gap-2 min-w-0">
                            <span className="text-sm font-medium text-foreground truncate">
                              {repo.owner}/{repo.name}
                            </span>
                            {repo.status === "scraping" && (
                              <Badge
                                variant="secondary"
                                className="text-[10px] gap-1"
                              >
                                <Loader2 className="h-2.5 w-2.5 animate-spin" />
                                Scraping
                              </Badge>
                            )}
                            {repo.status === "pending" && (
                              <Badge
                                variant="secondary"
                                className="text-[10px]"
                              >
                                Queued
                              </Badge>
                            )}
                          </div>
                          <div className="flex items-center gap-2 shrink-0">
                            {repo.status === "done" && (
                              <CheckCircle2 className="h-4 w-4 text-green-400" />
                            )}
                            <button
                              onClick={() => removeRepo(repo.id)}
                              className="text-muted-foreground hover:text-foreground transition-colors"
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        </div>
                        {repo.status === "scraping" && (
                          <div className="mt-1.5">
                            <div className="h-1 rounded-full bg-secondary overflow-hidden max-w-[200px]">
                              <div
                                className="h-full rounded-full bg-primary/60 transition-all"
                                style={{ width: `${repo.progress}%` }}
                              />
                            </div>
                            <span className="text-[10px] text-muted-foreground mt-0.5 block">
                              Fetching PRs, commits, reviews...
                            </span>
                          </div>
                        )}
                        {repo.status === "done" && (
                          <span className="text-xs text-muted-foreground">
                            PRs, commits, issues, and reviews scraped
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Pre-loaded Artifacts */}
          <Card className="bg-card">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base">
                    Pre-loaded Artifacts
                  </CardTitle>
                  <CardDescription>
                    {selectedArtifacts.size} of {artifacts.length} sources
                    selected
                  </CardDescription>
                </div>
                <Badge
                  variant="outline"
                  className="text-primary border-primary/30"
                >
                  {artifacts
                    .reduce((sum, a) => sum + a.items, 0)
                    .toLocaleString()}{" "}
                  items
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 sm:grid-cols-2">
                {artifacts.map((artifact) => {
                  const Icon = artifactIcons[artifact.type];
                  const isSelected = selectedArtifacts.has(artifact.id);

                  return (
                    <button
                      key={artifact.id}
                      onClick={() => toggleArtifact(artifact.id)}
                      disabled={isAnalyzing}
                      className={cn(
                        "flex items-start gap-3 rounded-lg border p-3 text-left transition-all",
                        isSelected
                          ? "border-primary/30 bg-primary/5"
                          : "border-border bg-secondary/30 opacity-50",
                        !isAnalyzing && "hover:border-primary/40"
                      )}
                    >
                      <div
                        className={cn(
                          "flex h-9 w-9 shrink-0 items-center justify-center rounded-md",
                          isSelected
                            ? "bg-primary/15 text-primary"
                            : "bg-secondary text-muted-foreground"
                        )}
                      >
                        <Icon className="h-4 w-4" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-sm font-medium text-foreground truncate">
                            {artifact.name}
                          </span>
                          {isSelected && (
                            <CheckCircle2 className="h-4 w-4 text-primary shrink-0" />
                          )}
                        </div>
                        <div className="flex items-center gap-2 mt-0.5">
                          <span className="text-xs text-muted-foreground">
                            {artifact.items} items
                          </span>
                          <span className="text-xs text-muted-foreground/50">
                            &bull;
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {artifact.size}
                          </span>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Run Analysis */}
          <Card className="bg-card border-primary/20">
            <CardContent className="py-5">
              {!isAnalyzing ? (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">
                      Total sources ready:
                    </span>
                    <span className="font-medium text-foreground">
                      {totalSources} source{totalSources !== 1 ? "s" : ""}
                      {uploadedFiles.filter((f) => f.status === "uploading")
                        .length > 0 && (
                          <span className="text-muted-foreground font-normal ml-1">
                            ({uploadedFiles.filter((f) => f.status === "uploading").length} uploading...)
                          </span>
                        )}
                    </span>
                  </div>
                  <Separator />
                  <Button
                    onClick={runAnalysis}
                    disabled={
                      totalSources === 0 ||
                      uploadedFiles.some((f) => f.status === "uploading") ||
                      githubRepos.some((r) => r.status === "scraping" || r.status === "pending")
                    }
                    className="w-full bg-primary text-primary-foreground hover:bg-primary/90 h-11"
                    size="lg"
                  >
                    <Play className="mr-2 h-4 w-4" />
                    Run Analysis
                    <span className="ml-2 text-xs opacity-70">
                      ({totalSources} sources)
                    </span>
                  </Button>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                    <span className="text-sm text-foreground">
                      {analysisStage}
                    </span>
                  </div>
                  <Progress value={progress} className="h-2" />
                  <p className="text-xs text-muted-foreground text-right">
                    {progress}%
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Info section */}
      <Card className="bg-card border-border">
        <CardContent className="py-4">
          <div className="flex items-start gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
              <User className="h-4 w-4" />
            </div>
            <div>
              <p className="text-sm text-foreground font-medium">How it works</p>
              <p className="text-sm text-muted-foreground mt-0.5">
                Gemellus analyzes all provided sources &mdash; uploaded files,
                scraped GitHub repos, and pre-loaded artifacts &mdash; using
                Gemini's 2M token context window. It extracts competencies,
                communication patterns, and institutional knowledge to generate
                an evidence-backed hiring pack.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
