.PHONY: dev prod test clear_cache backup

dev:
	flask --app app run --debug

prod: backup
	APP_ENV=production flask --app app run

test:
	pytest

clear_cache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

backup:
	@mkdir -p instance_prod/backups
	@if [ -f instance_prod/database.db ]; then \
		BACKUP="instance_prod/backups/database_$$(date +%Y-%m-%d).db"; \
		if [ ! -f "$$BACKUP" ]; then \
			python -c "import sqlite3; source=sqlite3.connect('instance_prod/database.db'); target=sqlite3.connect('$$BACKUP'); source.backup(target); target.close(); source.close()" && \
			echo "Backup criado: $$BACKUP" || exit 1; \
		else \
			echo "Backup de hoje já existe."; \
		fi; \
	else \
		echo "Banco de produção ainda não existe. Nenhum backup necessário."; \
	fi