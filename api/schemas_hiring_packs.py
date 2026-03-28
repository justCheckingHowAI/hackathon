from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HiringPackPerson(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: str
    name: str
    role: str
    avatar: str
    department: str
    yearsAtCompany: int
    keyProjects: list[str]


class HiringPackSkill(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    level: str
    evidence: list[str]
    category: str


class HiringPackRecommendedRole(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: str
    description: str
    seniority: str


class HiringPackScorecardItem(BaseModel):
    model_config = ConfigDict(extra='forbid')

    criterion: str
    weight: float
    description: str


class HiringPackInterviewQuestion(BaseModel):
    model_config = ConfigDict(extra='forbid')

    question: str
    category: str


class HiringPack(BaseModel):
    model_config = ConfigDict(extra='forbid')

    person: HiringPackPerson
    skills: list[HiringPackSkill]
    gapSummary: str
    recommendedRole: HiringPackRecommendedRole
    scorecard: list[HiringPackScorecardItem]
    interviewQuestions: list[HiringPackInterviewQuestion]
    mustHave: list[str]
    niceToHave: list[str]
    redFlags: list[str]
