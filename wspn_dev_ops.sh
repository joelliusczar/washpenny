#!/bin/sh

meName="wspn_dev_ops.sh"
isSourced=0
[ "${0##*/}" != "${meName}" ] && isSourced=1

deploy_app() (
	ansible-playbook dev_ops/deploy_api.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)

setup_new_box_vm() (
	ansible-playbook dev_ops/new_box.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass -K
)

setup_new_box() (
	ansible-playbook dev_ops/new_box.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)

deploy_app_vm() (
	ansible-playbook dev_ops/deploy_api.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass -K
)

setup_schedules_vm() (
	ansible-playbook dev_ops/setup_schedules.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass
)

deploy_local_app() (
	ansible-playbook dev_ops/startup_api.yml -i ~/.ansible/inventories/testing  --ask-vault-pass -K
)

setup_schedules() (
	ansible-playbook dev_ops/run_schedule_setup.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)


if [ $isSourced = 0 ]; then
	command="$1"
	shift
	"$command" "$@"
fi