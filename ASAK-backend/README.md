# ASAK Backend

Spring Boot backend workspace for the ASAK kiosk API.

## Current State

This folder is a clean backend code skeleton.

Build and run commands are intentionally not finalized yet. The backend build setup will be organized later with Gradle.

## Current Source Layout

```text
backend/
  build.gradle
  settings.gradle
  src/
    main/
      java/com/asak/backend/
      resources/application.yml
    test/
      java/com/asak/backend/
```

## First Endpoint

After the backend build setup is finalized, the first check endpoint is:

```text
GET http://127.0.0.1:8080/api/health
```

Expected response:

```json
{"success":true,"status":200,"code":"HEALTH_OK","message":"ASAK backend is running","data":{"status":"UP"}}
```

## Data Boundary

- Keep backend code here.
- Do not place pipeline outputs, seed JSON, or menu images in this folder.
- Read shared data from root-level folders only when needed:
  - `../data-pipeline/phase1/output/`
  - `../asak-data/seed/`
  - `../asak-data/images/menu/`
