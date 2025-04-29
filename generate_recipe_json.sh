#!/bin/bash

# Define output file path
OUTPUT_FILE="/Users/pete.jeffryes/Documents/pete/menu/menu_cli/input_data/20250428_2.json"
DESSERT_DIR="/Users/pete.jeffryes/Documents/pete/menu/mexican_update"

# Check if dessert_update directory exists
if [ ! -d "$DESSERT_DIR" ]; then
  echo "Error: $DESSERT_DIR directory not found!"
  exit 1
fi

# Start JSON array
echo "[" > "$OUTPUT_FILE"

# Counter for adding commas between entries
count=0
total=$(find "$DESSERT_DIR" -type f | wc -l)

# Process each file in the directory
find "$DESSERT_DIR" -type f | sort | while read -r file_path; do
  # Get just the filename without path and extension
  filename=$(basename "$file_path")
  extension="${filename##*.}"
  filename="${filename%.*}"

  # Replace underscores with spaces for title
  title=$(echo "$filename" | tr '_' ' ')

  # Increment counter
  count=$((count + 1))

  # Create JSON entry
  echo "  {" >> "$OUTPUT_FILE"
  echo "    \"category\": \"dessert\"," >> "$OUTPUT_FILE"
  echo "    \"title\": \"$title\"," >> "$OUTPUT_FILE"
  echo "    \"image_paths\": [" >> "$OUTPUT_FILE"
  echo "      \"$DESSERT_DIR/$filename.$extension\"" >> "$OUTPUT_FILE"
  echo "    ]" >> "$OUTPUT_FILE"

  # Add comma if not the last entry
  if [ "$count" -lt "$total" ]; then
    echo "  }," >> "$OUTPUT_FILE"
  else
    echo "  }" >> "$OUTPUT_FILE"
  fi
done

# Close JSON array
echo "]" >> "$OUTPUT_FILE"

echo "JSON file created successfully at $OUTPUT_FILE"
chmod +x ./generate_dessert_json.sh
