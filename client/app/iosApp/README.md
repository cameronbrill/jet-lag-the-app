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

The Xcode target **JetLagIOS** runs a **Run Script** phase (content synced from **`scripts/embed_kotlin_framework.sh`** when you run **`xcodegen generate`**) that `cd`s to **`client/`** and runs **`./gradlew :app:shared:embedAndSignAppleFrameworkForXcode`** (via **`mise x`** when **`mise`** is on **`PATH`**). If you build from the Xcode GUI and Gradle is not found, launch Xcode from a shell where **`mise activate`** ran, or put **`mise`** on your login **`PATH`**. The embed task expects Xcode’s build environment variables (configuration, SDK, architectures, etc.).

## Signing & device

1. Open **`JetLagIOS.xcodeproj`** in Xcode.
2. Select target **JetLagIOS** → **Signing & Capabilities** → choose your **Team**.
3. Change **Bundle Identifier** if `com.jetlag.app.ios.dev` is taken (unique per team).
4. Pick an **iPhone** or **simulator** destination and **Run**.

## Kotlin ↔ Swift entry

- Kotlin: [`../shared/src/iosMain/kotlin/com/jetlag/app/Main.kt`](../shared/src/iosMain/kotlin/com/jetlag/app/Main.kt) exports **`mainViewController()`** for the **`Shared`** framework.
- Swift: [`Sources/JetLagIOSApp.swift`](Sources/JetLagIOSApp.swift) calls **`MainKt.mainViewController()`**.

## Troubleshooting

- **`No such module 'Shared'`** — Xcode must find the framework under **`app/shared/build/xcode-frameworks/$(CONFIGURATION)/$(SDK_NAME)`** (e.g. `Debug/iphonesimulator`). [`project.yml`](project.yml) **`FRAMEWORK_SEARCH_PATHS`** must use that **`$(CONFIGURATION)/$(SDK_NAME)`** segment, **not** `$(CONFIGURATION)$(EFFECTIVE_PLATFORM_NAME)` (wrong folder shape). After changing **`project.yml`**, run **`xcodegen generate`** again, then **Product → Clean Build Folder** in Xcode.

## Tests / CI

- **`mise run //client:test`** on macOS with Xcode runs **`linkDebugFrameworkIosSimulatorArm64`** (framework link smoke) then **`allTests`** (includes **`iosSimulatorArm64Test`** under `:app:shared`).
- Linux CI keeps running JVM **`desktopTest`** only when Xcode is unavailable.
