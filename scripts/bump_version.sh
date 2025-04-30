#!/bin/bash
set -e

VERSION_FILE="VERSION"
VERSION=$(cat $VERSION_FILE)
IFS='.' read -r -a parts <<< "$VERSION"
patch=${parts[2]}
patch=$((patch + 1))
new_version="${parts[0]}.${parts[1]}.$patch"

echo $new_version > $VERSION_FILE

git config user.name "github-actions"
git config user.email "github-actions@github.com"
git add $VERSION_FILE
git commit -m "chore: bump version to $new_version"
git tag $new_version
git push origin main --tags