#!/bin/bash
# su - user && cd /app
CMD=$(python3 utils/mahi_helpers.py)
if [ -z "$CMD" ]; then
  echo "Error: CMD is empty!"
  exit 1
fi

echo "Generated mahi command: $CMD"
echo "user: $whoami"
exec $CMD -- python run.py --sender