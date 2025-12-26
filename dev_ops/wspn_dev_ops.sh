#!/bin/sh


deploy_app() (
	ansible-playbook deploy_api.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)

setup_new_box_vm() (
	ansible-playbook new_box.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass -K
)

setup_new_box() (
	ansible-playbook new_box.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)

deploy_app_vm() (
	ansible-playbook deploy_api.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass -K
)

setup_schedules_vm() (
	ansible-playbook setup_schedules.yml -i ~/.ansible/inventories/vms_inv  --ask-vault-pass
)

deploy_local_app() (
	ansible-playbook startup_api.yml -i ~/.ansible/inventories/testing  --ask-vault-pass -K
)

setup_schedules() (
	ansible-playbook run_schedule_setup.yml -i ~/.ansible/inventories/washpenny  --ask-vault-pass -K
)


command="$1"
shift
"$command"
