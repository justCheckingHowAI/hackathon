# Testing Your React Native Apps: Definitive Guide to a Bug-less Experience

**Author:** Mike Grabowski | **Publication:** Callstack Engineers | **Date:** May 3, 2016

## Introduction

React development benefits from having a single target environment: the browser. React Native introduces significantly greater complexity due to its multi-platform nature, requiring testing strategies for web, iOS, Android, and Windows. This guide focuses on iOS snapshot testing using React Native's testing framework.

## What Are Snapshots?

Screenshot testing compares reference images stored locally against your app's current visual state. When differences appear, tests fail. This approach proved invaluable when React Native released an update that subtly altered `<ListView />` rendering with different margins, breaking numerous layouts. Snapshot testing prevents such issues from going undetected.

## Implementation Steps

### Step 1: Create a Test Target
Navigate to File → New → Target and select iOS Unit Testing Bundle from the Test section.

### Step 2: Link RCTTest
Link React Native's RCTTest module to your test target through manual linking.

### Step 3: Configure the Test Runner
Add a private `_runner` property of type `RCTTestRunner` and initialize it in setUp.

### Step 4: Write Your First Test
Add a test method that executes your component.

### Step 5: Run Tests
Initially tests fail because no reference image exists yet.

### Step 6: Record Snapshots
Change `recordMode` to `YES` and run tests again. The system captures snapshots and stores them.

## Advanced Techniques

### Adjusting Snapshot Dimensions
Customize snapshot size to test different device dimensions.

### Mocking Data
Pass custom props to components during testing to test various states.

## Conclusion

Snapshot testing provides a straightforward mechanism for detecting unintended UI changes across React Native platforms.
