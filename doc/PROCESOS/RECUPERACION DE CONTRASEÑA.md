sequenceDiagram
    title RECUPERACION DE CUENTA

    participant C as API Consumer
    participant A as API
    participant DB@{ "type" : "database" }
    C->>+A: POST /users/recover <br> { email }

    A->>A: enviar correo con <br> token y enlace de verificacion
    A-->>-C: HTTP 200 <br> correo enviado

    C-->>C: Abrir correo enviado
    C->>+A: GET /recover?token

    A->>A: verificar token
    break token invalido o <br> con 1 dia de antiguedad
        A-->>C: HTTP 400 <br> vista(recover.html) <br> token invalido
    end

    A-->>-C: HTTP 200 <br> formulario(recover.html)

    C->>C: rellena el formulario y enviar

    C->>+A: PATCH /user/recover-password <br> {token,password}

    A->>A: verificar token
    break token invalido o <br> con 1 dia de antiguedad
        A-->>C: HTTP 400 <br> token invalido
    end

    A-->>+DB: actualizar contraseña
    DB-->>-A:  {numero de filas actualizadas}
    A-->>-C: HTTP 204