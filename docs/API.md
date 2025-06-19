# Data Explorer API Documentation

## Base URL
`http://localhost:8000/api`

## Endpoints

### Datasets

#### Create Dataset
```
POST /datasets/
```

**Request Body:**
```json
{
  "name": "string",
  "description": "string"
}
```

#### Upload Data
```
POST /datasets/{dataset_id}/upload
```

**Parameters:**
- `file`: CSV file to upload

#### Get Dataset Data
```
GET /datasets/{dataset_id}/data
```

**Query Parameters:**
- `limit`: Maximum number of rows to return (default: 100)
