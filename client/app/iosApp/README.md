# iOS app shell

The shared Kotlin Multiplatform code targets iOS (`iosArm64` + `iosSimulatorArm64`). A full Xcode project is intentionally not checked in yet — generate one with your preferred workflow (XcodeGen, Android Studio KMP wizard export, etc.) and wire the produced framework from `:app:shared`.
