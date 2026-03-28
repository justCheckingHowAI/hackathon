# 1:1 Notes - Mike & Board/Advisor

## 2025-01-13

**Mike's updates:**
- React Summit talk accepted for June. Topic: Cross-platform Module Federation.
  Preparing demo with real client codebase (anonymized).
- Re.Pack adoption growing - 3 new enterprise clients this quarter.
  Main blocker for adoption is still Hermes compatibility with dynamic imports.
- Concerned about CLI maintenance burden. Community CLI has 200+ open issues
  and we're the primary maintainers. Need to hire dedicated person or find
  more community contributors.
- callstackincubator/ai getting traction. On-device LLM demo impressed
  potential client in healthcare (privacy requirements = no cloud inference).

**Action items:**
- Mike: Draft blog post about Module Federation use cases (deadline: Jan 31)
- Mike: Start hiring process for Senior RN Tooling Engineer
- Mike: Review AI incubator roadmap for Q2

**Personal notes:**
- Mike prefers async communication. Best way to reach: Slack DM or GitHub mention.
- Most productive in mornings (before noon CET).
- Gets frustrated by feature requests without clear use cases.
- Energized by conference prep - uses talks as forcing function for shipping features.

---

## 2025-02-10

**Mike's updates:**
- Auto-linking bug with New Architecture was critical - fixed in 2 days.
  This highlighted a gap: our autolinking tests don't cover TurboModule scenarios.
  Added to Q2 testing backlog.
- Re.Pack Hermes compat layer prototype working. Performance is acceptable
  but memory usage needs optimization. Targeting March for beta.
- Blog post published. Got picked up by React Native newsletter - good visibility.
- Hiring: received 40 applications for tooling engineer role. Only 3 have
  relevant bundler experience. This confirms it's a niche skillset.

**Discussion: Open Source Strategy**
Mike's perspective on OS at Callstack:
"Our open source work is our best marketing and hiring pipeline. React Native Paper
has 13k stars and brings us enterprise leads every month. Re.Pack is smaller but
the clients it attracts are higher value - they're building serious production apps.
The key is maintaining quality - a buggy OS project hurts our brand more than
having no project at all."

**Action items:**
- Mike: Finalize Hermes compat beta by March 15
- Mike: Interview top 3 candidates for tooling role
- Mike: Write ADR for Metro vs Re.Pack recommendation

---

## 2025-03-03

**Mike's updates:**
- Hermes compat beta shipped on schedule. Two enterprise clients testing.
  One found edge case with large chunk sizes (>2MB) causing OOM on older devices.
  Working on lazy chunk loading as mitigation.
- Tooling engineer interviews: found a strong candidate with webpack core experience.
  Making offer this week.
- Next-gen CLI prototype at dev.grabbou.xyz getting attention on Twitter.
  Community reaction positive but some concerns about backward compat.
- React Summit demo prep: building live Super App demo with shared shopping cart
  module between web and RN. The "wow moment" will be: change code in web app,
  see it reflected in mobile app in real-time via Module Federation.

**Discussion: Knowledge Transfer**
"I realize I'm a single point of failure for too many things: CLI architecture,
Re.Pack internals, auto-linking logic, release process. We need to document
more of the 'why' behind decisions, not just the 'what'. I'm going to start
writing ADRs for major decisions and recording short video walkthroughs
of complex subsystems."

**Action items:**
- Mike: Record video walkthrough of auto-linking internals
- Mike: Write ADR: Metro vs Re.Pack
- Mike: Finalize React Summit demo
- Mike: Onboard new tooling engineer (start date: April 1)

---

## 2025-03-17

**Mike's updates:**
- New tooling engineer accepted offer. Starts April 1. First project:
  take over CLI issue triage and patch releases.
- Large chunk OOM fix shipped. Solution: progressive chunk loading with
  configurable max concurrent fetches. Defaulting to 3 concurrent chunks
  on devices with <4GB RAM.
- React Summit demo working end-to-end. The shared cart module loads
  correctly on both web and RN with real-time updates.
- callstackincubator/ai: published as npm package. First external contributor
  submitted PR for Android support (was iOS only).

**Discussion: If Mike left tomorrow**
Board asked Mike to think about bus factor mitigation:
"Honestly, the biggest risk areas are:
1. Re.Pack runtime internals - only I fully understand the chunk loading mechanism
2. Auto-linking architecture - I wrote the original design, it's evolved a lot
3. Relationship with Meta's RN team - I have direct contacts for escalation
4. Release process tribal knowledge - not documented well enough

The new tooling engineer will help with #2 and #4. For #1, I need to write
comprehensive architecture docs. For #3, we need to introduce more team members
to the Meta relationship."

**Action items:**
- Mike: Write Re.Pack architecture deep-dive doc
- Mike: Introduce 2 team members to Meta RN contacts
- Mike: Prepare knowledge transfer plan for top 5 critical areas
