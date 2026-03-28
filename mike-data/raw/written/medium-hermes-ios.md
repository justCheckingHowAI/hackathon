# Bringing Hermes to iOS in React Native 0.64

**Author:** Mike Grabowski | **Publication:** Callstack Engineers

## Introduction

"For a long time Hermes was exclusive to Android" but is now available on iOS as well. Callstack collaborated with Facebook and Microsoft teams to bring this JavaScript engine to Apple's platform as part of React Native 0.64.

## What is a JavaScript Engine?

A JavaScript engine executes application code and performs desired actions. Traditional engines optimize for web browsers and interactive websites, which differ significantly from mobile applications.

## React Native vs. Web Applications

React Native applications differ fundamentally from web apps. Rather than using HTML, CSS, and DOM interactions, "native code is shipped for both iOS and Android, respectively" to render elements and handle user interactions. Mobile users demand faster performance than web users, creating distinct optimization challenges.

## Why Hermes Matters

Facebook created Hermes specifically for React Native. The key distinction: "Hermes is an AOT engine" (Ahead-of-Time), meaning it compiles JavaScript during build time rather than at runtime. This shift eliminates parsing overhead when apps launch.

Android results showed significant improvements in startup times, CPU consumption, and memory usage, though iOS results may differ.

## Bringing Hermes to iOS

Using identical engines across platforms enables developers to "fully embrace its features" and reduces platform-specific bugs. Both platforms initially used JavaScriptCore, but Hermes' success on Android warranted iOS support.

## Technical Considerations

Apple restricts JIT engines, but "Hermes is an AOT engine, these restrictions do not apply." However, shipping a custom engine increases app size since it cannot rely on the built-in system engine.

## Availability and Testing

"Hermes is now available under a flag on iOS, starting from React Native 0.64." Benchmarks indicate performance improvements, though developers should evaluate tradeoffs independently.
