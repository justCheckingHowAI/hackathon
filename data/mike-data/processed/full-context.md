# TeamTwin Knowledge Base - Mike Grabowski (@grabbou)
## CTO & Co-Founder, Callstack | React Native Core Team

---

## GITHUB PROFILE

{
  "bio": "Passionate about cross platform technologies. When not working, find me on a race track.",
  "blog": "",
  "company": "@callstack",
  "created_at": "2012-10-01T16:10:34Z",
  "followers": 1785,
  "following": 8,
  "location": "\ud83c\uddf5\ud83c\uddf1 / \ud83c\uddfa\ud83c\uddf8",
  "login": "grabbou",
  "name": "Mike",
  "public_repos": 101
}

---

## PULL REQUESTS AUTHORED (185 total)

### PR: feat(ios): ability to link local spm packages
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/54405
Description: ## Summary:

While working on local project in monorepo, I found that `spm_dependency` utility available in CocoaPods does not support local SPM packages, assuming they always come from remote.

This change extends it so that `url` can also be a local path:

```ruby
  spm_dependency(s,
    url: File.join(__dir__, 'shared'),
    requirement: {},
    products: ['FooModule']
  )
```

In the above example, `shared` folder contains a SPM project.

I don't have opinions on the API design here, I am also happy to create `spm_local_dependency` utility in order to clean up the API desig
  Comment by @react-native-bot: 
<!--
  1 failure:  :clipboard: Verif...
  0 warning: 
  
  
  DangerID: danger-id-Danger;
-->

<table>
  <thead>
    <tr>
      <th width="50"></th>
      <th width="100%" data-danger-table="true">Fails</th>
    </tr>
  </thead>
  <tbody><tr>
      
  Comment by @meta-codesync[bot]: @sbuggay has **imported** this pull request. If you are a Meta employee, you can view this in [D86212929](https://www.internalfb.com/diff/D86212929).
  Comment by @meta-codesync[bot]: This pull request has been merged in facebook/react-native@d31fc328826a584a2351acf831ee987846ca7e21.

### PR: fix: React Native CodeGen integration for 0.64-stable
Repo: facebook/react-native | State: merged | URL: https://github.com/facebook/react-native/pull/31027
Description: ## Summary

This PR resolves issues reported in the 0.64.0 release candidate around CodeGen. Further reading here: https://github.com/react-native-community/releases/issues/214#issuecomment-783363624

  Review on package.json: Note: On 0.64-stable branch, React Native will always use CodeGen from `npm`, even when running from RNTester. 

I wish we had Yarn Workspaces set up right, that way, I could point here to use local version of CodeGen when running from this reposit
  Review on scripts/generate-specs.sh: One thing that I just realised is that you won't be able to set this unless the Script Phase is part of a user project. Right now, it's inside `FBReactNativeSpec` target.

So, I will most likely drop it.

### PR: Exclude `i386` from valid architectures when building with Hermes on iOS
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30592
Description: ## Summary

When building React Native application in Release mode for an iPhone Simulator _and_ targeting `armv7`, Xcode will build all architectures (due to `ONLY_ACTIVE_ARCH` set to `false`, unlike in Debug mode). As a result, Xcode will try building for `i386` (32-bit iPhone Simulator), which fails as we don’t build Hermes binaries for `i386`.

Fix is to disable `i386`, since it is not supported by `Hermes` and certain `Folly` features.

## Changelog

[IOS] [BREAKING] - `i386` architecture will be automatically disabled when Hermes is being used. This might be potentially breaking 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **42dde12aac81208c4e69da991f4e08b9e62d18f6**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Review on template/ios/Podfile: FWIW, I could detect when `flipper_post_install` is placed in a user `Podfile` and print a warning that this is deprecated and one should place `react_native_post_install` instead.

Is it worth it?
  Review on template/ios/Podfile: (just thinking about potential users that might forget to update the `Podfile`)

### PR: fix: default template on iOS
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30571
Description: ## Summary

Recently introduced steps to run Hermes accidentally removed `!` from the `use_react_native`, causing `pod install` to fail with an error.

## Changelog

[INTERNAL] [iOS] - Fix Podfle in default template

## Test Plan

Run `pod install` with this file and it should work.

  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **e54ead6556f813fc622fd5e1f27ab2b41fa4f213**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: fix: building in release mode for simulator
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30543
Description: ## Summary

Fixes #29984

Right now, running a React Native application with Xcode 12 in Release mode on an iPhone Simulator will fail with something like below:

> [some file path], building for iOS Simulator, but linking in object file built for iOS, file '[some file path]' for architecture arm64

The best explanation of this issue has been provided by @alloy in #29984:

> This issue has started coming up with Xcode 12 and support for the new ARM based Macs, as `arm64` now no longer can be assumed to _only_ be for iOS devices. This means Xcode 12 will now also build for `arm64` sim
  Comment by @andreialecu: I'm on an M1 Mac Mini and if I add `arm64` to excluded architectures I'm getting this error right at the beginning of the build:

```
Module map file '/Users/.../Library/Developer/Xcode/DerivedData/MyApp-bmibskzjfhlxbsblspkqkqtndyjb/Build/Products
  Comment by @andreialecu: The error in the previous comment seems to go away if I change the deployment target to `11.0` from `10.0` (as per: https://github.com/facebook/react-native/issues/29605#issuecomment-701920944) but then I got this which is related to Flipper:

```
  Comment by @andreialecu: Also note that I'm not even attempting to run in `Release` mode, just `Debug` -> but I felt the PR was relevant.
  Review on scripts/react_native_pods.rb: I might be reading this wrong somehow, but isn't this `if` the wrong way around? 

Seems to exclude `arm64` when on `arm`.
  Review on scripts/react_native_pods.rb: Oh, true!

### PR: fix: release branches miss workspace dependencies
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30472
Description: ## Summary

On the CI, e.g. inside `publish-npm.js`, we're missing `shelljs` dependency, which comes from `repo-config` package. This error started happening after introduction of Yarn workspaces.

During `bump-oss-version.js`, [we remove `private` and `workspaces` settings](https://github.com/facebook/react-native/commit/0117077b9572f5b674578e19073e31e4693e9d41#diff-7ae45ad102eab3b6d7e7896acd08c427a9b25b346470d7bc6507b6481575d519L81-L84), preparing it for publishing. As a result, CI steps testing and running on `0.64-stable` branch can potentially fail due to missing dependencies.

Such
  Comment by @cpojer: This fix looks good to me. I can’t merge it at fb this week (holidaaays!) but if you make the same PR against the release branch I can merge that for now, then merge this PR into master later.
  Comment by @grabbou: Thanks @cpojer, that was fast! It's okay for now, I am going to test it that we indeed remove `package.json` properties as designed and get back to you before we do the next RC (that's best moment to test it).
  Comment by @cortinico: Closing as we now moved to a proper monorepo and there is no need to cleanup `package.json` anymore

### PR: fix: android artifacts in a release package
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30470
Description: ## Summary

Android artefacts in a release package are missing, as a result, users are not able to run `0.64.0-rc.0` on Android. Locally, everything works.

After several hours of testing, we found out that running `./gradlew ReactAndroid:installArchives` will "sometimes" fix it and I have managed to verify both locally and on the CI, that running Gradle without cache is broken, but when running Gradle once again (right after corrupted build completed, but there is cache already) fixes the issue.

Seems to be Gradle related.

In this PR, I am adding a validation to `publish-npm.js` scr
  Comment by @grabbou: Shipped `0.64.0-rc.1` with that script included, and everything works. Here's the output! https://app.circleci.com/pipelines/github/facebook/react-native/7266/workflows/58b22daf-d6db-41e2-a4bd-51ffad4e650c/jobs/178795

```
android/com/facebook/rea
  Comment by @cortinico: Thanks for sending the PR. I'm closing this as the logic is completely rewritten now.
  Review on scripts/publish-npm.js: `man unzip` says that the `-l` option can just list the contents, which would be a little easier. Also would it make sense to check for other files too?
  Review on scripts/publish-npm.js: I’d personally reserve ‘corruption’ for cases where the files are present but do not match expected contents. In this case the files are simply missing, so perhaps we can just say, which might be more helpful anyways to readers of this error in the f

### PR: fix: pin hermes-engine to 0.7.x
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30432
Description: ## Summary

Right now, Hermes is not pinned to any version and CocoaPods will install latest. This PR pins it using the same way Flipper is pinned, to keep it easier to track.

## Changelog

[INTERNAL] [IOS] - Pin Hermes on iOS
  Comment by @grabbou: In the future, we may consider letting users change the version, just like we do for Flipper. Right now, I don't see such requirement.
  Comment by @alloy: I'm going to pull this into 0.64-stable ahead of this being merged.
  Comment by @lunaleaps: @grabbou Do we still need this on main? Or can we close this? 

### PR: [INTERNAL] Test Hermes and RNTester on CircleCI
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/30300
Description: Opening as a follow up to #29914 to see if CircleCI will run tests here instead.

### PR: feat: Enable Hermes to work on iOS
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/29914
Description: ## Summary

This PR makes it possible to build iOS applications with Hermes. Note that it doesn't work with `use_frameworks!` just yet.
 
Fixes #27845 (by downgrading iOS deployment target for RCT-Folly to 9.0)
Fixes #28810 (as above)

Checklist:
- [x] Adjust release scripts to create Hermes bytecode bundle
- [x] Release new Hermes npm package that includes iOS files (unreleased right now, if you want to try locally, you have to clone Hermes and `yarn link` its master to this project)
- [x] Test on a new React Native application in both Debug and Release (Device)
- [x] Test on an RN
  Comment by @analysis-bot: | Platform | Engine | Arch | Size (bytes) | Diff |
|:---------|:-------|:-----|-------------:|-----:|
| android | hermes | arm64-v8a | 7,211,837 | -182,156 |
| android | hermes | armeabi-v7a | 6,861,013 | -156,200 |
| android | hermes | x86 | 7,646,4
  Comment by @grabbou: Thank you @alloy for your swift review, appreciate it! Now time to move it out of WIP stage 
  Comment by @elicwhite: This looks pretty good to me, except for the line endings (I think that's the problem) for `gradlew.bat`?
  Review on React-Core.podspec: I think since `hermes` dependency is always pulled from the local `npm` package, I don't think it makes sense to a) keep version requirement in two places and b) read a version from `package.json` here. The main reason against doing the latter is tha
  Review on React-Core.podspec: CC: @alloy

### PR: Update react.gradle
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28776
Description: ## Summary

Running `./gradlew assembleRelease` fails as the path to the CLI contains a new line at the end. We don't run this command in `debug` mode, hence it passed the testing. My bad.

Fixed, checked in both `debug` with `bundleInDebug: true` and `release`.

Fixes #28700 

## Changelog

[INTERNAL] [ANDROID] - Fix `React.gradle` to build Android apps in production

## Test Plan

Running `./gradlew assembleRelease` works

  Comment by @grabbou: FYI we took this code straight from the CLI where we use `Runtime.getRuntime().exec()` and that one seems to be handling whitespaces automatically, unlike `commandLine` from Gradle.
  Comment by @elicwhite: The CI jobs are failing because this branch was opened on the main repo. In the future, you'll be better off if you create branches on your fork instead. 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **afdcdc760f560963fdb48e409470d4119763d10b**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: chore: update `./scripts/test-manual-e2e.sh`
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28653
Description: ## Summary

Recent changes broke the script - wrong path to open `RNTesterPods.xcworkspace` and other scripts - we change dir with `cd`. 

Another change is incorrect use of `RNTesterProject.xcodeproj` instead of a `xcworkspace`. 

This PR is a simple and short fix to make it run.

## Changelog

[INTERNAL] - chore: update `./scripts/test-manual-e2e.sh`

## Test Plan

Run `./scripts/test-manual-e2e.sh`. Things work.

  Comment by @analysis-bot: | Platform | Engine | Arch | Size (bytes) | Diff |
|:---------|:-------|:-----|-------------:|-----:|
| android | hermes | arm64-v8a | 6,758,965 | 0 |
| android | hermes | armeabi-v7a | 6,406,021 | 0 |
| android | hermes | x86 | 7,140,385 | 0 |
| and
  Comment by @analysis-bot: | Platform | Engine | Arch | Size (bytes) | Diff |
|:---------|:-------|:-----|-------------:|-----:|
| ios | - | universal | n/a | -- |

Base commit: ddc33007ad0b4a0a24966b833e797227b9c56cca
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **90f60a83e3671655360806b48e1604cdebebeb6b**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: chore: remove Kotlin version from the default template
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28626
Description: ## Summary

The default application requires Kotlin version that is not supported by the Gradle plugin (should be at least `1.3.10`). However, instead of upgrading, we should remove it entirely. Here's why.

This commit https://github.com/facebook/react-native/commit/29d3dfbd196176af98c9727c82ff2668e697d78e introduced Detox for RNTester Android application.

Since the commit doesn't mention Detox for the default application and there are no Detox tests present by default in the default application, I believe that this addition was performed by a mistake.

The best way is to remove Kotl
  Comment by @grabbou: CC: @cs01 please correct me if I am wrong :)
  Comment by @cs01: Will Kotlin be available in the RNTester app still? There are Detox tests for RNTester that run for iOS, and that we'd like to have run for Android (with `yarn run detox test -c android.emu.debug` and `yarn run detox test -c android.emu.release`).
  Comment by @cs01: As long as `yarn run detox build -c android.emu.debug` and `yarn run detox build -c android.emu.release` still succeed I am fine with this.

### PR: fix: do not throw on missing `cliPath`, use the default value
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28625
Description: ## Summary

The `cliPath` has always been optional value and in fact, even had its default value hardcoded in the React gradle file.

In this PR, I am just taking use of it and remove throwing an error, which is going to be a really annoying breaking change.

## Changelog

[ANDROID] [INTERNAL] - Don't require `cliPath`

## Test Plan

Run Android project, everything works. 
Provide custom `cliPath`, it gets respected

  Comment by @grabbou: CC: @hramos @vdmtrv @Esemesek @thymikee 
  Comment by @grabbou: Next step would be to replace `defaultCliPath` with what we have done for React Native CLI already:
https://github.com/react-native-community/cli/blob/master/packages/platform-android/native_modules.gradle#L220-L222

In other words, run `console.l
  Comment by @grabbou: If `rootProject.projectDir` is defined here as well, then, we can use the same mechanism to learn about the path. This will be better than using hardcoded version, which isn't going to work in most cases.
  Review on react.gradle: shouldn't we distinguish between Windows and the rest here as well?
  Review on react.gradle: Yeah, probably, we need a bit more work here. @Esemesek 

### PR: chore: update CLI to the latest version
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28623
Description: ## Summary

Bumps CLI to the latest version, needed by https://github.com/facebook/react-native/pull/28572 to work.

## Changelog

[INTERNAL] - Bump CLI to latest

  Comment by @cpojer: Note: I won't be able to land this until ~Friday or so.
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **ddc33007ad0b4a0a24966b833e797227b9c56cca**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: Update default Podfile to not depend on a path
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28572
Description: ##  Summary

Recently, a default Podfile has been modified to not contain all the React Native pods, but use a helper method `use_react_native!`.

While this is great, it assumes a hardcoded path of `../node_modules/react-native` to be always the correct location of the React Native. 

https://github.com/facebook/react-native/blob/d4d8887b5018782eeb3f26efa85125e6bbff73e4/scripts/autolink-ios.rb#L7-L9

Unfortunately, due to the way Ruby works, this completely hides the path away from the users. 

Before, they could have seen the wrong path explicitly in a Podfile and knew to update it
  Comment by @grabbou: CC: @Esemesek @thymikee needs a CLI bump before being merged.
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **cd13c99d001d25296dcf991ea3cb32929d872102**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Comment by @grabbou: Note: this depends on https://github.com/react-native-community/cli/commit/c8bfdc690d501c149a8c9f57a064069a28d19537 that hasn't been released yet. We're doing that now.
  Review on template/ios/Podfile: I guess these `RNTestProject` strings should be reverted, right?
  Review on template/ios/Podfile: This extra line can be removed as well.

### PR: feat: improve monorepo support by removing redundant PROJECT_ROOT
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28354
Description: ## Summary

Historically, React Native didn't support a lot of custom project structures apart from the standard flat directory with `ios` and `android` folders. The CLI had to be explicitly started from the project root, otherwise Metro didn't work right.

In order to resolve the project root in the most accurate way, React Native assumed that project root is always `../../` from its location in `node_modules` - this is not true when the installation gets hoisted (e.g. in a monorepo).

To address that, @janicduplessis brought support for custom [`PROJECT_ROOT`](https://github.com/facebo
  Comment by @alloy: Nice one 👌 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **a8e85026cfa60056b1bcbcd39cde789e4d65f9cb**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Comment by @KingAmo: is there a guide on how to use monorepo with this pr ?
  Review on scripts/react-native-xcode.sh: I would remove this entirely, but I don't really want to run into all the users that have some crazy setup today. Historically, there was a lot of hacks around setting up monorepos and we're working with the CLI team to educate the developers that so
  Review on scripts/react-native-xcode.sh: I know this PR is old, but I believe we have a bug here. If `$PWD` is going to be the `ios` folder when this script is invoked from Xcode, then this line should be
```
PROJECT_ROOT=${PROJECT_ROOT:-$PWD/..}
```

cc @grabbou 

### PR: chore: Bump CLI to latest
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/28227
Description: ## Summary

Bump CLI to the latest version.

CC: @alloy @thymikee 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **e1de7a5e654f4cb1c08405f58c811a9f0074bb5c**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: Update integration snapshots
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/27059
Description: This commit https://github.com/facebook/react-native/commit/a397d330a4cf7e08095faa0e751e38d5106ed5c7 changes colors in the RNTester slightly and makes snapshots to fail.

I have re-generated them and made sure it was just the background color (and few other minor gray shades) that were different.

I haven't spotted any other visual changes.
  Comment by @grabbou: CC: @cpojer 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **2c7a907b08fabcd774e037c8f8e5a9d56c1c57e9**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: Revert "Set rounded rectangle mask on TouchableNativeFeedback's rippl…
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/26682
Description: This reverts commit 14b455f69a30d128db384749347f41b03b9a6000. Fixes #26544. Reopens #6480

## Summary

The commit introduced regression https://github.com/facebook/react-native/issues/26544. Rolling it back fixes the issue.

## Test Plan

Test plan is in the #26544, I have confirmed it to be working. You can render `borderRadius` with `elevation` and observe the glitch (on latest Android API).

  Comment by @ScreamZ: Ios ci is crying :(
  Comment by @grabbou: I don't think that would be related to this PR as it's Android only tho.
  Comment by @grabbou: Unfortunately, this PR hasn't been merged and looks like somebody commited a fix directly to mastr branch few days ago.

https://github.com/facebook/react-native/commit/1dc03f4858029c470dc769a7b49c5cbf75644bd7

Well... in this case, I will close 

### PR: feat: Do not require `pod install` after `react-native init`
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/24638
Description: ## Summary

This pull request pre-generates CocoaPods files by running `pod install` locally inside a `template` before we publish it.

## Rationale:

We have recently migrated default template from a regular iOS project to the one powered by CocoaPods. This was done to simplify set up required and make it easier to handle native modules in the future too.

Unfortunately, one drawback was that `pod install` was now going to be required to be run as an additional command, after `react-native init` has completed.

The detailed discussion and rationale can be found here: https://github.
  Comment by @grabbou: Big thanks to @orta for pointing me towards a solution - I would loose my mind if it wasn't for you <3
  Comment by @grabbou: Now that https://github.com/react-native-community/cli/pull/362 is going to be merged, I'll update the PR to always init from a tarball.

That way, we will be able to make sure that we test contents of a real package, not the source. This is import
  Comment by @thymikee: FYI putting `Pods` into the tarball increases its size by ~12MB (from ~3MB to ~15MB). Not cool, as it affects everybody, not only those who `init` new project. We'll need to move the template to a separate package in the monorepo. 
  Review on scripts/prepare-template.sh: `npm install` creates `package-lock.json` (it's in gitignore so you don't see it). Can we use Yarn instead (it's faster) and checkout `yarn.lock` along with `package.json`?
  Review on scripts/prepare-template.sh: I didn't go with `yarn` for two reasons:
- it has issues with cache when installing from a tarball - it will quickly eat up available space unless you `yarn cache clean` yourself
- we use `npm install` and `npm pack` already in other `scripts/*`, s

### PR: Use latest React Native CLI
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/24517
Description: ## Summary

Updates React Native to use latest CLI.

Changes:
- No more `--reactNativePath`, define it once in the configuration file. This reverts the previous PR that added this flag
- Add `platforms` and `commands` - React Native now defines platform like any other package. There's no longer concept of "out-of-tree" platform. All are treated equally. If React Native works, any other platform will work too.
- Updates `jest/hasteImpl.js` to use public CLI interface (`loadConfig`) instead of `findPlugins` and removes a weird conditional that checks for CI presence.

## Changelog

[I
  Comment by @grabbou: Let's merge it so it unblocks https://github.com/facebook/react-native/pull/24506
  Comment by @grabbou: Thanks @cpojer!

We will need to update the CLI dependency one more time, but RNTester works
w/o issues on master now, so that's good!

On Tue, 23 Apr 2019 at 11:15, Facebook Community Bot <
notifications@github.com> wrote:

> *@facebook-github-bot* 
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **706f67a882310ea5f43b2e000e0ebd15ae168e25**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Review on react-native.config.js: maybe let's be explicit about what we put here, because:
1) it will serve as a documentation
2) if we ever export some extra helpers from these modules, they won't break the configuration

so, even though more verbose, I'd expect:
```js
platfor
  Review on react-native.config.js: Yeah, good idea! Let me do that in a second.

### PR: [WIP] chore: Upgrade React Native CLI to 2.0.0-alpha.4
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/24338
Description: ## Summary

Upgrade React Native CLI to latest version that has a nice configuration interface so that we can avoid passing `reactNativePath` all the time.

This fixes Metro not starting properly in some cases, especially when we can't set this command (e.g. launchPackager.command).

This is WIP. Need to release 2.0.0-alpha.5 and then, update again.

  Comment by @grabbou: This reverts temporary workaround shipped with https://github.com/facebook/react-native/commit/5558333c60c75b1ac68f3e248d2d393ec09e8c8a
  Comment by @cpojer: Let me know once it is ready to be shipped.
  Comment by @grabbou: Will reopen.

### PR: Fix PushNotificationIOS listeners
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/24041
Description: ## Summary

Fixes https://github.com/facebook/react-native/issues/23868

Turns out if you set multiple PushNotificationIOS event handlers (for different types or two functions for same type), calling `removeEventHandler` will only remove the last one set.

This can cause some leaks and is just kind of behaviour that you wouldn't expect.

We also return listener itself from the `addEventListener` so that you can call `remove()`, just like for `BackButton`.

## Changelog

[iOS] [Fixed] - PushNotificationIOS properly remove listeners for registered events

## Test Plan

Set multip
  Comment by @grabbou: Let’s test this tomorrow
On Tue, 19 Mar 2019 at 17:51, Facebook Community Bot <
notifications@github.com> wrote:

> *@facebook-github-bot* approved this pull request.
>
> @cpojer <https://github.com/cpojer> is landing this pull request. If you
> are 
  Comment by @grabbou: @cpojer tested, it's ready now.
  Comment by @cpojer: I'll ship the fix in RN but would you mind also sending a PR to https://github.com/react-native-community/react-native-push-notification-ios as this module is being extracted at the moment? Sorry for the overhead.

### PR: Fix PushNotificationIOS listeners
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/24040
Description: Wrong branch.

### PR: Update React Native to use latest CLI
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/23940
Description: ## Summary

Latest CLI requires `reactNativePath` to be explicitly set when `react-native` is not present under `node_modules` (which is the case when running from source).

Fixes #23936 

This PR also updates CLI to latest version and removes private calls to `findPlugins` (it's now exposed under public interface). 

We also remove custom `rn-cli.config.js` options that are no longer needed that we have `--reactNativePath`. I added them a month ago as a temporary workaround.

## Changelog

[GENERAL] [FIXED] - Internal - Update to the latest CLI

## Test Plan

Run RNTester with
  Comment by @grabbou: I will update `rn-cli.config.js` to Metro config in a follow-up PR. Right now, let's just stick to a legacy format we used to have for a while.
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **1fe4799a880a07ad5df5db57b55d00adf97ff2b5**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Comment by @aliakbarazizi: You should update this in launchPackager.bat and packager.sh too

I run this command `node cli.js --reactNativePath ./ start` for running metro bundler.
  Review on RNTester/android/app/build.gradle: should we update template too ?
  Review on RNTester/android/app/build.gradle: Nope, this only affects projects that run React Native from source. RNTester uses `react-native` from source (`../` folder). All other apps get `react-native` from `node_modules/react-native`

### PR: Do not run packager in Release mode
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/23938
Description: ## Summary

When running your project in "Release" mode, Metro will start automatically. This is not desired. See https://github.com/react-native-community/react-native-cli/issues/31 for details

## Changelog

<!-- Help reviewers and the release process by writing your own changelog entry. See http://facebook.github.io/react-native/docs/contributing#changelog for an example. -->

[IOS] [FIXED] - Do not start Metro in Release mode

## Test Plan

Run RNTester in Release mode - packager doesn't start anymore

  Comment by @grabbou: Since the diff is hard to read, I only added:
```bash
&& [ \"$CONFIGURATION\" == \"Debug\" ] ; 
```
to the `if` statement.

After changes, it's:
```bash
if [ -z "${RCT_NO_LAUNCH_PACKAGER+xxx}" ] && [ "$CONFIGURATION" == "Debug" ] ; then
```
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **581711ca55e4727c73f09dc0fd279d5badd41bfe**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re
  Comment by @deepsweet: Changes from this PR are reverted back with [this commit](https://github.com/facebook/react-native/commit/3273d23a2644e841877df2474cdec4a19f2253d2#diff-883359f85083d00b7266ec2acebcca9f). Was it a mistake?

### PR: Fix DatePickerIOS e2e tests
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/23861
Description: ## Summary

DatePickerIOS tests stopped working after US changed their time zone on CircleCI. I decided to update the tests to be more reliable, by:
- removing "timezoneoffset" from the examples - I don't think it's needed. We don't demonstrate other props and it was causing us some troubles when timezones actually changed
- changing "interval" example from "time-only" to "datetime" because there's a known bug that prevented the previous example from working https://github.com/facebook/react-native/issues/9566
- splitting the label to two: one for date and other one for time, so that we c
  Comment by @grabbou: Detox tests are green, so this is ready to ship!
  Comment by @ericlewis: Woot!
  Comment by @react-native-bot: This pull request was successfully merged by @grabbou in **8270de9c2cfad721b554201ab97d645ffbfdc84b**.

<sup>[When will my fix make it into a release?](https://github.com/react-native-community/react-native-releases#when-will-my-fix-make-it-into-a-re

### PR: Fix Detox tests after upgrading to latest CLI
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/23191
Description: Latest changes inside CLI now require that Metro configuration is provided when building RNTester app. This is to let CLI know that instead of looking for "react-native" under "node_modules" (that is obviously not present since we are running from source), it should check the paths provided.

When running "npm start", it finds the configuration at the root. However, when building through Xcode (e.g. "react-native bundle" or "xcodebuild" in Release scheme), it runs "react-native-xcode.sh" that works in different folder and makes Metro not detect the configuration file.

This PR explicitly s
  Comment by @react-native-bot: @grabbou merged commit **9a9370481fb909a6e2f1066e98092b7dbd3237b9** into `facebook:master`.

### PR: Update references to the CLI
Repo: facebook/react-native | State: closed | URL: https://github.com/facebook/react-native/pull/23052
Description: This updates React Native to use latest CLI. We also create Metro configuration, because CLI looks for React Native in "node_modules" by default. Since we are running React Native from source, it will fail to find required files.

To avoid hacky logic to detect if we are running from source backed into the CLI, I decided to leverage the Metro configuration instead.
  Comment by @grabbou: @hramos - heads up, I need to fix remaining test failures before this ships. I will let you know when it's ready.
  Comment by @facebook-github-bot: I tried to merge this pull request into the Facebook internal repo but some checks failed. To unblock yourself please check the following: Does this pull request pass all open source tests on GitHub? If not please fix those. Does the code still apply
  Comment by @grabbou: @facebook-github-bot shipit

---

## CODE REVIEWS (14 PRs reviewed)

### Reviewed: fix: React Native CodeGen integration for 0.64-stable by @grabbou
  Mike's comment: Note: On 0.64-stable branch, React Native will always use CodeGen from `npm`, even when running from RNTester. 

I wish we had Yarn Workspaces set up right, that way, I could point here to use local version of CodeGen when running from this repository.

Something we will have to improve in order
  Mike's comment: One thing that I just realised is that you won't be able to set this unless the Script Phase is part of a user project. Right now, it's inside `FBReactNativeSpec` target.

So, I will most likely drop it.
  Mike's comment: In this particular case, this is more than fine. Right now, on 0.64-stable, in `packages`, we have CodeGen at 0.0.6 which doesn't work with this release. We would need to cherry-pick ALL commits related to CodeGen to bump it to 0.0.7.

By using an npm version instead, we can test RNTester and othe

### Reviewed: Exclude `i386` from valid architectures when building with Hermes on iOS by @grabbou
  Mike's comment: FWIW, I could detect when `flipper_post_install` is placed in a user `Podfile` and print a warning that this is deprecated and one should place `react_native_post_install` instead.

Is it worth it?
  Mike's comment: (just thinking about potential users that might forget to update the `Podfile`)
  Mike's comment: The technique would be this:
1. Make `flipper_post_install` accept a second optional argument
2. Pass second argument  from within `react_native_pods.rb`, e.g. `flipper_post_install(installer, true)`
3. When second argument is not defined, print a warning that users should replace it with `react_

### Reviewed: fix: building in release mode for simulator by @grabbou
  Mike's comment: Oh, true!

### Reviewed: fix: android artifacts in a release package by @grabbou
  Mike's comment: Good idea!
  Mike's comment: Regarding checking other files, I am not sure about that one. In case their number changes, the script will fail. I would assume that if `libfbjni.so` is present, it's fine.

### Reviewed: fix(iOS): `pod install` fails outside `ios` folder by @tido64
  Mike's comment: To keep it the same with `use_react_native`, we should probably just stick to `options[:path]` and pass it like here:

https://github.com/facebook/react-native/blob/355239b99125ffc7d17009a1c71e2fc42f7c104a/template/ios/Podfile#L7-L9
  Mike's comment: `reactNativePath` can be programatically set in the `react-native.config.js` and might be not what this resolves to in `use_react_native!`.

Example: https://github.com/facebook/react-native/blob/master/react-native.config.js#L32

Set to `.` for React Native root, this will not work inside React
  Mike's comment: Looks like `codegen_pre_install(:path => config[:reactNativePath])` present in a default template would resolve all issues without any further code changes.

The reason is: when we tell `codegen_pre_install` to use `config[:reactNativePath]` as I said above, which is an absolute path to React Nati

### Reviewed: feat: Enable Hermes to work on iOS by @grabbou
  Mike's comment: I think since `hermes` dependency is always pulled from the local `npm` package, I don't think it makes sense to a) keep version requirement in two places and b) read a version from `package.json` here. The main reason against doing the latter is that CocoaPods has slightly different (and incompatib
  Mike's comment: CC: @alloy
  Mike's comment: Not sure what's the latest versioning pattern, but I followed what we do for `hermes-engine` already. Note that `hermes-engine` could potentially be renamed to `hermes-engine-android`.

### Reviewed: fix: do not throw on missing `cliPath`, use the default value by @grabbou
  Mike's comment: Yeah, probably, we need a bit more work here. @Esemesek 
  Mike's comment: I have rewrote the logic a bit to support both cases
  Mike's comment: Nope,  we're running this from `projectDir` context, which is a directory inside your project. Will resolve to local `node_moduls`.

### Reviewed: Update default Podfile to not depend on a path by @grabbou
  Mike's comment: ah right! Copy paste XD

### Reviewed: chore(breaking): remove `initCompat` a.k.a legacy "init" by @grabbou
  Mike's comment: Haha, again 🤦 

### Reviewed: chore: remove global-cli by @grabbou
  Mike's comment: lol mistake

### Reviewed: refactor(breaking): remove deprecated `link`, `unlink` and associated code by @grabbou
  Mike's comment: That function actually looks for `xcworkspace` in first place and returns `isWorkspace: true`. I guess in scenario when there's no `xcworkspace` but multiple projects, we can print a warning in verbose mode, similarly to `findPodfile`, asking users to look at custom config?
  Mike's comment: I like this idea.
  Mike's comment: We will favour `iOS` anyway since this is `iOSConfig` used for `run-ios`. But I guess we can adapt it in a later PR to work for `Mac` too?

Can you point me to a configuration/helpers that you use for `macos`?

### Reviewed: Bump ora to 6.x by @stianjensen
  Mike's comment: I don't think this change was required while bumping to 6.x, was it? I personally have no objections to either convention, but I was confused while reviewing the PR.

@thymikee please lmk if you're okay with that change.
  Mike's comment: Thanks for pointing this out!

### Reviewed: fix: template name replacement in package.json by @Esemesek
  Mike's comment: I think better would be to replace `fileContent` with `replacedFileContent`. That way, we maintain `lowerCase` behaviour, at the same time, we do not overwrite changes (that happened, if any) when working with `package.json` .

### Reviewed: chore: migrate from turbo to nx by @jbroma
  Mike's comment: nit: This is not really related to the PR, because it's been around for a while, but I personally use Prettier via ESLint, and use ESLint as a "default formatter". That way, I can also automatically fix all ESLint issues on save, which is handy!
  Mike's comment: Do we need to build a project before linting it? I thought we lint the source! I guess same goes for `typescript`.
  Mike's comment: What I usually do for my projects is I set up one ESLint config at the top and I just run one process from the top. Works very good with VSCode as well (haven't tested monorepo setup, but I would imagine this one works too).

I guess this may not make too much sense in this setup, where - as it se

---

## ISSUES (54 total)

### Hermes throws Error instead of SyntaxError 
Description: ## Bug Description

When working on React Native, one of the test cases started to fail. It checks whether an underlying JS engine throws a `SyntaxError` when there is an actual syntax issue.

The error is:

> Error: Exception in HostFunction: Compiling JS failed: 1:2:'}' expected at end of block

Instead of a `SyntaxError`.

The code is:

```js
global.globalEvalWithSourceUrl('{');
`

### Tests are failing on master 
Description: ## Description

Right now, `yarn install` is failing silently https://app.circleci.com/pipelines/github/facebook/react-native/6828/workflows/93bf3792-da93-4824-9a36-40511cc86b84/jobs/173433/parallel-runs/0/steps/0-104 

As a result, it doesn't run `build` script in `react-native-codegen`. That leads to a missing `FBReactNativeSpec.h` file (that is autogenerated in that phase) and results in a 

### `react-native init` fails on 0.57 with missing babel plugin
Description: One of React Native dependencies, Metro, [depends](https://github.com/facebook/metro/blob/master/packages/metro/src/reactNativeTransformer.js#L15) on a package that it does not specify in its package.json.

It is causing the following error:
```
Loading dependency graph, done.
error: bundling failed: Error: Cannot find module '@babel/plugin-external-helpers'
    at Function.Module._resolveFi

### WebSocket `registerEvents` is undefined when running master
Description: ## Environment
```
 React Native Environment Info:
    System:
      OS: macOS High Sierra 10.13.6
      CPU: x64 Intel(R) Core(TM) i5-6267U CPU @ 2.90GHz
      Memory: 2.07 GB / 16.00 GB
      Shell: 5.3 - /bin/zsh
    Binaries:
      Node: 8.7.0 - /usr/local/bin/node
      Yarn: 1.3.2 - /usr/local/bin/yarn
      npm: 5.4.2 - /usr/local/bin/npm
      Watchman: 4.7.0 - /usr/local/bin/w

### [0.53] Commits to cherry-pick into stable release
Description: The thread containing issues that are blocking the 0.53 release and need to be addressed.

Please keep this list to critical bug fixes that are new in 0.53 and ideally have been merged into master -- post commit hashes rather than issue/PR numbers unless the issue/PR in question targets a problem specific to 0.53. The intent of these cherry-pick threads is not to solicit features but to fix thin

### [0.51] Commits to cherry-pick into stable release
Description: The thread containing issues that are blocking 0.51 release and need to be addressed. 

Before posting your comment, please read the below quote by @ide:

> Please keep this list to critical bug fixes that are new in 0.51 and ideally have been merged into master -- post commit hashes rather than issue/PR numbers unless the issue/PR in question targets a problem specific to 0.51. The intent of 

### Circle 2.0 setup requires further work
Description: ### Is this a bug report?

Bug

### Have you read the [Contributing Guidelines](https://facebook.github.io/react-native/docs/contributing.html)?

Yes

### Environment

Not related, issue is about CI.

### Steps to Reproduce

Checkout stable branch of master and try releasing.

### Expected Behavior

CircleCI builds `android`, `js` and `website` in parallel. After all tasks have f

### Website deploy script is broken
Description: As in title, after migrating to Circle 2.0, it doesn't build the docs.

### Make master to pass tests on CI
Description: Currently CI is broken due to flow failing. After investigating that matter for a bit, it turns out issues are coming from `metro-bundler` package.

It doesn't happen on `0.49-stable` and has been a result of either `flow` or `metro-bundler` being updated.

I am opening this issue to keep a better track of the status of this issue. Further more, I would also suggest to change the order of test

### [0.50] Commits to cherry-pick into stable release 
Description: Please let me know if there's anything you would like to be cherry-picked. Please note we only add fixes (no new features)

### [0.49] Commits to cherry-pick into stable release

### [0.48] Commits to cherry-pick into stable release

### [0.47] Commits to cherry-pick into stable release

### [0.46] Commits to cherry-pick into stable branch

### [0.42] Commits to cherry pick into stable

### [0.41] Commits to cherry pick into stable
Description: List of fixes to cherry-pick

CC: @oblador 

### [rnpm] Support new import system in plugins
Description: This is iOS only. 

We have to not `addHeaderSearchPaths` when a library opts-in to copy headers just like Facebook. That way, the are no longer needed.

That solution was raised by CodePush team as a possible solution and priority is to get it implemented before next release gets cut (or maybe even next set of cherry-picks lands).

### [cli] Ability to specify pre/post-link global hooks
Description: For now, the `pre/post` link hooks are plugin specific. That means a plugin can specify an arbitrary code to run after its being linked (`postlink/prelink`). 

What we want is the ability to define it on a project level, so that it gets executed anytime `link` is run.

Setup:
```json
{
  "rnpm": {
     "commands": {
       "postlink": ""
    }
  }
}
```
which is exactly what a plugin

### ActivityIndicator `color` not respected when accessibilityLabel set
Description: As in issue, when accessibilityLabel is set on a component, the `color` gets ignored and it renders `white` indicator. Removing it makes it work again.

### [0.39] Commits to cherry-pick into stable branch 

---

## REACTIFLUX Q&A - DEEP INTERVIEW ABOUT REACT NATIVE CORE

*brianboyko*: [Q&A] What effect would a Brexit "Leave" vote have on the U.K.'s tech industry?  
**grabbou**: Regarding Brexit, pretty good question. Haven't thought about it that much, but I wouldn't be surprised if some of my friends from Poland decide to come back, like @knowbody 😄

*davidbrear*: [Q&A] re: Navigator/NavigatorExperimental... which should we use and are systems like react-native-router-flux which rely on NavigatorExperiemental influencing the path forward with development?  
**grabbou**: Apart from react-native-router-flux, there's also ex-navigation built by Exponent, which is meant to be a v2 for the current ex-navigator. Having used it for quite a long time, I am moving towards using it in my next project. There's nothing wrong in using bare NavigationExperimental as is from react-native core, at least to understand the internals and how it works. Although I still have this feeling it might be too low-level for most of the users and can introduce the extra maintainance oveerheat, at least know when we have quite a few breaking changes being shipped. If you want to stay on the safe side of things, definitelly try out these community packages.

*Alias*: [Q&A] : How is the work on moving animations away from the JS thread going on both Android and ios. I've noticed someone work has been done on ios but a PR for Android seems to have died down when issues were hit.  
**grabbou**: Thanks @Alias for bringing this up. In fact I've just upgraded all my apps to 0.29.0-rc.0 to take advantage of native iOS animations. Can't really tell the performance difference for now as they are all in the early stage of development, but the code is definitelly there and is moving towards having more and more features. iOS has now a bit better support for different kinds of animations (although it still doesn't support animating bottom property for instance) than the Android one. The work on Android things is mainly done by Kris (authored original PR) and I've been successfully seeing small additions being made in every release.

*lewix*: [Q&A]  In your honest opinion. How does working with react-native compare to swift. If somebody already know swift, why should it use react-native? (it's a very subjective question)  
**grabbou**: I wouldn't say I am a Swift expert, but I have worked with Objective-C for quite a long time. I think I can answer that given I am one of the few (?) developers who actually quite enojoy using its syntax! To me, react-native solved the most annoying problems I had when developing apps, which was seamless support for REST APIs (and other json resources) as well as managing state of my app and avoiding side effects. So I wouldn't neccessarily say there's something in React Native that makes it a to go solution, but it's more React and the paradigm that's moving the platform forward.

*Alias*: [Q&A] what's the general feeling about the documentation? At the moment it seems very hit and miss - ios only demos, es5 examples and very hard to read examples. Will this be a future focus?  
**grabbou**: There's a community-hackhaton happening right now as we speak here in order to improve documentation, conducted by Facebook CA & London. If you take a look at latest master commits, you'll see plenty of docs-related PRs merged. The general plan is to improve examples and user experience, so that it's easier to navigate and find the informations you need

*Asep*: [Q&A] In your opinion whats the best way to learn RN for a beginner? What kind beginner app would teach someone like me most of RN?   
**grabbou**: @Asep at the company I am working, we don't have a general app idea we suggest our interns to build. It is important at this stage to pick something /idea/ you are excited about so that in case you have troubles making it working, you are still excited enough to keep it going. Currently we are building an app that controls AirPlay speakers so that everyone in the office can queue song to be played. Takes ages since everyone's learning React Native there, but it's fun so maybe it's also your next app idea? 😉

*ilyagelman*: [Q&A] Hi 😄 From your experience (based on GH issues or perhaps questions you receive), what people find the most hard/unappealing/annoying in React Native when developing real production apps?  
**grabbou**: @ilyagelman Good question. I would say native APIs are quite tricky, but it's been easier now with things like rnpm and stackoverflow having more and more answers. Back in the day, things like adding push notifications or location watchers were a bit complicated to someone who just used to access these properties under window. And that's iOS only. Soon after that, you will find yourself going through Google docs trying to understand how to set it up.  
But I don't feel super strong with this answer. There are tons of issues, so I can also list styles and flexbox problems people are having, for sure.

*doodirock*: [Q&A]what are your thoughts on Angular 2? Do you see it being a competitor to React or has Angular had its time in the sun.   
**grabbou**: @doodirock I've stopped using Angular like a year ago, so can't really speak for it.  However, if we are speaking about its integration with the NativeScript which seems to be the most popular approach, I don't think it's going to have a better DX than React Native. Again, for someone with native experience, using 1:1 native APIs with Javascript may seem appealing, but at that point, I'd just consider going straight to the native code. React Native has this nice abstraction that you can just use web-like APIs in a cross-platform way where possible.  
*doodirock*: Interesting answer.  Makes a lot of sense

*igin*: [Q&A] I really love react and react native as view libraries but not having a  preferred way of handling the state of the application and  communication with any backends leaves many questions open for developers. Many different libraries like redux, relay and others try to solve these issues. Can you suggest a stack that works for large REST based apps or is it really better to move to graphql and relay?  
**grabbou**: @igin We are still slowly adopting GraphQL at the company, mainly because most of the apps are a companion additions to already made services that consume REST APIs. In regards to the state management, it really depends. We use redux, some plugins and stuff to store and persist system-wide elements, like currentUser, token, session, flags about onBoarding. We also use a lot of state where it makes sense, e.g. when you open up a modal that contains user profile - there's no need to fetch it through redux for instance. My personal advice is to always start small & simple and move things to a more convinient place, like redux when you feel like it's getting out of your control.  
*igin*: makes sense. thanks!

*davidbrear*: [Q&A]: In your personal projects, do you typically differentiate navigation between android (with a drawer) and iOS (with a tab bar). Do you like to keep a similar feel in the app and use one or have special handlers that render differently on different devices? (sorry for all the navigation questions, I'm just wrestling with "best practices")  
**grabbou**: @davidbrear depends on the project! Recently I am seeing a trend that people want to have the so-called MainScene platform specific, so that iOS utilises tab bar with e.g. 4 tabs and the last one is the "options" tab (kinda Facebook-like) whereas the Android just goes directly with side menu. In most of the apps, we keep containers and presenters platform-independent and optimise small components to platform design guideliness. For example - we have Notifications view, on iOS there's no shadow and on Android the card looks a bit more Material-like. But the container itself is the same.  
*davidbrear*: awesome. Thanks Mike.

*cbrevik*: [Q&A] Hi dude. At the bank I'm currently working at we're contemplating building an app for certain services. Obviously I'm biased towards React Native, but I see their point about using something like Cordova to re-use existing HTML views. At the same time React Native still seems like more "beta" than Cordova, which in banks means unstable (and banks hate non-stable). What are your thoughts on these points?  
**grabbou**: @cbrevik can't list the name because of NDA, but there's one very popular UK bank having React Native in production that I've seen being developed. People can't really tell the difference. When we are pitching React Native to the client who's concerned about stability and performance, I am always bringing up the interoperability. It can either be native app running few React Native views, or React native app running few native views. I wouldn't say building banking app in RN/Cordova would be a wise decision after all, but the companion apps seem totally fine to me.

*rseemann*: [Q&A] Routing and Navigation doesn't seem yet to have The Way to solve it, as we have it for the web or the native platforms. Do you think there will be some standard implementation of it in the future, maybe with NavigatorExeperimental, or that probably will always fall to the developer to implement?(edited)  
**grabbou**: @rseemann I think NavigationExperimental is definitelly closer to being the to go solution here, since it's all in all up to the developer to manage the state of views and perform actions, like push/pop. We can now see that things that were almost impossible previously (tap twice the tab bar icon to reset active stack) are now dead simple. I have this feeling that the community wrappers mentioned previously are a really good candidates to answer almost all use-cases for typical app.  
*rseemann*: Haven't seen the answer given before. Thanks! 😃

*cdreier*: [Q&A] Hi, what is your preferred test setup for your js?  
**grabbou**: @cdreier nothing fancy, standard Jest set up as in react-native itself. We mainly unit-test reducers and actions, for views, we haven't had a lot of time yet to do it 

---

## CONFERENCE TALKS (8 transcripts)

### Talk: Chain-React-2017-The-Dark-Art-of-Bundlers-by-Mike-Grabowski.en.txt

[Music]
so my co-founder and CTO it goes like
that IO I'm also one of the core
contributors to react natives
if you are using react natives probably
know me from announcing magnetic
releases and publishing change looks and
today I'm here to talk about bundlers
how they work and how they relate to
react native I feel like it's kind of a
bit of you know hard topic is the first
stock but I'm really hoping you guys
will kind of enjoy it so let's start
with the most fundamental question what
a bundler really is how many of you have
an idea what the bungalow is please
raise your hand all right so like 60 50
more or less so this might be the most
educational presentation I've ever made
so far so I really feel like I hope that
you guys will enjoy those graphs I kind
of put a lot of effort to make that look
nice but I really kind of feel bad about
them anyway but yeah it's like bundler
is a tool that simply takes all your
joyous source files and put them into
one file right and that process is
called bundling there are many of them
these days with webpack or browserify
the most popular so we are probably not
wondering why do we need that right like
why do we even need to merge all the
files each one so to better understand
us let's step back to early days of web
and see how the things used to be so
historically JavaScript hasn't had any
standards for requiring dependencies
from your code there was no import or
required statements available so how did
we make functions of our code visible to
the outer world or how would how did we
import first part Kovach code to to our
applications the only way was through
global variable right so for example if
you wanted to jQuery which was pretty
common those days you'll go ahead and
add a strict stack that blows it from
external resource as a result your
global scope would get populated with
its bin
things in this case at the lower side so
one can say that this is actually neat
right all said with just a few lines of
code however imagine this scenario your
prototype works out your application
grows and you end up looking into
splitting your file to smaller reusable
pieces so you would end up with
something like this now the code will
get executed and the script tag should
have access to all the global variables
as defining the proceeding file the
problem here is the order
what if you jes wanted to depend on
barges go you'd have to change the order
right and manipulating the other scale
can lead you to weird issues and it's
more like a it's kind of similar to call
box health and I often call it a script
code so how do we solve it
turns out it was already solved in other
environment like for example in ODS that
implements its own module system using
require functions any sport object
amongst other things up top on top of
the common J's
module specs so what if we could do the
same in our front end code that would be
great right however there is one
technical limitation here the require
itself is synchronous in node.js
environment it's fine right because when
you want to load a file it's kind of
physically available next to the file
you're already in so that's easy
however in context of web you need to
make an HTTP request to load a file that
has never been processed by the browser
yet and the other request is aging so
the solution is simple you can bundle
all the files and so on so that we have
them in memory at the time the required
function being cold and that's the
primary reason for you know the bundling
explained in under five minutes
so bundlers can be perceived as a
natural evolution of task runners that
we know like cows and grunt that
happened over the course a few years
there are lots of responsibilities in
scope for them rather than just getting
your code bundled into one chunk for the
sake of organizing
one of them for example in translation a
typical bundler can or has support for
transpiling your code that means for
reading it but source in particular
format for example in new at JS spec and
outputting it in an older supported form
of like es5 the most popular out there
is bubble and most bundlers out here
provide a first-class integration of it
so we mentioned already that in order
for required to work your entire
application has to be loaded into memory
that code is your bundle size to
increase and ship with models and
doesn't necessarily need to be loaded on
the initial page run right so code
splitting is a feature that allows you
to split your curl into various bundles
which can then be load it on demand or
in parallel and in es2015 compatible
environment for example you could resume
for function to obtain an instance of a
module the promise is resolved as soon
as the loading process is finished and
the instance of the module is available
and the last feature that is worth
mentioning is the code magnification for
example web pack 2 has suffered a poor
tree shaking that means it can determine
what parts of your modules are not used
for example you don't use one fun

---

### Talk: Chain-React-2018-ReasonML-and-You---A-Fireside-Chat-with-Mik.en.txt

hello everyone
uh i'm sort of surprised because from
the backstage i only saw those you know
tables so i was really sort of surprised
to see it's already prepared
anyway it's nice to see you again this
year enjoy portland beautiful weather
and u.s in general
this stuff that i'm making today is sort
of special because for most of my time
all the talks that i was making
they were all about javascript react
native tools you know releases and the
general experience working with native
modules
today i'm here to talk a bit about
reasonable our experience building that
and basically to tell you what we've
been after for the past year
so before we begin just a quick
introduction
i'm mike and surprisingly i'm a software
developer using react in particular
um i'm on a react native team
doing releases work around that helping
with general might enhance and some work
around common line tools as well so
three years ago i founded callstack
which is a consultancy with a mission to
help developers like you
launch their products on every platform
at the same time
that's three of us at chain react right
now with anna and adam we have a move
upstairs you can hit us up for some nice
t-shirts if there are any left stickers
and just generally chat about react
native and if you got any questions
about reasonable
about my talk feel free to hit us up
there
so before we start let me ask you a
question how many of you have ever heard
or used reasonable
before
okay so there is quite a few
those who didn't raise your hands don't
worry we got a few introduction slides
to go through reasonable basics so that
we all know uh what that's all gonna be
more or less about
so reasonable is a statically typed
language that is based on
more or less 25 years of occamol
experience you know
and research around multi-platform
development
it has a very powerful type system built
in with type inference and so that means
that you don't have to write types
everywhere you're writing your code
sometimes the compiler will just infer
the types for you
and the other key design point of reason
that i'm really excited about
is that reasonable is familiar to
javascript developers
and
i was sort of i sort of experienced that
myself because i used to
like be i used to learn a camel at my
university and i almost failed the
subject because of like being unable to
write algorithms in a comment it was
just too hard for me so when i first
experienced reasonable i was really
excited because many things that i
couldn't understand otherwise became
easy to understand straight away
and obviously it has a very very
powerful build system that makes build
times very fast especially the
incremental builds are so fast that
sometimes you even you know you you
can't even notice the that it rebuild in
the meantime
and so um just a quick uh introduction
to the syntax itself this is how you can
define a type declaration for something
that you would call an object in
javascript this is a record in
reasonable and in this case it's a
person that has a name and a surname of
type string
then you define
create an instance of that record
in this case it's me with my name and my
last name
and for example here's how you can
create an arrow function that accepts
this person as a first argument and what
it does is it basically console logs the
name
and this is something very similar to
spread operator in javascript which is
basically creating another instance of
that person as you can see type is
missing here it's automatically inferred
for you and it's obviously person
so more or less this is very similar to
javascript i picked those examples on
purpose just to show it's not a whole
new experience for you obviously there
are different things because it's a
different language all in all but in
many cases you will find yourself
already at home
so let's talk about ffi in reason ml
which is a foreign function interface
so ffi is a mechanism by which one
program written in this case in
reasonable can call routines or make use
of services that were made in other
language
so in case of reason this is about
accessing javascript code
for something that we call a binding and
bindings are just type definitions made
around javascript code to allow you
access
through types and guarantee sort of
types of safety when you are dealing
with a java world
and the following example will
demonstrate how you can actually create
a type definition for a math security
function in javascript so what you do
at the beginning is that you create
external
function of name sqrt and this is how
you will be calling that function from
reasonable and then you basically call
it as a next line
next what you do is you have to define
type definitions so you have to actually
think about the api declaration of the
javascript function in this case mafia
security and think what would be the
most appropriate type definition in this
case it's a float and it returns float
because that's essentially how it works
and as a last step you use so

---

### Talk: Imperative-is-the-new-black---Mike-Grabowski.en.txt

thank you hello everyone
so Mike and I'm here today to talk about
imperative development so I spent a lot
of time writing native modules and
extending react native and you know with
languages that are sort of less found in
JavaScript if you ask people on any meet
up like Objective C and those languages
are imperative and from the J's
community I've learned that imperative
is something bad something that I should
avoid and the code that I should be
writing some should be functional
declarative and pure it's not really
that true when we think in terms of
react native specifics and so the
purpose of this talk is to show you a
few use cases that I had some examples
and maybe the Mastiff itis fact that you
know in product is bad because it might
be actually a thing that you eventually
gonna use a like so why orchid call
stack which is company that I co-founded
and our mission is to help developers
and companies to run the wraps on all
the platforms and so it just happens to
the right now we are using react native
and since we are open-source enthusiasts
we are trying to contribute as much as
possible to the framework itself and by
going to conferences like this so if you
or your company is in need of some react
native help please reach out we'll be
more than happy to talk during this
conference so before we start let's do a
quick background check please raise your
hand if you have ever used react all
right I'm just testing if you are you
know gonna raise your head eventually
anyway so the real question is how many
of you know the difference between
imperative development and declarative
alright that's quite a few so let's do a
quick introduction anyway so that it's
easier to follow the slides long story
short in practice programming focuses on
how the change is going to happen right
and so you have this container that you
want to style so what you're gonna do is
you're gonna basically set every style
yourself line by line in this case
background wave and
so we give it a set of commands and you
expect the end result in return with
declarative approach on the other hand
you want your container you describe how
you want you your container to look like
and you don't think of how it's gonna be
painted on screen in our case that could
be react for instance where we describe
our render where we describe our kuraki
in render method and we expect the
framer to take care of that so the
difference between these two is that
instead of focusing on low level
implementation details like whether this
property is supported whether this is
going to be styled in that way or the
other we focus on the one we want to get
so we shift the responsibility from us
over to the framer girl library we trust
the library that the library will do its
job well and that gives you the
performant code and puts the focus on
the application development itself so
back to the title from urban dictionary
you know the new black is something cool
and new trend to follow and it's coming
from the fashion industry because black
is always you know in fashion so if
something is the new black it's
naturally going to be the cool thing but
interactive programming is not a new
thing right it used to be around for a
while the hardware implementation of
almost all computers are imperative all
hardware is designed to work that way
because it it sort of executed matching
code which is imperative and from the
low-level perspective the state of your
program is just memory and statements
that you write are the instructions that
imperatively tell the computer or the
processing unit what to do as a response
to what you want and if as a you know
the higher we go the more abstractions
are built on top like statements if if
statements and stuff like that so if
imperative programming is not a new
thing what is the title of my talk gonna
be about right so let's take a look a
closer look at one trend
that I've observed over the past few
years within our community and you will
hopefully have an answer one we once we
are done with this JavaScript ecosystem
compared to the others it's still
relatively young you know if we think of
reacting react native and the libraries
that we have and so we don't settle on
existing solutions we constantly keep
innovating right every once in a while
there is a new framework or a new
library that is about to change
something like we used to have Redux
now people are you know discussing
whether it's still the thing to go where
you know context was bad now it's not
that bad and stuff like that so it's
changing all the time as our use cases
change and so with our community hanging
out on mediums like Twitter that's the
place where we naturally share our
findings right when we find out
something really cool we post it on
Twitter like oh my god this is cool
library that I did please check it out
and that's what everyone does like we
check it out we install it we star it
and then we fill in backs and that's the
end of life cycle and then the other
develo

---

### Talk: Mike-Grabowski---Welcome-to-React-Native-EU-2017.en.txt

[Applause]
first of all thank you very much for
coming here and being part of this
conference I think that there are more
than 200 people in this hotel interested
in react native this week which is
exciting
so before we start let me tell you why
we decided to organize this conference
in first place react native has been out
there in a while for more than two years
now it's not longer at soy or yet
another fancy framework that can just
disappear the day after it's now a
serious platform that can have real
impact on the progress building and it
also changes the way we think about
mobile development in general right the
promise of platform agnostic JavaScript
that can run on many platforms at once
is attracting many developers from
different backgrounds starting from
project management and ending up with
native mobile development and so since
they all approach react native and
mobile development from a different
perspective the problems they are facing
are different I've read once on the
internet that attending conferences
doesn't make any sense they are
expensive the talks are recorded that
I'm being uploaded to the Internet so
what's the point right if all you can
get is free materials on YouTube well
for me it's us the community we don't
attend conferences just to listen to the
talks that you will be hearing after my
after my talk we attend these
conferences to talk with each other to
share our experience and learn how we
can write better apps together and
that's the reason and that's the real
reason why events like this exists you
know I'm also super excited about the
lineup that we have I believe that next
two days will change the way you think
about mobile development with react
native we have carefully selected 20
speakers each using react native in a
different way to sure that your
experience these challenges they are
facing on daily basis you will hear
everything here in order to get
productive react native starting from
how to plan the app in general ending up
with how to use condoms deployment
services in
to deploy your app right away to your
users since there is no dedicated time
for questions after each talk I
encourage you to remember your questions
and find speakers during coffee breaks
and just ask them there are a few
companies that I wanted to mention here
first of all thank you very much
formidable array index for coming here
and doing workshops on free as you know
the workshops that we decided to do this
year were slightly different than our
competitors regularly do other
conferences let's say we wanted to make
a university university that everyone
can attend and so we made it in a way
that we try to talk to as many people
and as many companies as possible and
try to convince them that the nonprofit
idea of a workshop is the best thing
that can happen for the community also
thank you very much in fin red for
partnering with us sharing your Twitter
sharing your customers user base to help
us kickstart the idea of react native
you and get very very first followers so
thank you very much for this without you
we wouldn't be here and you know now may
be a question did you already have
coffee today or planning to have yeah so
you can now go to native base repo give
them a star because today we are having
coffee thanks to them thank you and of
course this entire event wouldn't be
wouldn't happen if it wasn't for Cole
stack
now Cole stack is a company I co-founded
with Anna she's here on she's here in
the audience as well
we are JavaScript experts focused on the
reactive react native in particular we
have a lot of activity in the open
source and in the community if you are
following react native you probably seen
us doing releases from science a time or
you heard about Hall which is a
alternative to react native package or
that we doing and we are based here in
verse 12 so if this sounds like a geek
for you let us know we will be happy to
tell you more how how does it feel to
work at Cole Stagg and how you can apply
feel free to ask anyone from coal stock
about details we are wearing our
custom-made sweet work clothes military
style so we are kind of easy to locate
today and finally I just wanted to give
you a quick reminder about our code of
conduct that you can read in detail at
code of conduct comm since we kind of
put the link in the footer and I'm
pretty sure that some of you missed it
I'm just going to read it quick version
now and then we can start our conference
is dedicated to providing a harassment
free conference experience for everyone
regardless of gender gender identity and
expression age sexual orientation
disability physical appearance body size
race religion or lack thereof or
technology choices we do not tolerate
harassment of conference participants in
any form sexual language and imagery is
not appropriate for any conference venue
including talks workshops parties
Twitter and other online media
conference participants violating these
rules may be sanctioned or expelled from
the 

---

### Talk: Mike-Grabowski-interview.en.txt

Hi folks, welcome back live stream
Reacton 2025 day two. I'm here with Mike
Robavski, CTO and founder of Call Stack.
Hello.
>> Hey Mike, how you doing?
>> Great. Thanks for having me here.
>> Yeah, thank you for being here and
answering the questions from our live
studio uh live studio from our live
audience. Um and let's get started.
Okay,
>> let's go.
>> Cool. How lightweight is React Native
brownfield? Does it significantly
increase bundle size? That's a very good
question uh because you won't believe me
but I have never actually profiled the
actual u bundle size impact of the
brownfield library itself but I wouldn't
call it significant just because it is
mostly a couple of native files that I
would treat as helpers and utilities. So
generally speaking considering the whole
react native and all the native modules
you're adding to your application that
shouldn't feel like anything
significant.
>> Okay. Okay. Um, what kind of migration
path do you hope teams take? Start
small, one screen or feature islands? Do
you have any recommendations?
>> Typically, where we see most people uh
success stories is around starting with
uh a single screen and then uh gradually
moving outside. I mean that really
depends on your organization how you set
yourself KPIs, but it's either a screen
or feature island depending on that
migration.
>> Okay, cool. And speaking of migration
and success stories, are there any
brownfield success stories you can share
with us?
>> Yeah, there is a lot of I mean
unfortunately there's quite a few NDAs
I've signed over time. However, um you
know, we've seen um we've seen during
the keynote in the morning, we've seen
Zando and HelloFresh being showcased for
their brownfield stories and um React
Native Brownfield is pretty much um well
there is a picture of brownfield library
in uh one of the articles. So that's
what that one is easy to figure out. But
one thing to keep in mind is that
reactive brownfield itself is not a uh
it's not just a library. It's more of an
approach. You can really do it without
using our library. It's more about how
you package it. So I would say uh if you
look at those two articles uh they
pretty much uh capture reactive
brownfield and I would think of these
two as success story.
>> Okay. Wonderful. And how does the final
state of apps using brownfield look
like? Is it more of a hybrid approach or
do they fully transfer to React Native
over time?
>> Also very good question. I think often a
um misconception is that you have to
finish at a green field stage. So you
have to finish the rewrite uh where we
see a lot of companies being successful
is starting the migration uh doing only
the things that are necessary. Sometimes
they end up being grafield for the
foreseeable future. So I would say when
you start using uh React Native inside
your mobile app, do not aim necessarily
for phasing out all of your native
screens, if you end up staying somewhere
in between, that's perfectly fine.
>> Yeah. Cool. Well, thank you for sharing
those insights on migration and uh two
final questions for you. What's your
favorite React feature of all times?
>> Honestly, I love uh Hooks.
>> Okay. Wow.
>> I like Hooks. I I like how they u
initially when I was switching from
classes they made me change my mental
model and I learned a lot while I was
shifting from classes to function
components.
>> Okay. And what's uh what's a thing about
you that doesn't come up in normal
conversation.
>> So see here's the thing every time I go
to a conference I try to be uh very
lowkey about everything I do outside. I
mostly focus on code and I'm always
fully locked in. Okay.
>> But my passion is cars. I love driving.
style of racing and um
>> thing to know about me is that I have
full sleeve tattoo here and it's my
first car BMW. I have it tattooed all
the pieces on my arm. I cannot show it
right here but maybe when we meet the
other day you'll see it right here.
>> Part of the suspension is right here. So
it's like this little passion of mine.
>> Really passionate.
>> Yeah.
>> Cool. I never realized you had a full
sleeve. That's really cool.
>> Uh it was supposed to be a mystery so I
didn't really answer the question. Yeah.
There you go.
>> Thank you so much, Mike, for joining us
today. And uh folks, stay tuned.

---

## PODCAST EPISODES (5 transcripts)

### Episode: Building-in-React-React-Native-5-Years-Ago-Now-React-Univ.en.txt

[Music]
welcome to the react native Show podcast
brought to you by kak a total software
engineering consultancy my name is Kuba
Urban and I am your coffee talk host
today uh I have two more guests but you
know wait for it they're are special and
I will introduce them for now I just
wanted to say that we will talk about
the state of react state of react native
and all things around it uh we're going
to talk about Journeys in the tech
industry and how it can look like for
you know everyone else basically maybe
this will inspire your journey so my
guests today um one of them is my fellow
Co Stucker Ola Ola can you introduce
yourself please yes hi so my name is Ola
this short hand for Alexandra but I
always go by Ola because it's confusing
that these two names are one name yeah
as I've been uh I've been working at
Cola for the last oh my gosh over two
and a half years and in the same project
with Kuba for for like half a year or
year or even a year maybe a very
interesting project we work on TVs
mobile phones web everything and it's
challenging and it's
fun yeah and thank you very much Ola and
I'm glad to have you here to today and
my second guest it's a special guest
because she is not from Kack and she is
from from far away uh because uh from UK
Anisha uh can you please introduce
yourself tell us something more about
what you do on everyday basis sure uh hi
guys I'm Anisha and I'm a developer
Advocate at the Amazon app store um and
usually when I introduce myself the
first question that goes to everyone's
mind is like what is a developer
Advocate um so it's kind of my job to
make it easier for all the Developers to
develop for Amazon App Store so whatever
shape or form that takes sometimes it's
writing articles sometimes it's writing
sample code sometimes it's coming on
podcasts like these um but yeah it's
it's my role just to make it easier for
you to develop TV apps um tablet apps so
anything that goes on Amazon app store
and Fir OS um but my background is react
native and my focus is on react native
apps for
firest lovely so basically whenever I
cry over my project here I should just
call you and be like hey Anisha please
help yes and I will try my very best to
help because usually one person's
problem is similar to other people so if
I can solve it for you I'm sure I'll
help other people all right all right
awesome uh so yes people as you can see
and hear uh we have a lovely team today
and uh ladies here will talk about their
Journeys uh so you know sit back and uh
have a good good listen good watch
depending on the platform um
so maybe we'll start with Anisha so
Anisha how did you start your Tech
Career like what sparked the idea what
brought you to us yeah yeah so I did
engineering um at University so I did
biomedical engineering which is very not
related to what I do now um when I was
looking for jobs I knew that I wanted to
stay in London which is probably not a
good reason to be applying for jobs but
it was it was my motivation
and I started as a technical consultant
at IBM and while I was there a lot of
the projects were react and react native
based so I would annoy the developers
into teaching me because the project
management side or the things that you
have to do as a grad were not as
interesting as what they seem to be
doing um I did have a bit of background
so I did C++ and a bit of machine
learning in uni but I think it was just
really seeing like the cool things that
the developers were building so I
learned JavaScript um taught myself
while I was on the job and then begged
someone to put me on a project that was
react and that made me learn react um so
I didn't react like front end
development for about four years and
while I was doing that a lot of things
that I was learning I felt like would
consolidate it by sharing it so I did a
few talks and that's sort of how I ended
up as Amazon as a developer Advocate um
because sharing what I knew was like a
way for me to learn more um and I didn't
even realize it was 

---

### Episode: Migration-to-React-Native-React-Universe-On-Air-13.en.txt

[Music]
hello and welcome to the react native
show podcast i'm mook as your host and
in this episode we'll dive deep into the
migration to react native we'll talk
about migration from native to react
native expanding react web apps with
cross platform availabilities
and the two main approaches to use in
migrating to react native greenfield and
brownfield
and what to remember and what to avoid
during the migration process and much
much more so stay with us let's get
started and introduce my guest
joining me today is mike hujak head of
delivery department
at call stack and great expert in
brownfield development hello mike
hey lukas thank you for the introduction
it's great to see you
oh yeah definitely
so mike
as we know as me and you know you are my
boss so
i'll let you start easy and i will ask
you an easy question
so your official title is head of
delivery and i must admit when i joined
call stack
several months ago almost a year i
didn't know what that really means so
maybe you can explain to our listeners
what are your daily responsibilities at
call stack
sure but before i do it i'd like to say
that it is my second time on the react
native show podcast but it's first time
i will be talking with you
and i'm super excited about it uh
because
we've been working together for a while
but we rarely have a chance to dive deep
into uh topics uh as technical as
migration to react native
so yeah thank you for the invitation
again
and getting back to your question uh at
call stack i'm managing team of
developers project managers and quality
assurance engineers
and on top of that i'm responsible for
ensuring the highest quality of our
service delivery
hence the title uh which means setting
quality standards best practices uh for
both development and
managing our projects
and even it
sounds a bit manager-ish i still have
many opportunities to touch the
technical stuff for example i provide
technical consultancy for our
key accounts and i do some open source
oh yeah definitely and i know i know
that you had a lot of opportunities to
talk about this subject that we are in
right now so migration to react native
brownfield development in react native
can you quickly summarize for me what
are your credential in this area why we
should listen to you
because i love react native and i'm good
at it
but jokes aside um i'm the person who
really believes in react native for me
uh it's an amazing framework that brings
a lot of business value and it's very
pleasant to work with uh
so um
on
the other hand uh it is just a framework
to enhance mobile development and i was
always very keen to understand what lies
under the hood uh that's why i've been
exploring native technologies from
objective c to kotlin
in order to understand how they solve
certain problems so i participated in
many web
web and mobile projects both react
native and native and i think i have a
good grasp of both strong and weak
points of these technologies
and
yeah based on that experience i created
a library uh called react native
brownfield which is a set of tools for
facilitation of the integration of react
native intonative apps uh and um yeah
it's very uh useful in uh such
migrations so i think that's that's all
in terms of my credentials yeah let's
put up in in the uh react native
brownfield library we'll talk about it
in the
in the following part but maybe we can
start in more structured way and sure
we can discuss uh from your experience
what are the main reasons our client
come to call stack to migrate their apps
sure so there are multiple reasons why
uh i think we can split them into
two main categories uh
first is addressing existing
uh and second is creating gains for the
future
so future proofing
yes
uh or basically creating
benef business benefits for the
future uh yes so in terms of first
category the stimulus
for such a decision is often
a thing that's bad for your business for
example the application has poor
performance and you lose users or
receive flow absolute rat

---

### Episode: React-Native-EU-2021---Virtual-Conference-Day-I.en.txt

[Music]
[Applause]
[Music]
[Applause]
[Music]
[Applause]
[Music]
[Applause]
[Music]
[Applause]
[Music]
[Applause]
[Music]
[Applause]
[Music]
my
[Applause]
[Music]
done
[Music]
so
[Music]
hello everybody and welcome you to react
native youth edition my name is mike and
i'm your host of react native eu so
welcome everybody to our stream we are
streaming out of words of poland and as
you can see this conference is happening
remotely this time as well just like one
year before now regardless of this fact
we want to make sure that you take
maximum out of it because networking and
sharing knowledge between each other is
what we think is the most important
aspect of react native you so despite
being remotely we put a lot of effort to
making sure that this will be easy for
you um to do so before we start with the
talks i do have a couple of informations
to tell you uh connected to the
networking part there is a discord
channel on our callstack server you can
find the link
down below you can join it and ask your
questions about the talks we will answer
them on our special react native show
podcast that will be published soon
after the conference you can also talk
with other participants you can share
your knowledge and experience within
each other based on the talks so just
log in there stay there and treat it as
your networking aspect just like we were
all here in poland in the same place in
broadsword
now also make sure to follow call stack
i on twitter and reacneview on twitter
and tweet react native eu
everything about the conference let your
friends know that we are live so that
they can join us and they will not miss
the first part of the conference which
will be very exciting like the entire
two days that are in front of us
you can also visit our react native eu
website where you can see the agenda all
the talks and in case you are busy you
can pick the ones that you want to
attend but worry not we will all we will
publish them to our youtube channel a
couple of days
or maybe weeks after the conference so
it's still better to be here with us so
you can have the first hand experience
and knowledge
straight from the speakers
we are organizing this conference here
as i said in our code stack office so as
you can probably assume callstack is the
organizer
now callstack is a team of super great
react native and react developers we are
doing very very interesting projects all
about cross-platform software so in case
you are here somewhere from around
poland or maybe from poland make sure to
apply or just let us know that you are
interested in changing your job we have
a lot of great interesting opportunities
for you and challenges that may
uh feel you like there is still a lot of
exciting projects in front of you
just one important information before we
start this conference is also co-hosted
by my friend from costa gucash so in
case you see somebody else not me
introducing you to another call today or
tomorrow
don't be afraid
everything's going okay we are doing
this together because there is just so
many great talks here today that i i
felt like it's going to be a good idea
to share some of that experience with
somebody else that calls stack that also
likes doing podcasting and conferences
so let's start with what you are all in
for here so the react native talks now
the first blog is a cross-platform and
architecture blog so in this part we
will be talking about the things that
are important to react native at a core
level so underlying building blocks and
some things that you may not hear
every day about but understanding them
and having full exposition to them will
make you feel like you can build even
more advanced apps so our first speaker
is mark from expo and he will be talking
about how jsi powers the most advanced
camera library out there for react
native now
of course he will be talking about the
camera library but one thing that you
may that you don't that you can't miss
out of this talk is that uh gsi is
something that i

---

## TECHNICAL DOCUMENTATION (15 docs)

### ai-readme.md

[![image](https://github.com/user-attachments/assets/027ccbc1-c6c4-46a0-aa62-7b89d4e62f24)](https://www.callstack.com/open-source?utm_campaign=generic&utm_source=github&utm_medium=referral&utm_content=react-native-ai)

# React Native AI

A collection of on-device AI primitives for React Native with first-class Vercel AI SDK support. Run AI models directly on users' devices for privacy-preserving, low-latency inference without server costs.

## Features

- 🚀 **Instant AI** - Use built-in system models immediately without downloads
- 🔒 **Privacy-first** - All processing happens on-device, data stays local
- 🎯 **Vercel AI SDK compatible** - Drop-in replacement with familiar APIs
- 🎨 **Complete toolkit** - Text generation, embeddings, transcription, speech synthesis

## AI SDK Compatibility

| React Native AI | AI SDK |
| --------------- | ------ |
| 0.11 and below  | v5     |
| 0.12 and above  | v6     |

## DevTools

![AI SDK Profiler preview](website/src/public/dev-tools-preview.png)

The AI SDK Profiler plugin captures OpenTelemetry spans from Vercel AI SDK
requests and surfaces them in Rozenite DevTools. DevTools are runtime
agnostic, so they work with on-device and remote runtimes.

```bash
npm install @react-native-ai/dev-tools
```

Rozenite must be installed and enabled in your app. See the
[Rozenite getting started guide](https://www.rozenite.dev/docs/getting-started).

## Available Providers

| Provider        | Built-in | Platforms    | Runtime                                                             | Description                                                |
| --------------- | -------- | ------------ | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| [Apple](#apple) | ✅ Yes   | iOS          | [Apple](https://developer.apple.com/documentation/FoundationModels) | Apple Foundation Models, embeddings, transcription, speech |
| [Llama](#llama) | ❌ No    | iOS, Android | [llama.rn](https://github.com/mybigday/llama.rn)                    | Run GGUF models via llama.rn                               |
| [MLC](#mlc)     | ❌ No    | iOS, Android | [MLC LLM](https://github.com/mlc-ai/mlc-llm)                        | Run open-source LLMs via MLC runtime                       |

---

### Apple

Native integration with Apple's on-device AI capabilities. **Built-in** - no model downloads required, uses system models.

- **Text Generation** - Apple Foundation Models for chat and completion
- **Embeddings** - NLContextualEmbedding for 512-dimensional semantic vectors
- **Transcription** - SpeechAnalyzer for fast, accurate speech-to-text
- **Speech Synthesis** - AVSpeechSynthesizer for natural text-to-speech with system voices

#### Installation

```bash
npm install @react-native-ai/apple
```

No additional linking needed, works immediately on iOS devices (autolinked).

#### Usage

```typescript
import { apple } from '@react-native-ai/apple'
import {
  generateText,

---

### callstack-os.md

<!DOCTYPE html><!-- Last Published: Thu Mar 26 2026 08:30:44 GMT+0000 (Coordinated Universal Time) --><html data-wf-domain="www.callstack.com" data-wf-page="67ee625d7f1a7373681911c4" data-wf-site="67e6b7885e182e1054b556db" data-wf-intellimize-customer-id="117449901" lang="en"><head><meta charset="utf-8"/><title>Open Source Projects | React Native Core Contributors | Callstack</title><meta content="Explore our open source contributions to the React Native community. Core contributors since 2016 with 300+ commits and popular libraries used worldwide." name="description"/><meta content="Open Source Projects | React Native Core Contributors | Callstack" property="og:title"/><meta content="Explore our open source contributions to the React Native community. Core contributors since 2016 with 300+ commits and popular libraries used worldwide." property="og:description"/><meta content="https://cdn.prod.website-files.com/67e6b7885e182e1054b556db/681c9372dbb7524ecfc31526_Open%20Source.jpg" property="og:image"/><meta content="Open Source Projects | React Native Core Contributors | Callstack" property="twitter:title"/><meta content="Explore our open source contributions to the React Native community. Core contributors since 2016 with 300+ commits and popular libraries used worldwide." property="twitter:description"/><meta property="og:type" content="website"/><meta content="summary_large_image" name="twitter:card"/><meta content="width=device-width, initial-scale=1" name="viewport"/><meta content="3E3b9sipGWBVPgE8GTnPcJmRhBY9ANKavj9KNBFLoQE" name="google-site-verification"/><link href="https://cdn.prod.website-files.com/67e6b7885e182e1054b556db/css/callstack-3-0.shared.b19ee9baa.min.css" rel="stylesheet" type="text/css" integrity="sha384-sZ7puqVBVCyfFWk0qnBQg26nXU+J4yw2jRzh9ZwK0VjRsG/1uwRii2zOCA/KCvgX" crossorigin="anonymous"/><script type="text/javascript">!function(o,c){var n=c.documentElement,t=" w-mod-";n.className+=t+"js",("ontouchstart"in o||o.DocumentTouch&&c instanceof DocumentTouch)&&(n.className+=t+"touch")}(window,document);</script><link href="https://cdn.prod.website-files.com/67e6b7885e182e1054b556db/6821e1e956d1d88bb85f74fd_favicon.png" rel="shortcut icon" type="image/x-icon"/><link href="https://cdn.prod.website-files.com/67e6b7885e182e1054b556db/67fd992e0888d130d070d230_7d8dbf1cfd2604da8520f9d750434df1_webclip.png" rel="apple-touch-icon"/><script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Open Source Projects",
  "url": "/open-source",
  "inLanguage": "en",
  "description": "Explore our open source contributions to the React Native community. Core contributors since 2016 with 300+ commits and popular libraries used worldwide.",
  "about": {
    "@type": "Organization",
    "name": "Callstack",
    "description": "React Native core contributors building open source libraries and tools for the React ecosystem",
    "url": "https://callstack.com",
    "sameAs": [
      "https://github.com/

---

### cli-autolinking.md

# Autolinking

React Native libraries often come with platform-specific (native) code. Autolinking is a mechanism that allows your project to discover and use this code.

Add a library using your favorite package manager and run the build:

```sh
# install
yarn add react-native-webview
cd ios && pod install && cd .. # CocoaPods on iOS needs this extra step
# run
yarn react-native run-ios
yarn react-native run-android
```

That's it. No more editing build config files to use native code.

Also, removing a library is similar to adding a library:

```sh
# uninstall
yarn remove react-native-webview
cd ios && pod install && cd .. # CocoaPods on iOS needs this extra step
```

## How does it work

Each platform defines its own [`platforms`](./platforms.md) configuration. It instructs the CLI on how to find information about native dependencies. This information is exposed through the [`config`](./commands.md#config) command in a JSON format. It's then used by the scripts run by the platform's build tools. Each script applies the logic to link native dependencies specific to its platform.

## Platform iOS

The [react-native/scripts/react_native_pods.rb](https://github.com/facebook/react-native/blob/main/packages/react-native/scripts/react_native_pods.rb) script required by `Podfile` gets the package metadata from `react-native config` command during install phase and:

1. Adds dependencies via CocoaPods dev pods (using files from a local path).
1. Adds build phase scripts to the App project’s build phase. (see examples below)

This means that all libraries need to ship a Podspec in the root of their folder. Podspec references the native code that your library depends on.

The implementation ensures that a library is imported only once. If you need to have a custom `pod` directive then include it above the `use_native_modules!` function.

### Example

See example usage in React Native template's [Podfile](https://github.com/react-native-community/template/blob/main/template/ios/Podfile).

## Platform Android

The [`autolinkLibrariesWithApp`](https://github.com/facebook/react-native/blob/8c50bf0beb17ced7fdafeae7a734edfc03e6e0b2/packages/gradle-plugin/react-native-gradle-plugin/src/main/kotlin/com/facebook/react/ReactExtension.kt#L162) function from React Native Gradle Plugin (RNGP) must be registered in your project's `settings.gradle` file and called in `app/build.gradle` file and:

1. At build time, before the build script is run:
   1. RNGP plugin registered in `settings.gradle` runs `autolinkLibrariesFromCommand()` method. It uses the package metadata from `react-native config` to add Android projects.
   1. Then in `app/build.gradle` it runs `autolinkLibrariesWithApp()` method. It creates a list of React Native packages to include in the generated `/android/build/generated/rn/src/main/java/com/facebook/react/PackageList.java` file.
      1. When the new architecture is turned on, the `generateNewArchitectureFiles` task is fired, generating `/android/b

---

### cli-configuration.md

# Configuration

React Native CLI has a configuration mechanism that allows changing its behavior and providing additional features.

React Native CLI can be configured by creating a `react-native.config.js` at the root of the project. Depending on the type of a package, the set of valid properties is different.

Check the documentation for

- [projects](./projects.md)
- [dependencies](./dependencies.md)
- [platforms](./platforms.md)
- [plugins](./plugins.md)

to learn more about different types of configuration and features available.


---

### cli-init.md

# Initializing new project

There are couple of ways to initialize new React Native projects.

```sh
npx @react-native-community/cli@latest init ProjectName
```

> Note: If you have both `yarn` and `npm` installed on your machine, React Native CLI will always try to use `npm`. You can force usage of `yarn` by adding `--pm yarn` flag to the command.

> Note: for Yarn users, `yarn dlx` command similar to `npx` will be featured in Yarn 2.0: <https://github.com/yarnpkg/berry/pull/40> so we'll be able to use it in a similar fashion.

## Installing `react-native` and invoking `init` command

```sh
yarn init && yarn add react-native && yarn react-native init ProjectName
```

## Initializing project with custom version of `react-native`

```sh
# This will use the latest init command but will install react-native@VERSION and use its template
npx @react-native-community/cli@latest init ProjectName --version ${VERSION}

# This will use init command from react-native@VERSION through react-native-community/cli@${VERSION} (e.g. X.XX.X) automatically
npx react-native-community/cli@${VERSION} init ProjectName
```

## Initializing project with custom template

It is possible to initialize a new application with a custom template with
a `--template` option.

It should point to a valid package that can be installed with `npm` or `yarn` (if you're using `--pm yarn` option).

The most common options are:

- Full package name, eg. `react-native-template-typescript`.
- Absolute path to directory containing template, eg. `file:///Users/username/project/some-template`.
- Absolute path to a tarball created using `npm pack`.

For all available options, please check [Yarn documentation](https://classic.yarnpkg.com/en/docs/cli/add/#toc-adding-dependencies) and [Npm](https://docs.npmjs.com/cli/v6/commands/npm-install#synopsis).

```sh
# This will initialize new project using template from `react-native-template-typescript` package
npx @react-native-community/cli@latest init ProjectName --template ${TEMPLATE_NAME}

# This will initialize new project using init command from react-native@VERSION but will use a custom template
npx react-native-community/cli@${VERSION} init ProjectName --template ${TEMPLATE_NAME}
```

You can force usage of `yarn` if you have both `yarn` and `npm` installed on your machine:

```sh
npx @react-native-community/cli@latest init ProjectName --pm yarn
```

## Creating custom template

Every custom template needs to have configuration file called `template.config.js` in the root of the project:

```js
module.exports = {
  // Placeholder name that will be replaced in package.json, index.json, android/, ios/ for a project name.
  placeholderName: 'ProjectName',

  // Placeholder title that will be replaced in values.xml and Info.plist with title provided by the user.
  // We default this value to 'Hello App Display Name', which is default placeholder in react-native template.
  titlePlaceholder: 'Hello App Display Name',

  // Directory with the template w

---

### cli-readme.md

# React Native Community CLI

Command line tools that help you build apps with [`react-native`](https://github.com/facebook/react-native), shipped as the `@react-native-community/cli` NPM package.

[![Build Status][build-badge]][build] [![Version][version-badge]][package] [![MIT License][license-badge]][license] [![PRs Welcome][prs-welcome-badge]][prs-welcome] [![Lean Core Extracted][lean-core-badge]][lean-core]

_Note: CLI has been extracted from core `react-native` as a part of "[Lean Core](https://github.com/facebook/react-native/issues/23313)" effort. Please read [this blog post](https://www.callstack.com/blog/the-react-native-cli-has-a-new-home) for more details._

## Contents

- [Compatibility](#compatibility)
- [Documentation](#documentation)
- [About](#about)
- [Creating a new React Native project](#creating-a-new-react-native-project)
- [Usage in an existing React Native project](#usage-in-an-existing-react-native-project)
- [Updating the CLI](#updating-the-cli)
- [Maintainers](#maintainers)
- [License](#license)

## Compatibility

Our release cycle is independent of `react-native`. We follow semver and here is the compatibility table:

| `@react-native-community/cli`                                      | `react-native`            |
| ------------------------------------------------------------------ | ------------------------- |
| [^20.0.0](https://github.com/react-native-community/cli/tree/main) | ^0.81.0, ^0.82.0          |
| [^19.0.0](https://github.com/react-native-community/cli/tree/19.x) | ^0.80.0                   |
| [^18.0.0](https://github.com/react-native-community/cli/tree/18.x) | ^0.79.0                   |
| [^15.0.0](https://github.com/react-native-community/cli/tree/15.x) | ^0.76.0, ^0.77.0, ^0.78.0 |
| [^14.0.0](https://github.com/react-native-community/cli/tree/14.x) | ^0.75.0                   |
| [^13.0.0](https://github.com/react-native-community/cli/tree/13.x) | ^0.74.0                   |
| [^12.0.0](https://github.com/react-native-community/cli/tree/12.x) | ^0.73.0                   |
| [^11.0.0](https://github.com/react-native-community/cli/tree/11.x) | ^0.72.0                   |
| [^10.0.0](https://github.com/react-native-community/cli/tree/10.x) | ^0.71.0                   |
| [^9.0.0](https://github.com/react-native-community/cli/tree/9.x)   | ^0.70.0                   |
| [^8.0.0](https://github.com/react-native-community/cli/tree/8.x)   | ^0.69.0                   |
| [^7.0.0](https://github.com/react-native-community/cli/tree/7.x)   | ^0.68.0                   |
| [^6.0.0](https://github.com/react-native-community/cli/tree/6.x)   | ^0.65.0,^0.66.0,^0.67.0   |
| [^5.0.0](https://github.com/react-native-community/cli/tree/5.x)   | ^0.64.0                   |
| [^4.0.0](https://github.com/react-native-community/cli/tree/4.x)   | ^0.62.0,^0.63.0           |
| [^3.0.0](https://github.com/react-native-community/cli/tree/3.x)   | ^0.61.0                   |
| [^2.0.0](https://github.com/react-native-community/c

---

### paper-readme.md

<a href="https://www.callstack.com/open-source?utm_campaign=generic&utm_source=github&utm_medium=referral&utm_content=react-native-paper" align="center">
  <img alt="react-native-paper" src="https://github.com/user-attachments/assets/5c62c47c-7991-4189-be21-614d4ffa9029">
</a>
<h3 align="center">
  Material design for React Native.<br/>
  <a href="https://reactnativepaper.com">reactnativepaper.com</a>
</h3>

---

[![Greenkeeper badge](https://badges.greenkeeper.io/callstack/react-native-paper.svg)](https://greenkeeper.io/)

[![Build Status][build-badge]][build]
[![Version][version-badge]][package]
[![MIT License][license-badge]][license]
[![All Contributors][all-contributors-badge]][all-contributors]
[![PRs Welcome][prs-welcome-badge]][prs-welcome]
[![Chat][chat-badge]][chat]
[![Sponsored by Callstack][callstack-badge]][callstack]

 <p align="center"><i>React Native Paper is the cross-platform UI kit library containing a collection of customizable and production-ready components, which by default are following and respecting the Google’s Material Design guidelines.</i></p>
 
## Getting Started

Refer to the [getting started guide](https://callstack.github.io/react-native-paper/docs/guides/getting-started) for instructions.

## Documentation

Check the components and their usage in our [documentation](https://callstack.github.io/react-native-paper).

## Features

- Follows [material design guidelines](https://m3.material.io/get-started/)
- Works on both iOS and Android following [platform adaptation guidelines](https://material.io/design/platform-guidance/cross-platform-adaptation.html)
- Full [theming support](https://callstack.github.io/react-native-paper/docs/guides/theming)

## Try it out

🧑‍💻 Run the [example app](https://snack.expo.dev/@react-native-paper/react-native-paper-example_v5) with [Expo](https://expo.dev/) to see it in action. The source code for the examples are under the [/example](/example) folder.

📲 You can also try out components in our demo apps available in the both stores [Android](https://play.google.com/store/apps/details?id=com.callstack.reactnativepaperexample&hl=pl&gl=US) and [ iOS](https://apps.apple.com/app/react-native-paper/id1548934513).

## Contributing

Read the [contribution guidelines](/CONTRIBUTING.md) before contributing.

## Figma and Sketch component kits

Use official component kits provided by [Material Design](https://m3.material.io/).

## Made with ❤️ at Callstack

`react-native-paper` is an open source project and will always remain free to use. If you think it's cool, please star it 🌟. [Callstack][callstack-readme-with-love] is a group of React and React Native geeks, contact us at [hello@callstack.com](mailto:hello@callstack.com) if you need any help with these or just want to say hi!

Like the project? ⚛️ [Join the team](https://callstack.com/careers/?utm_campaign=Senior_RN&utm_source=github&utm_medium=readme) who does amazing stuff for clients and drives React Native Open Source! 🔥

<!-- badges -

---

### repack-package-readme.md

<a href="https://www.callstack.com/open-source?utm_campaign=generic&utm_source=github&utm_medium=referral&utm_content=repack" align="center">
  <img src="https://raw.githubusercontent.com/callstack/repack/HEAD/logo.png" alt="Re.Pack" />
</a>
<h3 align="center">A toolkit to build your React Native application with Rspack or Webpack.</h3>
<div align="center">

[![mit licence][license-badge]][license]
[![npm downloads][npm-downloads-badge]][npm-downloads]
[![Chat][chat-badge]][chat]
[![PRs Welcome][prs-welcome-badge]][prs-welcome]

</div>

Re.Pack is a modern bundler for React Native applications, powered by Rspack and Webpack.

It serves as a drop-in replacement for Metro, offering enhanced functionality and access to a broad Webpack ecosystem, making it especially useful for implementing microfrontends architecture with Module Federation in your mobile app.

## Documentation

The documentation is available at [re-pack.dev](https://re-pack.dev).

## Made with ❤️ at Callstack

`@callstack/repack` is an open source project and will always remain free to use. If you think it's cool, please star it 🌟. [Callstack][callstack-readme-with-love] is a group of React and React Native geeks, contact us at [hello@callstack.com](mailto:hello@callstack.com) if you need any help with these or just want to say hi!

Like the project? ⚛️ [Join the team](https://callstack.com/careers/?utm_campaign=Senior_RN&utm_source=github&utm_medium=readme) who does amazing stuff for clients and drives React Native Open Source! 🔥

<!-- badges -->

[callstack-readme-with-love]: https://callstack.com/?utm_source=github.com&utm_medium=referral&utm_campaign=repack&utm_term=readme-with-love
[license-badge]: https://img.shields.io/npm/l/@callstack/repack?style=for-the-badge
[license]: https://github.com/callstack/repack/blob/main/LICENSE
[npm-downloads-badge]: https://img.shields.io/npm/dm/@callstack/repack?style=for-the-badge
[npm-downloads]: https://www.npmjs.com/package/@callstack/repack
[prs-welcome-badge]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge
[prs-welcome]: ./CONTRIBUTING.md
[chat-badge]: https://img.shields.io/discord/426714625279524876.svg?style=for-the-badge
[chat]: https://discord.gg/Q4yr2rTWYF


---

### repack-readme.md

<a href="https://www.callstack.com/open-source?utm_campaign=generic&utm_source=github&utm_medium=referral&utm_content=repack" align="center">
  <img src="https://raw.githubusercontent.com/callstack/repack/HEAD/logo.png" alt="Re.Pack" />
</a>
<h3 align="center">A toolkit to build your React Native application with Rspack or Webpack.</h3>
<div align="center">

[![mit licence][license-badge]][license]
[![npm downloads][npm-downloads-badge]][npm-downloads]
[![Chat][chat-badge]][chat]
[![PRs Welcome][prs-welcome-badge]][prs-welcome]

</div>

Re.Pack is a modern bundler for React Native applications, powered by Rspack and Webpack.

It serves as a drop-in replacement for Metro, offering enhanced functionality and access to a broad Webpack ecosystem, making it especially useful for implementing microfrontends architecture with Module Federation in your mobile app.

## Documentation

The documentation is available at [re-pack.dev](https://re-pack.dev).

You can also use the following links to jump to specific topics:

- [Quick Start](https://re-pack.dev/docs/getting-started/quick-start)
- [About Re.Pack](https://re-pack.dev/docs/getting-started/introduction)
- [Configuration](https://re-pack.dev/docs/guides/configuration)
- [API documentation](https://re-pack.dev/api/)

## Made with ❤️ at Callstack

`@callstack/repack` is an open source project and will always remain free to use. If you think it's cool, please star it 🌟. [Callstack][callstack-readme-with-love] is a group of React and React Native geeks, contact us at [hello@callstack.com](mailto:hello@callstack.com) if you need any help with these or just want to say hi!

Like the project? ⚛️ [Join the team](https://callstack.com/careers/?utm_campaign=Senior_RN&utm_source=github&utm_medium=readme) who does amazing stuff for clients and drives React Native Open Source! 🔥

<!-- badges -->

[callstack-readme-with-love]: https://callstack.com/?utm_source=github.com&utm_medium=referral&utm_campaign=repack&utm_term=readme-with-love
[license-badge]: https://img.shields.io/npm/l/@callstack/repack?style=for-the-badge
[license]: https://github.com/callstack/repack/blob/main/LICENSE
[npm-downloads-badge]: https://img.shields.io/npm/dm/@callstack/repack?style=for-the-badge
[npm-downloads]: https://www.npmjs.com/package/@callstack/repack
[prs-welcome-badge]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge
[prs-welcome]: ./CONTRIBUTING.md
[chat-badge]: https://img.shields.io/discord/426714625279524876.svg?style=for-the-badge
[chat]: https://discord.gg/Q4yr2rTWYF


---

### rn-getting-started.md

---
id: environment-setup
title: Get Started with React Native
hide_table_of_contents: true
---

import PlatformSupport from '@site/src/theme/PlatformSupport';
import BoxLink from '@site/src/theme/BoxLink';

**React Native allows developers who know React to create native apps.** At the same time, native developers can use React Native to gain parity between native platforms by writing common features once.

We believe that the best way to experience React Native is through a **Framework**, a toolbox with all the necessary APIs to let you build production ready apps.

You can also use React Native without a Framework, however we’ve found that most developers benefit from using a React Native Framework like [Expo](https://expo.dev). Expo provides features like file-based routing, high-quality universal libraries, and the ability to write plugins that modify native code without having to manage native files.

<details>
<summary>Can I use React Native without a Framework?</summary>

Yes. You can use React Native without a Framework. **However, if you’re building a new app with React Native, we recommend using a Framework.**

In short, you’ll be able to spend time writing your app instead of writing an entire Framework yourself in addition to your app.

The React Native community has spent years refining approaches to navigation, accessing native APIs, dealing with native dependencies, and more. Most apps need these core features. A React Native Framework provides them from the start of your app.

Without a Framework, you’ll either have to write your own solutions to implement core features, or you’ll have to piece together a collection of pre-existing libraries to create a skeleton of a Framework. This takes real work, both when starting your app, then later when maintaining it.

If your app has unusual constraints that are not served well by a Framework, or you prefer to solve these problems yourself, you can make a React Native app without a Framework using Android Studio, Xcode. If you’re interested in this path, learn how to [set up your environment](set-up-your-environment) and how to [get started without a framework](getting-started-without-a-framework).

</details>

## Start a new React Native project with Expo

<PlatformSupport platforms={['android', 'ios', 'tv', 'web']} />

Expo is a production-grade React Native Framework. Expo provides developer tooling that makes developing apps easier, such as file-based routing, a standard library of native modules, and much more.

Expo's Framework is free and open source, with an active community on [GitHub](https://github.com/expo) and [Discord](https://chat.expo.dev). The Expo team works in close collaboration with the React Native team at Meta to bring the latest React Native features to the Expo SDK.

The team at Expo also provides Expo Application Services (EAS), an optional set of services that complements Expo, the Framework, in each step of the development process.

To create a new Expo projec

---

### rnpm-readme.md

# Dear friends,

Last November me ([@Kureev](https://github.com/Kureev)) and Mike ([@grabbou](https://github.com/grabbou)) started RNPM. We aimed to bring you a better developer experience and bridge the tooling gap we had back then. Now, as you may know, RNPM is merged into [React Native core](https://github.com/facebook/react-native). It means that from now on you don't need to install a third-party software to use your favorite linking functionality (just use a react-native cli). We'd like to say a big "Thank you!" to everybody who supported us, filed new issues, composed PRs and helped us to review them.

Now, when RNPM is a part of React Native, we're going to seal this repository and keep working on React Native tooling inside the core. That said, I kindly ask you to file all new issues / prs in react-native repo and cc us. This repo (and other rnpm plugins) will be a available for a few more months in a read-only mode.

With love, 
Alexey Kureev and Michał Grabowski

![](http://esq.h-cdn.co/assets/16/17/640x360/gallery-1462115295-obama-mic-drop.gif)



![rnpm logo](http://s18.postimg.org/ex7oladjt/logornpm_final4.png)

![npm version](https://img.shields.io/npm/v/rnpm.svg) ![dependencies](https://img.shields.io/david/rnpm/rnpm.svg) [![Code Climate](https://codeclimate.com/github/rnpm/rnpm/badges/gpa.svg)](https://codeclimate.com/github/rnpm/rnpm) [![Test Coverage](https://codeclimate.com/github/rnpm/rnpm/badges/coverage.svg)](https://codeclimate.com/github/rnpm/rnpm/coverage) [![Circle CI](https://img.shields.io/circleci/project/rnpm/rnpm/master.svg)](https://circleci.com/gh/rnpm/rnpm)

**React Native Package Manager** built to ease your daily React Native development. Inspired by `CocoaPods`, `fastlane` and `react-native link` it acts as your best friend and guides you through the native unknowns. It aims to work with almost all packages available with no extra configuration required.

> RNPM should always be run in projects that use **version control** to ensure any changes made can be easily reverted

## Requirements

- node >= 4.1

## Getting started

#### Installation
```bash
$ npm install rnpm -g
```

#### Running

**Installing dependency:**

If you want to install a dependency and link it in one run:
```bash
$ rnpm install <name>
```

**Linking dependency:**

If you already have some installed (but not linked) modules, run:
```bash
$ rnpm link
```
In the case you want to link only one dependency, you can specify its name as an argument:
```bash
$ rnpm link <name>
```

## Rationale

Why? Tooling is important. We all know this. One of the biggest advantages of native iOS development is Xcode and its great tools. Unfortunately, the process of adding native dependencies to React Native projects is far from perfect and our aim is to make it fun again.

React Native Package Manager provides you with (soon) multiple actions to help you with daily development, including automatic app store releases, over-the-air integration with AppHub and r

---

### super-app-readme.md

# Super App Example

Welcome to the **Super App Example** repository! This project is part of a tutorial published on Callstack's blog, which you can find [here](https://www.callstack.com/blog/step-by-step-guide-to-super-app-development).

There are 2 branches in this repository:

- `main` - starting point for the tutorial
- `finished` - the end result that you should achieve after following the steps in the tutorial

Learn more about Super Apps here: [https://www.callstack.com/super-app-development](https://www.callstack.com/super-app-development?utm_campaign=super_apps&utm_source=github&utm_content=super_apps_example).

## Getting Started

Follow these steps to set up the project on your local machine.

### Prerequisites

- Make sure you have the latest version of `node` and `yarn` installed on your system. Please note that this project uses `yarn@3.x.x`, and not the classic version.

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/callstack/super-app-example.git
   ```

2. Install the dependencies (including pods):

   ```sh
   yarn bootstrap
   ```

### Running the app

1. Start the dev servers

   ```sh
   yarn start
   ```

2. Run the host-app on `ios` or `android`:

   ```sh
   yarn run:host-app:ios
   # or
   yarn run:host-app:android
   ```

## Made with ❤️ at Callstack

Super App Example is an open source project and will always remain free to use. If you think it's cool, please star it 🌟. [Callstack][callstack-readme-with-love] is a group of React and React Native geeks, contact us at [hello@callstack.com](mailto:hello@callstack.com) if you need any help with these or just want to say hi!

<!-- badges -->

[callstack-readme-with-love]: https://callstack.com/?utm_source=github.com&utm_medium=referral&utm_campaign=super-app-template&utm_term=readme-with-love


---

### Written: medium-case-studies.md

# "Is this possible with React Native?" — said an iOS developer to a React one

**By Mike Grabowski | Callstack Engineers | February 15, 2018**

## Introduction

At Callstack, the team frequently encounters a common question about React Native's capabilities. Whether clients seek to launch applications across multiple platforms or developers within the community aim to complete projects efficiently, the risk of encountering React Native's limitations is ever-present.

> "With React Native, the only limits are the ones you define yourself. In all other cases, you have native code that comes to the rescue."

## We Are Voice

This case study highlights a music application with significant technical demands. A primary challenge involved implementing an SVG score that synchronized with a music player, accounting for tempo and note highlighting.

> "One of the challenges was the score SVG, that represented the notes and voices for a particular arrangement and had to work seamlessly"

Additional requirements included offline functionality with the ability to transmit analytics data regardless of network connectivity.

## Green Bits

This application required integration with external hardware systems. The project demanded compatibility with Zebra label printers and jewelry scales through multiple connection types: USB, Bluetooth, and network protocols.

> "The major challenge with developing the app was to integrate the external hardware."

## Closing Remarks

Callstack welcomes new React Native development challenges, from hardware integration to navigation implementations. Contact: mike@callstack.com


---

### Written: medium-hermes-integration.md

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


---

### Written: medium-hermes-ios.md

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


---

### Written: medium-testing-rn.md

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


---

## INTERNAL DATA (Synthetic - Jira, Slack, 1:1 Notes)

### Jira Tickets

[
  {
    "key": "RPACK-401",
    "type": "Epic",
    "priority": "High",
    "status": "In Progress",
    "summary": "Module Federation v2 - Cross-platform Web + React Native support",
    "assignee": "mike",
    "sprint": "Q1-2025",
    "description": "Implement full Module Federation v2 support enabling shared modules between web (React) and mobile (React Native) apps. This is the core of our Super App strategy. Key challenges: Hermes compatibility, async chunk loading on mobile, shared dependency resolution across platforms.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-01-15",
        "body": "After the React Summit talk, got a lot of interest from enterprise clients. We need to prioritize the Hermes compat layer - right now dynamic imports crash on Hermes because it doesn't support the standard chunk loading mechanism. I'm working on a custom runtime plugin."
      },
      {
        "author": "pawel",
        "date": "2025-01-18",
        "body": "The webpack plugin is ready for testing. Mike, can you review the chunk loading implementation?"
      },
      {
        "author": "mike",
        "date": "2025-01-20",
        "body": "Reviewed. Two concerns: 1) Memory pressure on low-end Android devices when loading multiple federated modules simultaneously. 2) We need a fallback for when network fetch of remote module fails. Added both to acceptance criteria."
      }
    ]
  },
  {
    "key": "CLI-892",
    "type": "Bug",
    "priority": "Critical",
    "status": "Done",
    "summary": "Auto-linking breaks with New Architecture (TurboModules) on iOS",
    "assignee": "mike",
    "sprint": "v0.73-hotfix",
    "description": "When New Architecture is enabled, auto-linking generates incorrect podspec entries for TurboModule-compatible libraries. The generated code references the old bridge API instead of the TurboModule registry.",
    "comments": [
      {
        "author": "developer-x",
        "date": "2025-02-01",
        "body": "We're hitting this on our production app. Upgrading to 0.73 with New Arch enabled causes build failures for 12 of our 30 native dependencies."
      },
      {
        "author": "mike",
        "date": "2025-02-02",
        "body": "Root cause: the autolinking codegen in cli/packages/cli-platform-ios doesn't check for the turbomodule flag in the library's package.json. It always generates Bridge-style registration. Fix is straightforward but we need to handle the backward compat case where a library supports both old and new arch. PR incoming."
      },
      {
        "author": "mike",
        "date": "2025-02-04",
        "body": "Fix merged. The solution detects whether a library exports a TurboModule spec and generates the appropriate registration code. For libraries that support both architectures, we generate a conditional compilation block. Backported to 0.72.x as well."
      }
    ]
  },
  {
    "key": "CORE-155",
    "type": "Technical Decision",
    "priority": "Medium",
    "status": "Done",
    "summary": "ADR: Metro vs Re.Pack for enterprise monorepo clients",
    "assignee": "mike",
    "description": "Decision record: When should we recommend Metro vs Re.Pack to enterprise clients? Context: Several large clients are asking about our bundler recommendation for monorepo setups with 10+ packages.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-01-10",
        "body": "After working with 5 enterprise clients on this, here's my recommendation:\n\nUse Metro when: single app, <5 packages in monorepo, no code sharing with web, team unfamiliar with webpack.\n\nUse Re.Pack when: Super App architecture needed, Module Federation required, code sharing between web and mobile, complex build pipeline with custom transforms, >10 packages in monorepo.\n\nThe key differentiator is not performance (both are fast enough) - it's the webpack ecosystem. Enterprise clients already have webpack plugins, custom loaders, and build tooling. Re.Pack lets them reuse all of that."
      }
    ]
  },
  {
    "key": "RPACK-445",
    "type": "Story",
    "priority": "High",
    "status": "In Review",
    "summary": "Hermes compatibility layer for webpack dynamic imports",
    "assignee": "mike",
    "sprint": "Q1-2025",
    "description": "Hermes engine doesn't support standard webpack chunk loading via script tags (there's no DOM in RN). We need a custom runtime plugin that intercepts chunk loading requests and uses React Native's bundle fetching mechanism instead.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-02-10",
        "body": "The approach: we replace webpack's default chunk loading runtime with a custom one that uses RN's nativeModules to fetch and evaluate JS chunks. This is similar to what we did in Haul years ago, but now it needs to work with Hermes bytecode precompilation. The tricky part is making sure the Hermes bytecode cache works correctly with dynamically loaded chunks."
      }
    ]
  },
  {
    "key": "CS-2401",
    "type": "Initiative",
    "priority": "Medium",
    "status": "In Progress",
    "summary": "On-device LLM integration in React Native (callstackincubator/ai)",
    "assignee": "mike",
    "description": "Explore and ship production-ready on-device LLM execution for React Native apps. Use Vercel AI SDK compatibility layer. Target: enable RN developers to run small language models directly on device without server roundtrip.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-03-01",
        "body": "Initial prototype works with Llama 3.2 1B on iPhone 15 Pro. Inference speed is acceptable for chat-like interactions (~15 tokens/sec). Memory usage is the main constraint - we need to figure out model quantization and lazy loading. This could be huge for privacy-sensitive enterprise apps."
      }
    ]
  },
  {
    "key": "PAPER-789",
    "type": "Epic",
    "priority": "Medium",
    "status": "In Progress",
    "summary": "Material You (Material Design 3) migration for React Native Paper",
    "assignee": "mike",
    "sprint": "Q2-2025",
    "description": "Migrate React Native Paper from Material Design 2 to Material Design 3 (Material You). This involves dynamic color theming, updated component APIs, and new components.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-02-20",
        "body": "High-level strategy: incremental migration. We ship MD3 components alongside MD2 with a migration guide. No breaking changes in minor versions. The dynamic color extraction from wallpaper only works on Android 12+ - on iOS and older Android we fall back to manual theme configuration. Delegating component-level work to the Paper team, I'll focus on the theming engine architecture."
      }
    ]
  },
  {
    "key": "CS-2500",
    "type": "Story",
    "priority": "High",
    "status": "Done",
    "summary": "Prepare React Summit 2025 talk: Cross-Platform Federated Modules",
    "assignee": "mike",
    "description": "Prepare and deliver conference talk about building cross-platform Super Apps with Module Federation, React, React Native and Re.Pack.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-05-15",
        "body": "Talk outline:\n1. Why Super Apps matter for enterprise (real client examples, anonymized)\n2. Module Federation primer - how it works on web\n3. The challenge: making it work on mobile (no script tags, no dynamic imports on Hermes)\n4. Our solution: Re.Pack runtime plugin + custom chunk loading\n5. Live demo: shared cart module between web and RN app\n6. Future: cross-platform design systems via federated UI components"
      }
    ]
  },
  {
    "key": "CLI-950",
    "type": "Story",
    "priority": "Medium",
    "status": "In Progress",
    "summary": "Next-gen React Native CLI - successor to Community CLI",
    "assignee": "mike",
    "description": "Design and build the next generation React Native CLI that improves DX, startup time, and plugin architecture. Reference: dev.grabbou.xyz",
    "comments": [
      {
        "author": "mike",
        "date": "2025-03-10",
        "body": "The current CLI has grown organically and has accumulated a lot of tech debt from the rnpm days. The new CLI should be: 1) Faster (no unnecessary Node.js module resolution on startup), 2) Plugin-based (first-class plugin API instead of the current hack), 3) Better error messages (inspired by Rust compiler errors), 4) Built-in doctor command that actually works. I'm prototyping at dev.grabbou.xyz."
      }
    ]
  },
  {
    "key": "CS-2100",
    "type": "Technical Decision",
    "priority": "Low",
    "status": "Done",
    "summary": "ADR: Why we sunset Haul in favor of Re.Pack",
    "assignee": "mike",
    "description": "Document the decision to sunset callstack/haul and create Re.Pack as its successor.",
    "comments": [
      {
        "author": "mike",
        "date": "2024-06-01",
        "body": "Haul was our first attempt at bringing webpack to React Native. It worked, but it was a monolithic architecture that was hard to extend. Re.Pack is a complete rewrite with these improvements:\n1. Modular architecture - each feature is a separate plugin\n2. Webpack 5 support (Haul was stuck on 4)\n3. Module Federation support (impossible with Haul's architecture)\n4. Better Dev Server with HMR that actually works on device\n5. First-class support for code splitting\n\nHaul served us well for 3 years but the codebase was too rigid for where we needed to go."
      }
    ]
  },
  {
    "key": "HIRE-301",
    "type": "Task",
    "priority": "High",
    "status": "Open",
    "summary": "Define hiring criteria for Senior React Native Tooling Engineer",
    "assignee": "mike",
    "description": "We need to hire someone to take over CLI and Re.Pack maintenance. Define the role, required skills, and interview process.",
    "comments": [
      {
        "author": "mike",
        "date": "2025-03-15",
        "body": "This role is critical. The person needs to understand:\n- Bundler internals (webpack or metro, ideally both)\n- React Native build pipeline (both iOS and Android)\n- Native module linking and auto-linking architecture\n- Module Federation concepts\n- Open source maintenance (triaging issues, release process, community management)\n\nNice to have: Hermes internals, CocoaPods/Gradle plugin development.\n\nThe interview should include a practical task: given a broken auto-linking scenario, debug and fix it. This tests both RN knowledge and debugging skills."
      }
    ]
  }
]


### 1:1 Notes

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



### Slack Threads

[
  {
    "channel": "#react-native-core",
    "date": "2025-01-20",
    "thread": [
      {
        "author": "new-dev",
        "message": "Hey team, I'm trying to understand how auto-linking works under the hood. The docs explain the API but not the internals. Where should I start?"
      },
      {
        "author": "mike",
        "message": "Start with `packages/cli-platform-ios/src/link` and `packages/cli-platform-android/src/link` in the CLI repo. The core logic is:\n1. CLI scans node_modules for packages with native code\n2. It reads `react-native.config.js` from each package (or infers from package.json)\n3. For iOS: generates Podfile entries and runs pod install\n4. For Android: generates settings.gradle includes and build.gradle dependencies\n\nThe 'magic' is in step 2 - the config resolution. It has to handle edge cases like: scoped packages, monorepo symlinks, and packages that have different native code for old vs new architecture.\n\nI wrote the original rnpm which did this manually. When we merged it into RN core and then into the Community CLI, the architecture got more complex but the core idea is the same: scan, resolve config, generate native build files."
      },
      {
        "author": "new-dev",
        "message": "That's super helpful! One question - why do we generate build files instead of using a runtime approach?"
      },
      {
        "author": "mike",
        "message": "Runtime linking would require shipping a custom module resolver with every app, and it would need to know about native build systems (Xcode, Gradle) at runtime - which doesn't make sense. Native code needs to be compiled and linked at build time. The closest thing to 'runtime linking' for RN is Module Federation in Re.Pack, where JS modules are loaded dynamically. But native modules always need build-time linking."
      }
    ]
  },
  {
    "channel": "#repack-dev",
    "date": "2025-02-05",
    "thread": [
      {
        "author": "enterprise-client-dev",
        "message": "We're seeing Module Federation containers fail to load on Android with Hermes enabled. Error: `Cannot find module '__webpack_require__.l'`. Works fine with JSC."
      },
      {
        "author": "mike",
        "message": "Known issue - Hermes doesn't support the standard webpack chunk loading mechanism (`__webpack_require__.l`) which relies on `<script>` tags (no DOM in RN). We're working on a fix in the Hermes compat layer.\n\nWorkaround for now: add this to your webpack config:\n```js\noutput: {\n  chunkLoading: 'async-node',\n  chunkFormat: 'module'\n}\n```\nAnd in your Re.Pack config, enable the experimental runtime plugin:\n```js\nnew Repack.plugins.ChunkLoadingPlugin({ experimental: true })\n```\nThis uses our custom chunk fetcher instead of the default webpack one. It's not production-ready yet but works for testing."
      },
      {
        "author": "enterprise-client-dev",
        "message": "That worked! When is the production-ready fix expected?"
      },
      {
        "author": "mike",
        "message": "Beta in March, stable by end of Q1. The main thing we need to nail is memory management - when you load 10 federated modules, each one fetches and evaluates a JS chunk. On low-end devices that can cause OOM. We're implementing lazy loading with a max concurrency limit."
      }
    ]
  },
  {
    "channel": "#general",
    "date": "2025-02-15",
    "thread": [
      {
        "author": "junior-dev",
        "message": "Dumb question maybe but... why does Callstack maintain Re.Pack when Metro exists? Isn't Metro the official bundler?"
      },
      {
        "author": "mike",
        "message": "Not a dumb question at all, I get it a lot :)\n\nMetro is great for most RN apps. It's fast, well-integrated, and maintained by Meta. For 80% of projects, Metro is the right choice.\n\nRe.Pack exists for the other 20% - apps that need things Metro can't do:\n1. Module Federation (Super Apps with independently deployed features)\n2. Code splitting with dynamic imports\n3. Custom webpack loaders (SASS, SVG as components, etc)\n4. Integration with existing webpack-based build pipelines\n5. Tree shaking (Metro doesn't do this)\n\nThink of it like: Metro is Create React App, Re.Pack is custom webpack config. Most people should use CRA, but enterprise teams often need the flexibility.\n\nHistorically, we first built Haul (our webpack bundler for RN in 2017), then learned from that and rebuilt as Re.Pack with Module Federation as the core feature. The key insight was: enterprise clients don't want to replace their entire build system - they want to extend it to mobile."
      },
      {
        "author": "junior-dev",
        "message": "Makes total sense. So if I'm starting a new personal project, Metro is fine?"
      },
      {
        "author": "mike",
        "message": "100%. Don't use Re.Pack unless you have a specific reason to. It adds complexity that personal projects don't need."
      }
    ]
  },
  {
    "channel": "#react-native-releases",
    "date": "2025-01-08",
    "thread": [
      {
        "author": "release-coordinator",
        "message": "Preparing 0.74 RC. @mike any blockers from CLI side?"
      },
      {
        "author": "mike",
        "message": "Two things:\n1. The new init template needs updating for Kotlin DSL in build.gradle. PR is ready, needs review.\n2. Auto-linking codegen needs a fix for the New Architecture pod installation order. I'll have the fix today.\n\nOther than that, CLI is ready for 0.74. We tested against the RC branch yesterday - all integration tests pass."
      },
      {
        "author": "release-coordinator",
        "message": "Great. Can you also update the upgrade helper with 0.73 -> 0.74 diff?"
      },
      {
        "author": "mike",
        "message": "On it. The diff is clean this time - no major config file changes, just the Kotlin DSL migration which is optional."
      }
    ]
  },
  {
    "channel": "#hiring",
    "date": "2025-02-20",
    "thread": [
      {
        "author": "hr-lead",
        "message": "Mike, we have 3 finalists for the Senior RN Tooling Engineer role. Can you define the technical interview format?"
      },
      {
        "author": "mike",
        "message": "Here's what I want to test:\n\n1. **Debugging task** (30 min): Give them a broken auto-linking scenario - a native library that doesn't link correctly on iOS. They need to find the root cause. This tests: understanding of RN build pipeline, ability to read unfamiliar code, debugging methodology.\n\n2. **Design discussion** (30 min): 'A client wants to share a React component library between their web app and RN app. How would you architect this?' Looking for: understanding of bundler differences, awareness of platform-specific code, practical trade-offs.\n\n3. **Open source scenarios** (15 min): 'An issue with 50 upvotes asks for a feature that would add complexity to the codebase. How do you handle it?' Looking for: communication skills, ability to say no constructively, understanding of maintenance burden.\n\nThe ideal candidate doesn't need to know Re.Pack specifically - they need to understand how bundlers work and how native build systems (Xcode, Gradle) integrate with JS tooling."
      }
    ]
  },
  {
    "channel": "#repack-dev",
    "date": "2025-03-05",
    "thread": [
      {
        "author": "contributor-1",
        "message": "I submitted a PR to add Rspack support to Re.Pack. Thoughts?"
      },
      {
        "author": "mike",
        "message": "I love the initiative! Rspack is interesting because it's webpack-API-compatible but written in Rust, so it's much faster.\n\nHowever, before we merge this, we need to think about:\n1. Does Module Federation work with Rspack? Last I checked their MF implementation was incomplete.\n2. Our custom runtime plugins assume webpack internals - do they work with Rspack's runtime?\n3. Maintenance burden - do we want to support two bundler backends?\n\nMy suggestion: let's keep this as an experimental flag for now. If Rspack's MF support matures and we see demand, we can promote it to first-class. Can you add an `experimental_rspack` option and make sure our test suite passes with it?"
      }
    ]
  },
  {
    "channel": "#ai-incubator",
    "date": "2025-03-12",
    "thread": [
      {
        "author": "ai-dev",
        "message": "First external PR merged for callstackincubator/ai! Someone added Android NNAPI support."
      },
      {
        "author": "mike",
        "message": "Awesome! This is exactly what I was hoping for. The Vercel AI SDK compatibility layer makes it easy for people to contribute backend implementations.\n\nNext priorities for this project:\n1. Model quantization support (INT4/INT8) - critical for making larger models run on device\n2. Streaming responses (right now it waits for full generation)\n3. Better error handling when model doesn't fit in device memory\n\nI think this could become a significant project. Every enterprise client I talk to asks about on-device AI for privacy compliance. If we nail the DX, this could be as impactful as Re.Pack."
      }
    ]
  },
  {
    "channel": "#general",
    "date": "2025-03-20",
    "thread": [
      {
        "author": "team-member",
        "message": "Mike, someone on Twitter is saying Re.Pack is dead because we haven't released in 2 months. Should we respond?"
      },
      {
        "author": "mike",
        "message": "Ha, classic open source drama. We've been heads down on the Hermes compat layer - the biggest feature since Module Federation support. When it ships next week, they'll see it's very much alive.\n\nGeneral rule: don't engage with 'is X dead' tweets. Ship the work, the code speaks for itself. If people are asking, it means they care about the project, which is a good sign.\n\nI'll post a thread about what we've been working on once the beta is out."
      }
    ]
  }
]