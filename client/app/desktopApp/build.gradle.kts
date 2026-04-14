import org.gradle.api.tasks.compile.JavaCompile
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.kotlinJvm)
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }

    dependencies {
        implementation(projects.app.shared)
        implementation(compose.desktop.currentOs)
        implementation(libs.kotlinx.coroutines.swing)
    }
}

compose.desktop {
    application {
        mainClass = "com.jetlag.desktop.MainKt"
    }
}

// JDK 21 defaults `compileJava` to release 21; Kotlin stays on JVM 17 above — Gradle rejects the mix.
tasks.withType<JavaCompile>().configureEach {
    options.release.set(17)
}
