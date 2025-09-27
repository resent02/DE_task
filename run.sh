#!/bin/bash
set -eu


CRON_TEMPLATE="/app/cronfile.tmpl"
CRON_FILE="/etl/cronfile"


if [ -f ".env" ]; then
  export $(cat ".env" | grep -v '#' | xargs)
fi


if [ -z "${CRON_SCHEDULE:-}" ]; then
  echo "CRON_SCHEDULE is not set in .env file!"
  exit 1
fi


echo "Generating new cronfile from template..."
sed "s~{{CRON_SCHEDULE}}~${CRON_SCHEDULE}~g" "$CRON_TEMPLATE" > "$CRON_FILE"


# echo "Rebuilding and restarting containers..."
# docker-compose build
# docker-compose up -d

# echo "Cronfile updated and Docker containers restarted."
