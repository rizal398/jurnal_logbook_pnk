import pymysql
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# 1. Install PyMySQL sebagai driver MySQLdb
pymysql.install_as_MySQLdb()

# 2. Bypass pengecekan versi MariaDB
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# 3. Matikan fitur RETURNING agar kompatibel dengan MariaDB 10.4
DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)