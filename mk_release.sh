#!/bin/bash
set -e

# --- Configuration ---
RELEASE_TAG="v1.0-models"
RELEASE_TITLE="Fixed greCy Model Wheels"
REPO_URL="CrispStrobe/greCy" # Your GitHub username/repo
# ---

# Define all 6 models
MODELS=(
    "grc_proiel_trf"
    "grc_perseus_trf"
    "grc_proiel_lg"
    "grc_perseus_lg"
    "grc_proiel_sm"
    "grc_perseus_sm"
)

# --- Step 1: Ensure all models are downloaded and cached ---
echo "--- Ensuring all 6 models are cached... ---"
for model in "${MODELS[@]}"; do
    echo "Caching $model..."
    # We run the installer. It will use the cache if the file exists,
    # or download it if it doesn't. We use --no-deps to avoid errors.
    # This assumes install_model.py (v6) is used, which creates the
    # correctly-named files (with underscores).
    python install_model.py "$model" --no-deps
done
echo "--- All models are cached. ---"


# --- Step 2: Define file paths (with correct names) ---
CACHE_DIR="$HOME/.cache/grecy_models"

# --- *** THE FIX *** ---
# Wheel filenames must use underscores in the distribution name
# (e.g., grc_proiel_trf) to be valid.
WHL_FILES=(
    "$CACHE_DIR/grc_proiel_trf-3.7.5-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_trf-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_proiel_lg-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_lg-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_proiel_sm-0.0.0-py3-none-any.whl"
    "$CACHE_DIR/grc_perseus_sm-0.0.0-py3-none-any.whl"
)
# --- *** END FIX *** ---

# Check if files exist
for f in "${WHL_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "Error: Wheel file not found at $f"
        echo "This means 'install_model.py' did not create the file as expected."
        echo "Please ensure you are using the fixed (v6) version of 'install_model.py'."
        exit 1
    fi
done

# --- Step 3: Create the GitHub Release ---
echo
echo "--- Checking for existing release $RELEASE_TAG ---"
# Check if release already exists to avoid error
if gh release view "$RELEASE_TAG" --repo "$REPO_URL" > /dev/null 2>&1; then
    echo "Release $RELEASE_TAG already exists. Uploading files to it."
else
    echo "--- Creating GitHub Release $RELEASE_TAG ---"
    gh release create "$RELEASE_TAG" \
        --repo "$REPO_URL" \
        --title "$RELEASE_TITLE" \
        --notes "Fixed, PEP 427-compliant wheel files for all 6 greCy models. Install with --no-deps."
fi

# --- Step 4: Upload all 6 files to the release ---
echo
echo "--- Uploading 6 wheel files to $RELEASE_TAG (will overwrite if existing) ---"
# Add --clobber to allow overwriting files if you re-run the script
gh release upload "$RELEASE_TAG" "${WHL_FILES[@]}" --repo "$REPO_URL" --clobber

echo
echo "--- All 6 models successfully uploaded to GitHub Releases! ---"