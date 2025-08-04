#!/bin/bash

# Nombre del contenedor y la imagen de Docker para DynamoDB Local
CONTAINER_NAME="dynamodb-local-container"
IMAGE_NAME="amazon/dynamodb-local"
PORT_MAPPING="3100:8000"
ENDPOINT_URL="http://localhost:3100"
REGION="us-east-1"
TABLE_NAME="FormSessions"

echo "==================================================="
echo "  Gestión de DynamoDB Local con Docker y AWS CLI"
echo "==================================================="
echo ""

# --- Paso 1: Gestión del Contenedor Docker ---

echo "Verificando el estado del contenedor Docker '${CONTAINER_NAME}'..."

# 1.1. Verificar si el contenedor ya existe y está corriendo
if docker ps --filter "name=${CONTAINER_NAME}" --filter "status=running" --quiet | grep -q .; then
    echo "El contenedor '${CONTAINER_NAME}' ya está corriendo. No se requiere ninguna acción de Docker."
    # Si el contenedor ya está corriendo, no necesitamos hacer nada más con Docker.
elif docker ps -a --filter "name=${CONTAINER_NAME}" --quiet | grep -q .; then
    # 1.2. Verificar si el contenedor existe pero no está corriendo (detenido/exited)
    echo "El contenedor '${CONTAINER_NAME}' existe pero no está corriendo. Iniciándolo..."
    docker start "${CONTAINER_NAME}"
    if [ $? -eq 0 ]; then
        echo "Contenedor '${CONTAINER_NAME}' iniciado correctamente."
    else
        echo "ERROR al iniciar el contenedor '${CONTAINER_NAME}'. Por favor, verifica los logs de Docker."
        exit 1
    fi
else
    # 1.3. Si el contenedor no existe, verificar si la imagen está presente y ejecutar
    echo "El contenedor '${CONTAINER_NAME}' no existe. Verificando la imagen '${IMAGE_NAME}'..."
    if docker images --quiet "${IMAGE_NAME}" | grep -q .; then
        echo "La imagen '${IMAGE_NAME}' está presente. Creando y ejecutando el contenedor..."
    else
        echo "La imagen '${IMAGE_NAME}' no está presente. Descargando la imagen y creando el contenedor..."
    fi

    # Ejecutar el comando Docker para crear y correr el contenedor
    echo "Ejecutando: docker run -d --name ${CONTAINER_NAME} -p ${PORT_MAPPING} ${IMAGE_NAME}"
    docker run -d --name "${CONTAINER_NAME}" -p "${PORT_MAPPING}" "${IMAGE_NAME}"

    if [ $? -eq 0 ]; then
        echo "Contenedor '${CONTAINER_NAME}' creado y ejecutado correctamente en el puerto ${PORT_MAPPING//:/\/}."
    else
        echo "ERROR al crear y ejecutar el contenedor '${CONTAINER_NAME}'. Por favor, verifica los logs de Docker."
        exit 1
    fi
fi

echo ""

# --- Paso 2: Esperar a que DynamoDB Local esté listo ---

# Función para verificar si DynamoDB Local está respondiendo
check_dynamodb_ready() {
    echo "Esperando a que DynamoDB Local esté listo en ${ENDPOINT_URL}..."
    local retries=15 # Número de intentos
    local count=0
    local sleep_time=2 # Segundos entre intentos

    while ! aws dynamodb list-tables --endpoint-url "${ENDPOINT_URL}" --region "${REGION}" &>/dev/null; do
        if [ $count -ge $retries ]; then
            echo "ERROR: DynamoDB Local no respondió después de $retries intentos. Abortando."
            return 1
        fi
        echo "  DynamoDB Local aún no está listo. Reintentando en ${sleep_time} segundos... (Intento $((count + 1))/${retries})"
        sleep "${sleep_time}"
        count=$((count + 1))
    done
    echo "DynamoDB Local está listo y respondiendo."
    return 0
}

# Llamar a la función para esperar a que el servicio esté listo
check_dynamodb_ready
if [ $? -ne 0 ]; then
    echo "No se pudo conectar con DynamoDB Local. Terminando el script."
    exit 1 # Salir si DynamoDB Local no está listo
fi

echo ""

# --- Paso 3: Gestión de la Tabla DynamoDB ---

echo "Verificando si la tabla '${TABLE_NAME}' existe en DynamoDB Local..."

# 3.1. Verificar si la tabla ya existe
if aws dynamodb list-tables --endpoint-url "${ENDPOINT_URL}" --region "${REGION}" | grep -q "\"${TABLE_NAME}\""; then
    echo "La tabla '${TABLE_NAME}' ya existe. Saltando la creación de la tabla."
else
    # 3.2. Si la tabla no existe, crearla
    echo "La tabla '${TABLE_NAME}' no existe. Creándola..."
    aws dynamodb create-table \
        --table-name "${TABLE_NAME}" \
        --attribute-definitions AttributeName=session_id,AttributeType=S \
        --key-schema AttributeName=session_id,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
        --region "${REGION}" \
        --endpoint-url "${ENDPOINT_URL}"

    if [ $? -eq 0 ]; then
        echo "Tabla '${TABLE_NAME}' creada exitosamente."
    else
        echo "ERROR al crear la tabla '${TABLE_NAME}'. Por favor, verifica los logs de AWS CLI."
        exit 1
    fi

    # 3.3. Esperar a que la tabla esté activa antes de configurar TTL
    echo "Esperando a que la tabla '${TABLE_NAME}' esté activa..."
    aws dynamodb wait table-exists --table-name "${TABLE_NAME}" --endpoint-url "${ENDPOINT_URL}" --region "${REGION}"
    if [ $? -eq 0 ]; then
        echo "La tabla '${TABLE_NAME}' está activa."
    else
        echo "ERROR: La tabla '${TABLE_NAME}' no se activó. Abortando la configuración de TTL."
        exit 1
    fi
fi

echo ""

# 3.4. Configurar Time-to-Live (TTL) para la tabla
# Esta operación se puede ejecutar incluso si la tabla ya existía, ya que es una actualización.
echo "Configurando Time-to-Live (TTL) para la tabla '${TABLE_NAME}'..."
aws dynamodb update-time-to-live \
    --table-name "${TABLE_NAME}" \
    --time-to-live-specification "Enabled=true,AttributeName=ttl" \
    --region "${REGION}" \
    --endpoint-url "${ENDPOINT_URL}"

if [ $? -eq 0 ]; then
    echo "TTL configurado exitosamente para la tabla '${TABLE_NAME}' con el atributo 'ttl'."
else
    echo "ERROR al configurar TTL para la tabla '${TABLE_NAME}'. Por favor, verifica los logs de AWS CLI."
    exit 1
fi

echo ""
echo "==================================================="
echo "  Proceso completado exitosamente."
echo "==================================================="
