export interface Person {
  id: string;
  name: string;
  role: string;
  avatar: string;
  department: string;
  yearsAtCompany: number;
  keyProjects: string[];
}

export interface Skill {
  name: string;
  level: "expert" | "advanced" | "intermediate";
  evidence: string[];
  category: string;
}

export interface ScoreCardItem {
  criterion: string;
  weight: number;
  description: string;
}

export interface HiringPack {
  person: Person;
  skills: Skill[];
  gapSummary: string;
  recommendedRole: {
    title: string;
    description: string;
    seniority: string;
  };
  scorecard: ScoreCardItem[];
  interviewQuestions: { question: string; category: string }[];
  mustHave: string[];
  niceToHave: string[];
  redFlags: string[];
}

export interface CandidateResult {
  name: string;
  matchScore: number;
  strengths: string[];
  gaps: string[];
  fitSummary: string;
  criteriaScores: { criterion: string; score: number; maxScore: number }[];
}

export interface Artifact {
  id: string;
  name: string;
  type: "github" | "transcript" | "documentation" | "slack" | "synthetic";
  size: string;
  items: number;
}

export const mike: Person = {
  id: "mike-grabowski",
  name: "Mike Grabowski",
  role: "Senior React Native Engineer & OSS Lead",
  avatar: "MG",
  department: "Engineering",
  yearsAtCompany: 6,
  keyProjects: [
    "React Native CLI",
    "Re.Pack (Webpack for RN)",
    "React Native Paper",
    "Hermes Engine Integration",
  ],
};

export const artifacts: Artifact[] = [
  {
    id: "github",
    name: "GitHub Activity",
    type: "github",
    size: "2.4 MB",
    items: 847,
  },
  {
    id: "talks",
    name: "Conference Talks",
    type: "transcript",
    size: "1.1 MB",
    items: 12,
  },
  {
    id: "podcast",
    name: "Podcast Episodes",
    type: "transcript",
    size: "890 KB",
    items: 5,
  },
  {
    id: "docs",
    name: "Technical Documentation",
    type: "documentation",
    size: "3.2 MB",
    items: 15,
  },
  {
    id: "slack",
    name: "Slack Conversations",
    type: "slack",
    size: "540 KB",
    items: 234,
  },
  {
    id: "synthetic",
    name: "1:1 Notes & Jira",
    type: "synthetic",
    size: "180 KB",
    items: 42,
  },
];

export const hiringPack: HiringPack = {
  person: mike,
  skills: [
    {
      name: "React Native Core",
      level: "expert",
      category: "Technical",
      evidence: [
        'PR #2847: "Refactored the native modules bridge to support async initialization" — React Native CLI',
        'Talk at React Native EU 2024: "Deep dive into the new architecture and how we migrated 200+ modules"',
        "Maintained react-native-cli with 12k+ GitHub stars",
      ],
    },
    {
      name: "Build Systems & Tooling",
      level: "expert",
      category: "Technical",
      evidence: [
        "Created Re.Pack — Webpack toolkit for React Native, enabling code splitting and module federation",
        'PR #156: "Implemented tree-shaking for native modules in Re.Pack v3"',
        "Podcast Ep. 12: Explained custom Metro transformer architecture decisions",
      ],
    },
    {
      name: "JavaScript Engine Integration",
      level: "advanced",
      category: "Technical",
      evidence: [
        'Medium post: "Integrating Hermes engine on iOS — lessons learned from profiling startup time"',
        'PR #4521: "Added Hermes bytecode precompilation to CLI build step"',
      ],
    },
    {
      name: "Open Source Leadership",
      level: "expert",
      category: "Leadership",
      evidence: [
        "Managed 50+ contributors across React Native CLI and Re.Pack",
        "Reactiflux Q&A: Consistently helped community members debug native module issues",
        '1:1 Notes: "Mike mentors 3 junior devs on OSS contribution best practices"',
      ],
    },
    {
      name: "Architecture Design",
      level: "advanced",
      category: "Technical",
      evidence: [
        'Talk: "Designing plugin architectures for React Native tooling"',
        "Docs: Authored autolinking specification and configuration API",
        'Slack: Led discussion on modular architecture for monorepo migration',
      ],
    },
    {
      name: "Native Modules (iOS/Android)",
      level: "advanced",
      category: "Technical",
      evidence: [
        "Docs: Authored native modules introduction and Turbo Modules migration guide",
        'PR #891: "Bridged native camera module with new architecture support"',
      ],
    },
  ],
  gapSummary:
    "Mike's departure creates critical gaps in React Native build tooling ownership (Re.Pack, CLI), JavaScript engine integration expertise, and open-source community leadership. The team loses its primary architecture decision-maker for cross-platform tooling and the main bridge between the React Native core team and the broader OSS community. No current team member has equivalent depth in build system internals or native module bridging.",
  recommendedRole: {
    title: "Staff React Native Platform Engineer",
    description:
      "Own React Native build infrastructure, native module architecture, and developer tooling. Lead the OSS community engagement for internal frameworks. Drive architectural decisions for cross-platform tooling and ensure smooth migration paths for the new React Native architecture.",
    seniority: "Staff / Principal",
  },
  scorecard: [
    {
      criterion: "React Native internals & new architecture",
      weight: 0.25,
      description:
        "Deep understanding of Fabric, TurboModules, and the JSI bridge. Can debug native crashes and performance issues at the engine level.",
    },
    {
      criterion: "Build tooling & bundler expertise",
      weight: 0.2,
      description:
        "Experience with Metro, Webpack, or custom bundlers for mobile. Understands code splitting, tree-shaking, and bytecode compilation.",
    },
    {
      criterion: "Open source leadership",
      weight: 0.2,
      description:
        "Track record maintaining popular OSS projects. Can manage community contributions, triage issues, and drive roadmap decisions publicly.",
    },
    {
      criterion: "Native platform knowledge (iOS + Android)",
      weight: 0.15,
      description:
        "Comfortable writing and debugging native modules in Swift/ObjC and Kotlin/Java. Understands platform-specific build systems (Gradle, CocoaPods).",
    },
    {
      criterion: "Architecture & system design",
      weight: 0.1,
      description:
        "Can design plugin systems, define API contracts, and make trade-offs for long-lived developer tools.",
    },
    {
      criterion: "Mentorship & technical communication",
      weight: 0.1,
      description:
        "Writes clear technical docs, gives internal/external talks, and mentors junior engineers effectively.",
    },
  ],
  interviewQuestions: [
    {
      question:
        "Walk us through how you'd debug a React Native app that crashes on startup only on Android 12+ devices after enabling the new architecture. What tools and steps would you use?",
      category: "React Native Internals",
    },
    {
      question:
        "You need to implement code splitting for a React Native app with 50+ feature modules. How would you approach this, and what are the trade-offs vs. a single bundle?",
      category: "Build Tooling",
    },
    {
      question:
        "Describe a time you made a controversial technical decision in an open-source project. How did you communicate it to the community and handle pushback?",
      category: "OSS Leadership",
    },
    {
      question:
        "Design a native module that provides a unified API for biometric authentication across iOS (Face ID, Touch ID) and Android (BiometricPrompt). How would you handle platform differences?",
      category: "Native Modules",
    },
    {
      question:
        "An OSS contributor submits a large PR that refactors your project's plugin system. The code works but changes the public API. How do you handle this?",
      category: "OSS Leadership",
    },
    {
      question:
        "You're tasked with reducing the JS bundle startup time by 40%. Where do you start, and what metrics do you track?",
      category: "Performance",
    },
  ],
  mustHave: [
    "3+ years hands-on React Native experience (not just React)",
    "Experience with native module development (iOS or Android)",
    "Track record in build tooling or developer experience",
    "Published OSS work or significant contributions to major projects",
    "Strong written and verbal communication skills",
  ],
  niceToHave: [
    "Experience with Hermes or other JS engines (V8, JSC internals)",
    "Knowledge of Module Federation or micro-frontend patterns",
    "Conference speaking experience",
    "Experience managing a team of 3+ engineers",
    "Rust or C++ for performance-critical native modules",
  ],
  redFlags: [
    "Only web React experience — no native mobile background",
    "No open-source contributions or community involvement",
    "Cannot explain build pipeline beyond 'npm run build'",
    "Dismissive of backward compatibility and migration paths",
    "No experience working asynchronously with distributed teams",
  ],
};

export const candidateResult: CandidateResult = {
  name: "Alex Chen",
  matchScore: 78,
  strengths: [
    "Strong React Native experience (4 years), including Fabric migration",
    "Maintained 2 popular RN libraries (3k+ combined GitHub stars)",
    "Excellent communication — gave 3 conference talks on mobile performance",
    "Experience with custom Metro plugins and bundle optimization",
  ],
  gaps: [
    "Limited experience with Webpack/Re.Pack — primarily Metro-focused",
    "No direct Hermes engine integration work",
    "Has led community contributions but not managed a full OSS project lifecycle",
  ],
  fitSummary:
    "Alex is a strong candidate who covers ~78% of the identified competency gap. Their React Native depth and community involvement align well with the role. The main development areas are build tooling breadth (Webpack/Re.Pack) and JS engine internals, both of which are learnable given their strong foundations. Recommended for final round with a focus on architecture design assessment.",
  criteriaScores: [
    {
      criterion: "React Native internals & new architecture",
      score: 9,
      maxScore: 10,
    },
    {
      criterion: "Build tooling & bundler expertise",
      score: 6,
      maxScore: 10,
    },
    { criterion: "Open source leadership", score: 7, maxScore: 10 },
    {
      criterion: "Native platform knowledge (iOS + Android)",
      score: 8,
      maxScore: 10,
    },
    { criterion: "Architecture & system design", score: 7, maxScore: 10 },
    {
      criterion: "Mentorship & technical communication",
      score: 9,
      maxScore: 10,
    },
  ],
};
