#!/usr/bin/env bash
# Invoked from Xcode (Run Script). SRCROOT is the iosApp directory (sibling of this scripts/ folder's parent).
set -euo pipefail

export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:${PATH}"

if [[ -z "${SRCROOT:-}" ]]; then
	echo "error: SRCROOT is unset; this script must run from an Xcode build." >&2
	exit 1
fi

CLIENT_ROOT="$(cd "${SRCROOT}/../.." && pwd)"
cd "${CLIENT_ROOT}"

# Compose's syncComposeResourcesForIos reads PLATFORM_NAME and ARCHS from the environment.
# Some xcodebuild / Run Script contexts omit them → Gradle "provider has no value" / missing architectures.
if [[ -z "${PLATFORM_NAME:-}" ]]; then
	case "${SDK_NAME:-}" in
		iphonesimulator | *simulator)
			export PLATFORM_NAME=iphonesimulator
			;;
		iphoneos)
			export PLATFORM_NAME=iphoneos
			;;
	esac
fi
# When Xcode omits ARCHS, default to the host CPU for simulator (Intel x86_64 vs Apple arm64).
if [[ -z "${ARCHS:-}" || "${ARCHS:-}" == *undefined_arch* ]]; then
	case "${PLATFORM_NAME:-}" in
		iphonesimulator)
			export ARCHS="$(uname -m)"
			;;
		*)
			export ARCHS=arm64
			;;
	esac
fi

# Configuration cache can reuse a graph configured without Xcode env (e.g. after a desktop CLI run),
# which breaks Compose's syncComposeResourcesForIos (lazy providers stay unset at execution).
if command -v mise >/dev/null 2>&1; then
	exec mise x -- ./gradlew --no-configuration-cache :app:shared:embedAndSignAppleFrameworkForXcode
fi

if [[ -n "${JAVA_HOME:-}" && -x "${JAVA_HOME}/bin/java" ]]; then
	exec ./gradlew --no-configuration-cache :app:shared:embedAndSignAppleFrameworkForXcode
fi

if command -v java >/dev/null 2>&1; then
	exec ./gradlew --no-configuration-cache :app:shared:embedAndSignAppleFrameworkForXcode
fi

echo "error: could not run Gradle embed: mise and Java not found (PATH is often minimal when Xcode is launched from the Dock)." >&2
echo "hint: add ~/.local/bin and Homebrew to PATH, run 'mise activate', or open Xcode from a Terminal where mise works." >&2
exit 1
