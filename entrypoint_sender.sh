#!/bin/bash
ARG_A=${ARG_A}
CMD=$(python3 utils/mahi_helpers.py)
if [ -z "$CMD" ]; then
  echo "Error: CMD is empty!"
  exit 1
fi

echo "Generated mahi command: $CMD"
echo "user: $whoami"
echo "Algorithm: $ARG_A"
exec $CMD -- python run.py --sender -A "$ARG_A"