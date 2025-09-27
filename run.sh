#!/bin/bash
set -eu


CRON_TEMPLATE="etl/cronfile.templ"
CRON_FILE="etl/cronfile"


if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi


if [ -z "${CRON_SCHEDULE:-}" ]; then
  echo "CRON_SCHEDULE is not set in .env file!"
  exit 1
fi


echo "Generating new cronfile from template..."
if [ -f "$CRON_FILE" ]; then
  rm "$CRON_FILE"
fi
sed "s~{{CRON_SCHEDULE}}~${CRON_SCHEDULE}~g" "$CRON_TEMPLATE" > "$CRON_FILE"


echo "Rebuilding and restarting containers..."
docker-compose build
docker-compose up -d

echo "Cronfile updated and Docker containers restarted."


echo "Creating virtual env and installing dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r api/requirements.txt

echo "Setup complete. Running API server..."
python api/app.py