#!/bin/bash
set -e

# --- Configuration ---
RELEASE_TAG="v1.0-models"
RELEASE_TITLE="Fixed greCy Model Wheels"
REPO_URL="CrispStrobe/greCy" # you can change to your GitHub username/repo
# ---

MODELS=(
    "grc_proiel_trf"
    "grc_perseus_trf"
    "grc_ner_trf"
    "grc_proiel_lg"
    "grc_perseus_lg"
    "grc_proiel_sm"
    "grc_perseus_sm"
)

# --- Step 1: Ensure all models are downloaded and cached ---
echo "--- Ensuring all models are cached... ---"
for model in "${MODELS[@]}"; do
    echo "Caching $model..."
    # Use install_model.py (v7)
    python install_model.py "$model" --no-deps
done
echo "--- All models are cached. ---"


# --- Step 2: Define file paths (with correct names) ---
CACHE_DIR="$HOME/.cache/grecy_models"

# --- ADDED grc_ner_trf ---
WHL_FILES=(
    "$CACHE_DIR/grc_proiel_trf-3.7.5-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_trf-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_ner_trf-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_proiel_lg-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_lg-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_proiel_sm-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_sm-0.0.0-py3-none-any.whl"
)

# Check if files exist
for f in "${WHL_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "Error: Wheel file not found at $f"
        echo "This means 'install_model.py' did not create the file as expected."
        echo "Please ensure you are using the fixed (v7) version of 'install_model.py'."
        exit 1
    fi
done

# --- Step 3: Create/Verify the GitHub Release ---
echo
echo "--- Checking for existing release $RELEASE_TAG ---"
if gh release view "$RELEASE_TAG" --repo "$REPO_URL" > /dev/null 2>&1; then
    echo "Release $RELEASE_TAG already exists. Uploading files to it."
else
    echo "--- Creating GitHub Release $RELEASE_TAG ---"
    gh release create "$RELEASE_TAG" \
        --repo "$REPO_URL" \
        --title "$RELEASE_TITLE" \
        --notes "Fixed, PEP 427-compliant wheel files for all greCy models. Install with --no-deps."
fi

# --- Step 4: Upload all files to the release ---
echo
echo "--- Uploading wheel files to $RELEASE_TAG (will overwrite if existing) ---"
gh release upload "$RELEASE_TAG" "${WHL_FILES[@]}" --repo "$REPO_URL" --clobber

echo
echo "--- All models successfully uploaded to GitHub Releases! ---"