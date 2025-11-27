#!/bin/bash
set -e

# Функция для создания базы данных и пользователя
create_database_and_user() {
    local db_name=$1
    local username=$2
    local password=$3

    echo "Создание базы данных '$db_name' и пользователя '$username'..."

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $username WITH PASSWORD '$password';
        CREATE DATABASE $db_name;
        GRANT ALL PRIVILEGES ON DATABASE $db_name TO $username;
        ALTER DATABASE $db_name OWNER TO $username;
EOSQL
}

# Создание базы данных и пользователя для SonarQube
create_database_and_user "sonar" "sonar" "sonar"

# Создание базы данных и пользователя для GitLab
create_database_and_user "gitlabhq_production" "gitlab" "gitlab"

echo "Базы данных и пользователи успешно созданы!"

# Проверка создания баз данных
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \l
    \du
EOSQL