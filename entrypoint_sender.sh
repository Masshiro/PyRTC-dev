#!/bin/bash

CMD=$(python3 utils/mahi_helpers.py)
if [ -z "$CMD" ]; then
  echo "Error: CMD is empty!"
  exit 1
fi

echo "Generated mahi command: $CMD"
exec $CMD -- bash -c '. run_sender.sh'
