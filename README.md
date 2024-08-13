# EVTX File Upload API

## Overview

This is a Python Flask-based application that provides a RESTful API for uploading `.evtx` files (Windows Event Viewer logs). The uploaded EVTX files are processed and converted to JSON format, which is then returned as a response. The application also includes Swagger UI for easy testing and interaction with the API.

## Features

- **Upload Endpoint**: A `/upload` endpoint that accepts `.evtx` files, processes them, and returns the contents as JSON.
- **File Validation**: Ensures that only `.evtx` files are accepted; returns a `400 Bad Request` error for other file types.
- **Error Handling**: Includes error handling for invalid or corrupt EVTX files, returning relevant error messages.
- **Swagger Integration**: Provides an interactive Swagger UI to test the API.


