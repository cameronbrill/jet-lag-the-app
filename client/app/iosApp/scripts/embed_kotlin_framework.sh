#!/bin/sh
# Invoked from Xcode (Run Script). SRCROOT is the iosApp directory (sibling of this scripts/ folder's parent).
set -eu
CLIENT_ROOT="$(cd "${SRCROOT:?}/../.." && pwd)"
cd "$CLIENT_ROOT"
if command -v mise >/dev/null 2>&1; then
	exec mise x -- ./gradlew :app:shared:embedAndSignAppleFrameworkForXcode
else
	exec ./gradlew :app:shared:embedAndSignAppleFrameworkForXcode
fi
