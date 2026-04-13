import org.jetbrains.kotlin.gradle.plugin.KotlinPlatformType

plugins {
    alias(libs.plugins.androidApplication) apply false
    alias(libs.plugins.androidLibrary) apply false
    alias(libs.plugins.composeCompiler) apply false
    alias(libs.plugins.composeMultiplatform) apply false
    alias(libs.plugins.detekt) apply false
    alias(libs.plugins.kotlinAndroid) apply false
    alias(libs.plugins.kotlinJvm) apply false
    alias(libs.plugins.kotlinMultiplatform) apply false
    alias(libs.plugins.kotlinSerialization) apply false
}

// Compose Multiplatform publishes androidJvm and JVM/desktop variants; desktop source sets must
// request KotlinPlatformType.jvm so Gradle selects the desktop artifacts.
subprojects {
    afterEvaluate {
        configurations.forEach { cfg ->
            val n = cfg.name
            if (n.contains("desktopMain") &&
                (n.endsWith("CompileClasspath") || n.endsWith("RuntimeClasspath"))
            ) {
                cfg.attributes {
                    attribute(KotlinPlatformType.attribute, KotlinPlatformType.jvm)
                }
            }
        }
    }
}
