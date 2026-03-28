# Technical Guide, Part 2: Integrating Hermes with React Native

**By Mike Grabowski | Callstack Engineers | August 16, 2021**

## Overview

React Native 0.64 introduced support for the Hermes engine on iOS, resulting from collaborative work between Callstack, Facebook, and Microsoft teams.

## Integration Process

### Starting Point
React Native requires a JSExecutor instance to run JavaScript code. Previously, JSCExecutor handled this using JavaScript Core. Now, HermesExecutor provides an alternative using the Hermes engine.

The core React Native code is written in C++, enabling code sharing between Android and iOS platforms.

### Activation Method
Enabling Hermes requires minimal developer effort—just one step. In your Podfile's `use_react_native` function, set `hermes_enabled: true`, then run `pod install`.

### Technical Implementation
A macro sets the `RCT_USE_HERMES` project-wide variable when Hermes headers are included. This allows conditional imports and executor factory initialization based on Hermes availability.

RCTCxxBridge selects the appropriate executor factory depending on Hermes availability, with no additional architecture changes needed.

## Practical Results
Applications automatically detect and display Hermes engine information. Since `<NewAppScreen>` is cross-platform and already runs on Android with Hermes, iOS components recognize the engine without modification.
