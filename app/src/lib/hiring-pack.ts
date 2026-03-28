import { API_URL } from "@/lib/api";

export interface HiringPackPerson {
  id: string;
  name: string;
  role: string;
  avatar: string;
  department: string;
  yearsAtCompany: number;
  keyProjects: string[];
}

export interface HiringPackSkill {
  name: string;
  level: "expert" | "advanced" | "intermediate";
  evidence: string[];
  category: string;
}

export interface HiringPackScoreCardItem {
  criterion: string;
  weight: number;
  description: string;
}

export interface HiringPackRecommendedRole {
  title: string;
  description: string;
  seniority: string;
}

export interface HiringPackInterviewQuestion {
  question: string;
  category: string;
}

export interface HiringPack {
  person: HiringPackPerson;
  skills: HiringPackSkill[];
  gapSummary: string;
  recommendedRole: HiringPackRecommendedRole;
  scorecard: HiringPackScoreCardItem[];
  interviewQuestions: HiringPackInterviewQuestion[];
  mustHave: string[];
  niceToHave: string[];
  redFlags: string[];
}

export class HiringPackNotFoundError extends Error {
  constructor(message = "Hiring pack not found.") {
    super(message);
    this.name = "HiringPackNotFoundError";
  }
}

export async function fetchHiringPack(
  personId: string,
  signal?: AbortSignal,
): Promise<HiringPack> {
  const response = await fetch(
    `${API_URL}/hiring-packs/${encodeURIComponent(personId)}`,
    { signal },
  );

  if (response.status === 404) {
    throw new HiringPackNotFoundError();
  }

  if (!response.ok) {
    throw new Error("Could not load hiring pack from the server.");
  }

  return (await response.json()) as HiringPack;
}
