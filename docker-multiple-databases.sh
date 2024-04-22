#!/bin/bash

set -e
set -u

function create_user_and_database() {
  local database=$1
  echo "  Creating user and database '$database'"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE DATABASE "$database" OWNER $POSTGRES_USER;
EOSQL
}
# Создание базы для облигаций
if [ -n "$POSTGRES_BOND_DATABASES" ]; then
  echo "BOND database creation requested: $POSTGRES_BOND_DATABASES"
  for database in $(echo "$POSTGRES_BOND_DATABASES" | tr ',' ' '); do
    create_user_and_database "$database"
  done
  echo "BOND databases created"
fi
# Создание базы для облигаций
if [ -n "$POSTGRES_PORTFOLIO_DATABASES" ]; then
  echo "PORTFOLIO database creation requested: $POSTGRES_PORTFOLIO_DATABASES"
  for database in $(echo "$POSTGRES_PORTFOLIO_DATABASES" | tr ',' ' '); do
    create_user_and_database "$database"
  done
  echo "PORTFOLIO databases created"
fi

# Создание тестовый базы для облигаций
if [ -n "$POSTGRES_TEST_BOND_DATABASES" ]; then
  echo "BOND TEST database creation requested: $POSTGRES_TEST_BOND_DATABASES"
  for database in $(echo "$POSTGRES_TEST_BOND_DATABASES" | tr ',' ' '); do
    create_user_and_database "$database"
  done
  echo "BOND TEST databases created"
fi
# Создание тестовый базы для портфеля
if [ -n "$POSTGRES_TEST_PORTFOLIO_DATABASES" ]; then
  echo "PORTFOLIO TEST database creation requested: $POSTGRES_TEST_PORTFOLIO_DATABASES"
  for database in $(echo "$POSTGRES_TEST_PORTFOLIO_DATABASES" | tr ',' ' '); do
    create_user_and_database "$database"
  done
  echo "PORTFOLIO TEST databases created"
fi
