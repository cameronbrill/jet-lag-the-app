@file:Suppress("UnstableApiUsage")

rootProject.name = "JetLagClient"

enableFeaturePreview("TYPESAFE_PROJECT_ACCESSORS")

pluginManagement {
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("android")
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        gradlePluginPortal()
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositories {
        google {
            mavenContent {
                includeGroupAndSubgroups("android")
                includeGroupAndSubgroups("androidx")
                includeGroupAndSubgroups("com.android")
                includeGroupAndSubgroups("com.google")
            }
        }
        mavenCentral()
    }
}

include(":core")
include(":core-network")
include(":core-database")
include(":core-ui")
include(":core-platform")
include(":feature-game")
include(":feature-creator")
include(":feature-curses")
include(":feature-auth")
include(":app:shared")
include(":app:androidApp")
include(":app:desktopApp")
