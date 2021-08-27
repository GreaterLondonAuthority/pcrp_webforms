import: mount install import_submissions unmount

import_submissions:
	@. $(PWD)/bin/activate && python import_webform_submissions.py

import_components: install
	@. $(PWD)/bin/activate && python import_webform_components.py

import_nodes: install
	@. $(PWD)/bin/activate && python import_webform_nodes.py

install_complete.txt:
	@ echo "Setting up virtual environment..."
	@python3 -m venv .
	@echo "Installing required packages..."
	@ . $(PWD)/bin/activate && pip install -r requirements.txt && touch install_complete.txt
	@echo "Creating webform files directory"
	@mkdir -p $(WEBFORM_FILES_PATH)

install: install_complete.txt

mount:
	@echo "Mounting the Drupal private files directory"
	@mkdir -p $(EFS_MOUNT_TARGET)
	@sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport $(EFS_MOUNT_SOURCE):$(EFS_PATH) $(EFS_MOUNT_TARGET)

unmount:
	@echo "Unmounting the Drupal private files directory at $(EFS_MOUNT_TARGET)"
	@if sudo test -d $(EFS_MOUNT_TARGET)/webform ; then sudo umount $(EFS_MOUNT_TARGET); fi

uninstall:
	@echo "Uninstalling Pip modules..."
	@ . $(PWD)/bin/activate && pip uninstall -y -r requirements.txt && rm install_complete.txt

clean: uninstall
	@echo "Removing directories..."
	@rm -rf bin include lib64 lib pyvenv.cfg share __pycache__ $(WEBFORM_FILES_PATH)
