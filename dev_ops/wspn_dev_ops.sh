#!/bin/sh


connect_remote() (
	echo "connectiong to ${WSPN_SERVER_SSH_ADDRESS} using ${WSPN_SERVER_KEY_FILE}" &&
	ssh -ti "$WSPN_SERVER_KEY_FILE" "root@${WSPN_SERVER_SSH_ADDRESS}" bash -l
)

command="$1"
shift
"$command"
