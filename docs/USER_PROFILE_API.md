# Lógica de Usuarios y Editar Perfil

Documentación corregida según la implementación real del backend.

---

## 1. URL base

Configurada en `.env`:
```
VITE_DOMAIN=127.0.0.1:8000
VITE_SSL=false
```

**Resultado:** `http://127.0.0.1:8000`

---

## 2. Endpoints utilizados

| Acción | Método | URL | Requiere token |
|--------|--------|-----|----------------|
| Login | POST | `{base}/auth/login/` | No |
| Logout | POST | `{base}/auth/logout/` | No |
| Obtener perfil actual | GET | `{base}/auth/me/` | Sí |å
| Actualizar perfil | PUT | `{base}/auth/me/` | Sí |
| Subir imagen de perfil | POST | `{base}/auth/me/profile-image` | Sí |

**Alternativa:** `PUT {base}/user/` y `GET {base}/user/{user_id}` también existen, pero para el perfil del usuario autenticado se recomienda usar `/auth/me/` (no requiere enviar `id`).

---

## 3. Estructuras de datos

### 3.1 Modelo User (dominio frontend)

```typescript
interface User {
  id: string
  email: string | null
  names: string | null
  lastnames: string | null
  name: string                    // names + lastnames o email (computado)
  document_number: string | null
  document_type: string | null
  profile_image: string | null    // ruta relativa, ej: "profile_images/profile_xxx.jpg"
  is_agent: boolean | null
  role: string | null
  phone: number | null
  code_phone: string | null
  created_at?: string
  updated_at?: string
}
```

### 3.2 Login – Request

```http
POST /auth/login/
Content-Type: application/json

{
  "username": "email@ejemplo.com",
  "password": "tu_password"
}
```

**Importante:** El backend acepta `application/json` o `application/x-www-form-urlencoded`. Si usas **form-urlencoded**, la respuesta solo incluye `access_token` y `token_type`, **no** el objeto `user`. Para obtener el perfil completo debes usar `Content-Type: application/json`.

### 3.3 Login – Response (JSON)

```json
{
  "token": "opaque-token-xxx",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "names": "Juan",
    "lastnames": "Pérez",
    "email": "email@ejemplo.com",
    "profile_image": "profile_images/profile_xxx.jpg",
    "document_number": "12345678",
    "role": "user"
  }
}
```

**Nota:** El `user` del login (UserInfoDTO) es **parcial**: no incluye `document_type`, `is_agent`, `phone`, `code_phone`, `created_at`, `updated_at`. Para el perfil completo usa `GET /auth/me/`.

### 3.4 GET /auth/me/ – Response (UserReadDTO)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "names": "Juan",
  "lastnames": "Pérez",
  "email": "email@ejemplo.com",
  "profile_image": "profile_images/profile_xxx.jpg",
  "document_number": "12345678",
  "document_type": "dni",
  "is_agent": true,
  "role": "user",
  "phone": 987654321,
  "code_phone": "pe",
  "created_at": "2025-01-15T10:00:00",
  "created_by": null,
  "updated_at": "2025-01-15T10:00:00"
}
```

### 3.5 PUT /auth/me/ – Request (recomendado)

**No requiere `id` en el body.** El backend lo obtiene del token.

```typescript
interface UpdateProfilePayload {
  names?: string
  lastnames?: string
  email?: string
  profile_image?: string | null
  document_number?: string | null
  document_type?: string | null
  is_agent?: boolean
  role?: string | null
  phone?: number | null
  code_phone?: string | null
}
```

**Ejemplo de body:**
```json
{
  "names": "Juan Carlos",
  "lastnames": "Pérez García",
  "document_number": "87654321",
  "document_type": "dni",
  "is_agent": false,
  "phone": 999888777,
  "code_phone": "pe"
}
```

Todos los campos son opcionales. Solo envía los que quieras actualizar.

### 3.6 PUT /user/ – Request (form-data)

```http
PUT /user/
Content-Type: multipart/form-data
Authorization: Bearer <token>

id: 550e8400-e29b-41d4-a716-446655440000   (requerido)
names: Juan Carlos
lastnames: Pérez García
email: nuevo@email.com
document_number: 87654321
document_type: dni
is_agent: false
role: user
phone: 999888777
code_phone: pe
profile_image: <archivo>  (opcional, .png, .jpg, .jpeg, .webp, .gif)
```

Si envías `profile_image` como archivo, se guarda automáticamente y se actualiza la ruta en el usuario.

### 3.7 POST /auth/me/profile-image – Request

```http
POST /auth/me/profile-image
Authorization: Bearer <token>
Content-Type: multipart/form-data

profile_image: <archivo>  (.png, .jpg, .jpeg, .webp, .gif)
```

**Respuesta:**
```json
{
  "profile_image": "profile_images/profile_abc123.jpg"
}
```

---

## 4. Flujo recomendado (frontend)

### 4.1 Inicio de sesión

1. Usuario envía credenciales → `POST /auth/login/` con `Content-Type: application/json`
2. Backend devuelve `{ token, user }`
3. Guardar `token` y `user` en Pinia (authStore)
4. Persistir en `localStorage` (`token`, `auth_user`)

### 4.2 Restauración al cargar la app

1. `restoreUser()` lee `token` y `auth_user` de `localStorage`
2. Si hay token, restaurar `authStore.user`
3. **Opcional pero recomendado:** `restoreSession()` hace `GET /auth/me/` para refrescar el perfil completo (incluye campos que el login no devuelve)

### 4.3 Vista de perfil (ProfileView.vue)

**Modo visualización:**
- Avatar: `{base}/media/{profile_image}` o iniciales si no hay imagen
- Campos: nombre, email, documento, rol (solo lectura)
- Botón "Editar"

**Modo edición:**
- Avatar: zona clicable para subir/cambiar foto
- Campos editables: nombres, apellidos, documento
- Email: deshabilitado
- Botones: Guardar, Cancelar

### 4.4 Guardar perfil

1. Usuario pulsa "Guardar"
2. `authStore.updateProfile({ names, lastnames, document_number, ... })`
3. **Usar `PUT /auth/me/`** con body: solo los campos enviados (sin `id`)
4. Actualizar `authStore.user` con la respuesta
5. Actualizar `localStorage`

### 4.5 Subir imagen

1. Usuario selecciona archivo (solo en modo edición)
2. `authStore.uploadProfileImage(file)`
3. `POST /auth/me/profile-image` con `FormData` (campo `profile_image`)
4. Se obtiene `profile_image` de la respuesta
5. **`PUT /auth/me/`** con body: `{ profile_image: "profile_images/profile_xxx.jpg" }`
6. Actualizar `authStore.user` y `localStorage`

---

## 5. URL de la imagen de perfil

**Lógica:** `{base}/media/{profile_image}`

- Si `profile_image` es URL absoluta (`http://` o `https://`) → usar tal cual
- Si empieza con `media/` → `{base}/{path}` (evitar duplicar `media`)
- En otros casos → `{base}/media/{path}`

**Ejemplo:** `profile_images/profile_xxx.jpg` → `http://127.0.0.1:8000/media/profile_images/profile_xxx.jpg`

**Placeholder:** Si la imagen no existe en el servidor, el backend devuelve un avatar gris por defecto (sin 404).

---

## 6. Autenticación en requests

- Header: `Authorization: Bearer <token>`
- Todas las rutas `/auth/me/*` requieren token válido

---

## 7. Manejo de errores

- **401:** El interceptor cierra sesión y redirige a `/`
- **PUT /auth/me/** y **POST profile-image:** considerar `skipAuthRedirect: true` para no cerrar sesión en 401
- **Imagen:** Si falla la carga, mostrar iniciales en lugar del avatar

---

## 8. Resumen: correcciones

| Aspecto | Antes (incorrecto) | Ahora (correcto) |
|---------|--------------------|------------------|
| Actualizar perfil | `PUT /user/` con `id` requerido | `PUT /auth/me/` sin `id` (recomendado) |
| Login response | `user` con todos los campos | `user` parcial; usar `GET /auth/me/` para perfil completo |
| Content-Type login | Cualquiera | `application/json` para obtener `user` |
| Flujo de imagen | PUT /user/ con id | PUT /auth/me/ con solo profile_image |

---

## 9. Archivos relevantes (frontend)

| Archivo | Responsabilidad |
|---------|-----------------|
| AuthApiAdapter.ts | Llamadas: login, GET /auth/me/, PUT /auth/me/, POST profile-image |
| AuthRepository.ts | Interfaces y tipos |
| useAuthStore.ts | Estado, acciones, persistencia |
| ProfileView.vue | UI de perfil y edición |
| User.ts | Modelo de dominio |
| domain.ts | URLs base y media |
| api/client.ts | Cliente HTTP, token, interceptores |
