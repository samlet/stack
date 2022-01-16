bluecc:
	ipython --profile=bluecc

dump-pkgs:
	python -m sagas.ofbiz.tools dump_packages
	cp dump_pkgs.json /opt/app/hubs-common/asset/meta/pkgs.json

# dump-views:
#	python -m sagas.ofbiz.tools dump_views
#	cp dump_views.json /opt/app/hubs-common/asset/meta/views.json




