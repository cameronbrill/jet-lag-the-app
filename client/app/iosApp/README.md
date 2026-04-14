# JetLag iOS placeholder (XcodeGen)

Host app under **`client/app/iosApp`**: SwiftUI shell that loads **`:app:shared`** as **`Shared.framework`**, which runs the same **`JetlagApp()`** Compose UI as Android/desktop.

## Prerequisites

- **macOS** with **Xcode** + Command Line Tools (`xcodebuild` works).
- **mise** from the repo root, then **`mise install`** inside **`client/`** (installs pinned **Java** and **XcodeGen** from [`client/mise.toml`](../mise.toml)).

## Regenerate the Xcode project

After editing **`project.yml`** or Swift sources layout:

```bash
cd client
mise install
cd app/iosApp
mise x -- xcodegen generate
open JetLagIOS.xcodeproj
```

The generated **`JetLagIOS.xcodeproj`** is committed so you can usually **`open`** directly; run **`xcodegen generate`** whenever **`project.yml`** changes.

## Gradle embed (Run Script)

The Xcode target **JetLagIOS** runs a **Run Script** phase (content synced from **`scripts/embed_kotlin_framework.sh`** when you run **`xcodegen generate`**) that `cd`s to **`client/`** and runs **`./gradlew :app:shared:embedAndSignAppleFrameworkForXcode`**. The script prepends common locations (**`~/.local/bin`**, Homebrew) to **`PATH`**, then prefers **`mise x -- ./gradlew …`** when **`mise`** is found; otherwise it uses **`JAVA_HOME`** or **`java`** on **`PATH`**. If neither **`mise`** nor Java is available, it prints a short error and exits (Dock-launched Xcode often has a minimal **`PATH`**). The embed task expects Xcode’s build environment variables (configuration, SDK, architectures, etc.).

### `PhaseScriptExecution` / “Embed Kotlin Framework” failed

Xcode’s issue navigator usually shows only a generic **PhaseScriptExecution** line. **Open the full log:** **Report** navigator (speech-bubble icon) → select the latest build → **Embed Kotlin Framework (Gradle)** → expand for **stderr** (Gradle / Kotlin / **`mise`** messages). Fix **`mise: command not found`** or missing JDK by putting **`mise`** and Java on **`PATH`**, or launch Xcode from a Terminal after **`mise activate`**.

### Reproduce the same build from the terminal (`xcodebuild`)

Useful for CI (on a **macOS** agent), agents, or avoiding the Xcode GUI. From the repo root, **`mise`** should be on your **`PATH`** (same constraint as a GUI build):

```bash
cd client
mise install
mise run //client:ios-xcode-build
```

That runs **`xcodebuild`** against **`app/iosApp/JetLagIOS.xcodeproj`**: it picks the first available **iPhone** simulator from **`simctl`**, passes **`-destination 'platform=iOS Simulator,id=…'`**, then sets **`ARCHS`** from the host (**`uname -m`**): **`arm64`** + **`ONLY_ACTIVE_ARCH=YES`** on Apple Silicon, **`x86_64`** + **`ONLY_ACTIVE_ARCH=YES`** on Intel, so the Swift link matches the Kotlin slice (**`iosSimulatorArm64()`** vs **`iosX64()`**). If **`uname -m`** is **`x86_64`** under **Rosetta** on an Apple Silicon Mac, prefer a native **arm64** shell (**`arch -arm64`**) so the CLI build matches arm64 simulators. **Buildkite** in this repo stays Linux-only unless you add a macOS builder.

To pick a specific simulator (adjust name to match **`xcrun simctl list devices available`**):

```bash
cd client/app/iosApp
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
xcodebuild -project JetLagIOS.xcodeproj -scheme JetLagIOS -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 16' build
```

On failure, scroll the log for **PhaseScriptExecution** / **BUILD FAILED** and the Gradle lines above them.

## Signing & device

1. Open **`JetLagIOS.xcodeproj`** in Xcode.
2. Select target **JetLagIOS** → **Signing & Capabilities** → choose your **Team**.
3. Change **Bundle Identifier** if `com.jetlag.app.ios.dev` is taken (unique per team).
4. Pick an **iPhone** or **simulator** destination and **Run**.

## Kotlin ↔ Swift entry

- Kotlin: [`../shared/src/iosMain/kotlin/com/jetlag/app/Main.kt`](../shared/src/iosMain/kotlin/com/jetlag/app/Main.kt) exports **`mainViewController()`** for the **`Shared`** framework.
- Swift: [`Sources/JetLagIOSApp.swift`](Sources/JetLagIOSApp.swift) calls **`MainKt.mainViewController()`**.

## Troubleshooting

- **Crash in `PlistSanityCheck` / `EXC_BAD_ACCESS` right after launch** — Compose Multiplatform validates the **host** [`Info.plist`](Sources/Info.plist). From **1.7.x**, **`CADisableMinimumFrameDurationOnPhone`** must be present and **`true`** (see Kotlin’s [Compose 1.7 release notes](https://kotlinlang.org/docs/multiplatform/whats-new-compose-170.html)). Without it, startup can throw **`IllegalStateException`** inside **`PlistSanityCheck`** (sometimes surfaced as a bad access in the debugger). The template **`Info.plist`** in this repo includes that key.

- **`No such module 'Shared'`** — Xcode must find the framework under **`app/shared/build/xcode-frameworks/$(CONFIGURATION)/$(SDK_NAME)`** (e.g. `Debug/iphonesimulator`). [`project.yml`](project.yml) **`FRAMEWORK_SEARCH_PATHS`** must use that **`$(CONFIGURATION)/$(SDK_NAME)`** segment, **not** `$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)` (wrong folder shape). After changing **`project.yml`**, run **`xcodegen generate`** again, then **Product → Clean Build Folder** in Xcode.

- **Undefined symbol `_OBJC_CLASS_$_SharedMainKt`** / **Linker command failed** — Swift calls **`MainKt.mainViewController()`**, which maps to that symbol inside **`Shared.framework`**. This almost always means an **architecture mismatch**: the app link line targets **x86_64** while the embedded framework is **arm64** only, or the opposite. **Intel Mac** simulators need an **x86_64** slice from Kotlin (**`iosX64()`** in every KMP module in the **`:app:shared`** graph); do **not** use **`EXCLUDED_ARCHS[sdk=iphonesimulator*]=x86_64`** on Intel (it produces an arm64 simulator app that will not run natively on the Intel simulator). **Apple Silicon** hosts should use **arm64** simulators and a matching framework (e.g. **`iosSimulatorArm64()`**). Check **`lipo -info app/shared/build/xcode-frameworks/Debug/iphonesimulator/Shared.framework/Shared`** (from **`client/`**) and compare to the linker’s **required architecture** in the Report navigator. **`mise run //client:ios-xcode-build`** should pass **`ARCHS`** consistent with **`uname -m`** (arm64 vs x86_64) when forcing a CLI build.

## Tests / CI

- **`mise run //client:test`** on macOS with Xcode runs a simulator **link smoke** for **`:app:shared`** (**`linkDebugFrameworkIosSimulatorArm64`** when **`uname -m`** is **`arm64`**, else **`linkDebugFrameworkIosX64`**), then **`allTests`** (includes **`iosSimulatorArm64Test`** / **`iosX64Test`** under `:app:shared` per host).
- **`mise run //client:ios-xcode-build`** on macOS runs a full **JetLagIOS** **`xcodebuild`** (embed script + Swift); see the **`xcodebuild`** section above.
- Linux CI keeps running JVM **`desktopTest`** only when Xcode is unavailable.
