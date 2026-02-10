# Kitchen

## 1.0 Project Overview

Kitchen is a user-based web application designed to help users decide what dishes they can cook based on the ingredients they select or plan to purchase. The system bridges the gap between grocery shopping and meal planning by allowing users to explore recipes that match their available or selected ingredients, and then manage those ingredients through an integrated cart workflow.

The application targets users who frequently cook at home but struggle with deciding what to make or what ingredients to buy. By modeling ingredients, recipes, and user interactions as a modular backend system with RESTful APIs, Kitchen provides a structured and scalable solution that can later integrate with external grocery platforms or recipe sources.

Kitchen is implemented using a backend-first architecture with Flask and MongoDB, exposing clear API interfaces that support multiple user roles, persistent data storage, and modular expansion. A React frontend consumes these APIs to provide an interactive user experience. The system emphasizes clean separation of concerns, testability, and real-world software engineering practices consistent with the course requirements.

---

## 2.0 Core Requirements

### 2.1 User-Based System

Kitchen is designed as a user-based system in which all core functionality is centered around authenticated users and their interactions with the platform. Each user interacts with the system through a defined role, and the available actions and data access are determined by that role.

Users are able to create accounts, log in to the system, and maintain persistent state across sessions. User-specific data such as selected ingredients, saved recipes, and cart contents are stored in the database and associated with the user’s account. This ensures that each user has a personalized experience and that data is preserved between visits.

The backend enforces user-based access control by validating user identity on API requests and restricting certain actions to specific user roles. All user interactions with ingredients, recipes, and carts are performed through RESTful API endpoints, ensuring consistent and secure communication between the frontend and backend.

By structuring Kitchen as a user-based system, the application supports personalization, role-based functionality, and scalable growth, while meeting the project requirement for user-centered design and persistent data management.

---

### 2.2 User Roles

#### ROLE 1: Regular User

Regular Users are the primary users of the Kitchen application. They use the platform to explore recipes and plan meals.

Responsibilities and permissions include:

- Browse and search recipes by cuisine (e.g., Chinese, Mexican, European)
- View required ingredients for selected dishes
- Select ingredients and manage a personal cart
- Initiate grocery orders that are forwarded to third-party vendors (e.g., Weee)
- Upload images of ingredients they already have for ingredient recognition and recipe recommendations
- View and manage their own saved data only

Regular Users cannot:

- Modify global recipes or ingredients
- Access system configuration or administrative functions

---

#### ROLE 2: Content Manager

Content Managers are responsible for maintaining and curating all food-related content within the platform.

Responsibilities and permissions include:

- Create, update, and remove recipes
- Create, update, and manage ingredient definitions
- Tag recipes by cuisine, region, difficulty, kcal, and dietary attributes
- Ensure accuracy and consistency of food content across the platform

Content Managers cannot:

- Manage user accounts or roles
- Configure system settings or integrations
- Access administrative or infrastructure-level controls

---

#### ROLE 3: System Administrator

System Administrators oversee the operational and infrastructural aspects of the Kitchen platform.

Responsibilities and permissions include:

- Manage user accounts (activate, deactivate, suspend)
- Assign and manage user roles and permissions
- Configure and maintain third-party integrations (e.g., grocery vendors, image recognition services)
- Monitor system health, logs, and application stability
- Manage platform-level configuration and security settings

System Administrators do not:

- Perform routine recipe or ingredient curation

---

### 2.3 Persistent Storage

Kitchen requires persistent storage to support a real commerce + content platform, including: user accounts, recipe/ingredient reveal and recommendation, carts, orders forwarded to vendors (e.g., Weee), and optional image-based ingredient detection. All user state and platform content must survive across sessions and devices.

Kitchen will use MongoDB as the primary database because the system needs flexible content schemas (recipes evolve, cuisines expand, tags change) and high iteration speed. We will still design the data layer with clear ownership boundaries and explicit reference keys between collections.

---

### Proposed Database Schema

#### 1) users

Purpose: store accounts, roles, and account status.

PK: users._id  
FK: (none)

Fields:

- _id (PK)
- email (unique)
- password_hash
- role (enum: user, content_manager, admin)
- status (active/suspended)
- created_at, updated_at

---

#### 2) recipes

Purpose: store recipes, cuisine, instructions, and ingredient requirements.

PK: recipes._id  
FKs:
- recipes.created_by_user_id → users._id
- recipes.ingredients[].ingredient_id → ingredients._id

Fields:

- _id (PK)
- title
- cuisine_id (FK → cuisines) (optional but recommended)
- ingredients (array of objects)
  - ingredient_id (FK)
  - quantity
  - unit
- steps (array of strings)
- tags
- created_by_user_id (FK)
- status (draft/published)
- created_at, updated_at

---

#### 3) ingredients

Purpose: canonical ingredient list shared across all recipes and shopping.

PK: ingredients._id  
FK: (none)

Fields:

- _id (PK)
- name
- category
- aliases
- created_at, updated_at

---

#### 4) cuisines

Purpose: support multi-region expansion.

PK: cuisines._id  
FK: (none)

Fields:

- _id (PK)
- name
- region
- created_at

---

#### 5) carts

Purpose: persistent cart for ingredients to buy.

PK: carts._id  
FKs:
- carts.user_id → users._id
- carts.items[].ingredient_id → ingredients._id

Fields:

- _id (PK)
- user_id (FK)
- items
- updated_at

---

#### 6) vendors

Purpose: define partner grocery providers.

PK: vendors._id  
FK: (none)

Fields:

- _id (PK)
- name
- type
- api_enabled
- created_at

---

#### 7) vendor_products

Purpose: map Kitchen ingredients to vendor catalog items.

PK: vendor_products._id  
FKs:
- vendor_products.vendor_id → vendors._id
- vendor_products.ingredient_id → ingredients._id

Fields:

- _id (PK)
- vendor_id (FK)
- ingredient_id (FK)
- vendor_sku
- display_name
- price_snapshot
- last_synced_at

---

#### 8) orders

Purpose: orders created in Kitchen and forwarded to vendors.

PK: orders._id  
FKs:
- orders.user_id → users._id
- orders.vendor_id → vendors._id

Fields:

- _id (PK)
- user_id (FK)
- vendor_id (FK)
- items
- status
- vendor_order_reference
- created_at, updated_at

---

#### 9) image_uploads

Purpose: store image metadata.

PK: image_uploads._id  
FKs:
- image_uploads.user_id → users._id

Fields:

- _id (PK)
- user_id (FK)
- image_url or storage_key
- status
- created_at

---

#### 10) detections

Purpose: ingredient recognition results from images.

PK: detections._id  
FKs:
- detections.image_id → image_uploads._id
- detections.ingredient_id → ingredients._id

Fields:

- _id (PK)
- image_id (FK)
- ingredient_id (FK)
- confidence
- model_version
- created_at

---

## 2.4 Modular Architecture

Kitchen is designed as a modular system where each module owns a clear domain and exposes RESTful APIs. Modules depend on each other through API calls and shared identifiers (PK/FK-style references). This separation supports scalability, maintainability, and future integration with external grocery vendors (e.g., Weee) and AI services (image-based ingredient detection).

### Proposed Modules:

#### Module 1 — Identity & Access Module

Purpose: authentication, user accounts, roles, permissions.

Core responsibilities:

- Register / login / logout
- Issue and validate auth tokens (session/JWT)
- Store user profile + role (user / content_manager / admin)
- Admin-only: suspend users, change roles

Owned data:

- users (PK: users._id)

Dependencies:

Other modules depend on this module to validate identity and role before allowing actions.

---

#### Module 2 — Content Module (Recipes, Ingredients, Cuisines)

Purpose: manage and serve recipes, ingredients, and cuisine taxonomy.

Core responsibilities:

- Public/authorized browsing of recipes and ingredients
- Content manager: create/update/delete recipes and ingredients
- Manage cuisine categories and tagging
- Ensure canonical ingredient definitions (avoid duplicates)

Owned data:

- recipes (PK: recipes._id, FK: created_by_user_id → users._id)
- ingredients (PK: ingredients._id)
- cuisines (PK: cuisines._id, FK used by recipes.cuisine_id)

Dependencies:

- Depends on Identity module for role checks (content_manager/admin)
- Used by Recommendation module
- Used by Commerce module

---

#### Module 3 — Recommendation & Intelligence Module

Purpose: “What can I cook?” logic + image-to-ingredient detection pipeline.

Core responsibilities:

- Match recipes based on selected ingredients
- Recommend recipes ranked by match percentage
- Accept image uploads and return detected ingredients
- Store detection results for auditing and improvements

Owned data:

- image_uploads
- detections

Dependencies:

- Depends on Content module
- Depends on Identity module

---

#### Module 4 — Commerce & Vendor Integration Module

Purpose: convert meal planning into purchases and forward orders to vendors.

Core responsibilities:

- User cart management
- Create Kitchen orders
- Map ingredients to vendor products
- Forward orders to vendor APIs
- Track order lifecycle

Owned data:

- carts
- orders
- vendors
- vendor_products

Dependencies:

- Depends on Identity module
- Depends on Content module
- Depends on external vendor APIs

---

### Module Dependency Summary

- Content Module is the core knowledge base
- Recommendation Module depends on Content
- Commerce Module depends on Content and Vendors
- Identity Module is a cross-cutting dependency

---

## 2.5 API Interfaces

Kitchen exposes a set of RESTful API interfaces that allow internal modules to communicate with each other and enable future integrations with external services such as grocery vendors and image recognition providers. All APIs follow standard REST conventions, use JSON request/response bodies, and enforce authentication and role-based access control where required.

### 1) Identity & Access API

Public / Auth APIs:

- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

Admin-only APIs:

- PATCH /api/admin/users/:user_id/status
- PATCH /api/admin/users/:user_id/role

---

### 2) Content API (Recipes, Ingredients, Cuisines)

Recipe APIs:

- GET /api/recipes
- GET /api/recipes/:recipe_id
- POST /api/recipes
- PATCH /api/recipes/:recipe_id
- DELETE /api/recipes/:recipe_id

Ingredient APIs:

- GET /api/ingredients
- GET /api/ingredients/:ingredient_id
- POST /api/ingredients
- PATCH /api/ingredients/:ingredient_id

Cuisine APIs:

- GET /api/cuisines
- POST /api/cuisines

---

### 3) Recommendation & Intelligence API

- POST /api/recommendations/by-ingredients
- GET /api/recommendations/for-me
- POST /api/vision/upload
- GET /api/vision/:image_id/status
- GET /api/vision/:image_id/results

---

### 4) Commerce & Vendor Integration API

Cart APIs:

- GET /api/cart
- POST /api/cart/items
- PATCH /api/cart/items/:ingredient_id
- DELETE /api/cart/items/:ingredient_id

Order APIs:

- POST /api/orders
- GET /api/orders
- GET /api/orders/:order_id
- POST /api/orders/:order_id/forward

Vendor APIs:

- POST /api/admin/vendors
- GET /api/admin/vendors
- POST /api/admin/vendors/:vendor_id/products/map

---

## 3.0 Technical Stack

- Main Language: Python 3.9 or greater
- Operating System: UNIX-like
- API Server: Flask, flask-restx
- Database: MongoDB
- Testing Framework: pytest
- Build Tool: make
- Linting Tool: flake8
- CI/CD: GitHub Actions
- Cloud Deployment: Heroku
- Frontend: React
- Project Management: GitHub Kanban board
- Communication: Slack
