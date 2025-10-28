# 📘 ENDPOINTS
Se omiten los endpoints de las vistas de verificacion de cuenta y recuperacion de contraseña

## `REGISTRAR USUARIO`
Recurso usado para registrar un usuario y enviar un mensaje de verificacion a su correo para validar el registro

**RUTA Y METODOS:** `/users/register (POST)`

#### CUERPO
```json
{
    "name":"string",
    "email": "string",
    "password": "string"
}
```

#### REQUISITOS: 
- password debe ser de minimo 8 caracteres
- usuario no registrado o no verificado pasado 1 semana

**RESPUESTA:** HTTP 201

---

## `LOGIN DE USUARIO`
Usado para obtener un token de verificacion para que el usuario pueda editar su cuenta, notas y carpetas

**RUTA Y METODOS:** `/users/login (POST)`

#### CUERPO
```json
{
    "email": "string",
    "password": "string"
}
```

**RESPUESTA:** 
```javascript
HTTP 200
{
    "message":"usuario validado",
    "payload":{
        "user": {id,email,name} /*datos de usuario*/,
        "token":"string",
        "root_folder": {title,id} /* folder principal del usuario */,
        
        "children":{
            /*lista de folders hijos directos del folder principal */
            "folders": [...],
            /*lista de notas hijas directos del folder principal */
            "notes":  [...],
        }
    }
}
```


## `CAMBIAR CONTRASEÑA DE USUARIO`
Usado para cambiar la contraseña de un usuario con un token de sesion activo

**RUTA Y METODOS:** `/users/password (PATH)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,

#### CUERPO ESPERADO
```json
{
    "password": "string"
}
```

#### REQUISITOS: 
- password debe ser de minimo 8 caracteres


**RESPUESTA:** HTTP 204


## `CREAR FORMULARIO DE RECUPERACION DE CONTRASEÑA`
Usado para cambiar la contraseña de un usuario que olvido su contraseña enviandole un correo con un enlace con un formulario de cambio de contraseña

**RUTA Y METODOS:** `/users/recover (POST)`

#### CUERPO
```json
{
    "email": "string"
}
```

**RESPUESTA:** HTTP 200



## `CREAR NOTA`
Usado para crear una nota mientras en una sesion

**RUTA Y METODOS:** `/notes (POST)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,

#### CUERPO
```json
{
    "message":"nota creada",
    "payload":{
        "title": "string",
        "content": "string",
        "folder_id": "int"
    }
}
```

#### REQUISITOS: 
- el folder_id debe pertenecer al usuario

**RESPUESTA:**
```javascript
HTTP 201
{
    "message":"nota creada",
    "payload":{
        "note":{...,id}
    }
}
```

## `EDITAR NOTA`
Usado para editar una nota mientras en una sesion

**RUTA Y METODOS:** `/notes/<note_id> (PATCH)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "title": "string | null",
    "content": "string | null"
}
```
#### REQUISITOS: 
- title y content son opcionales, pero no pueden faltar los 2 a la vez

**CUERPO DE RESPUESTA:**
```json
HTTP 200
{
    "message":"nota actualizada",
    "payload":{
        "updated_at": "date-time (ISO 8601 datetime)"
    }
}
```

## `MOVER NOTAS`
Usado para mover varias notas durente una sesion

**RUTA Y METODOS:** `/notes/move (PATCH)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "folder_id":"int" /*folder destino */,
    "note_ids": "list[note_id]"
}
```

**CUERPO DE RESPUESTA:**
```json
HTTP 200
{
    "message":"notas movidas correctamente",
    "payload":{
        "updated_at":"date-time (ISO 8601 datetime)"
    }
}
```

## `BORRAR NOTAS`
usado para borrar notas en una sesion

**RUTA Y METODOS:** `/notes (DELETE)`
#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "note_ids": "list[note_id]"
}
```

**CUERPO DE RESPUESTA:** HTTP 204

## `OBTENER NOTAS Y FOLDERS HIJOS DE UN FOLDER`
Usado para obener el contenido directo de un folder en una sesion

**RUTA Y METODOS:** `/folders/<folder_id>/childs (GET)`
#### ENCABEZADO
- Authorization: **Bearer < JWT >**,


**RESPUESTA:**
```json
HTTP 200
{
    "message":"contenido econtrado",
    "payload":{
        "notes":"list[note]",
        "folders":"list[note]"
    }
}
```

## `CREAR FOLDER`
Usado para crear un folder en una sesion

**RUTA Y METODOS:** `/folders (POST)`
#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "title": "string",
    "parent_folder_id":"int"
}

**RESPUESTA:**
```json
HTTP 200
{
    "message":"folder creado",
    "payload":{
        "notes":"list[note]",
        "folders":"list[note]"
    }
}
```

## `MOVER FOLDERS`
Usado para mover varios folders durente una sesion

**RUTA Y METODOS:** `/folders/move (PATCH)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "folder_id":"int" /*folder destino */,
    "folder_ids": "list[folder_id]"
}
```
**CUERPO DE RESPUESTA:**
```json
HTTP 200
{
    "message":"folder movido",
    "payload":{
        "updated_at":"date-time (ISO 8601 datetime)"
    }
}
```


## `RENOMBRAR FOLDER`
Usado para cambiar el titulo de un folder durente una sesion

**RUTA Y METODOS:** `/folders/<folder_id>/rename (PATCH)`

#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "folder_id":"int" /*folder destino */,
    "folder_ids": "list[folder_id]"
}
```
**CUERPO DE RESPUESTA:**
```json
HTTP 200
{
    "message":"folder renombrado",
    "payload":{
        "updated_at":"date-time (ISO 8601 datetime)"
    }
}
```

## `BORRAR FOLDERS`
usado para borrar folders de un usuario en una sesion

**RUTA Y METODOS:** `/folders (DELETE)`
#### ENCABEZADO
- Authorization: **Bearer < JWT >**,
#### CUERPO
```json
{
    "folder_ids": "list[folder_id]"
}
```
**CUERPO DE RESPUESTA:** HTTP 204