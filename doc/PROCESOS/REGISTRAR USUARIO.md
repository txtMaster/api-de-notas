sequenceDiagram
    title REGISTRO DE USUARIO

    participant C as API Consumer
    participant A as API
    participant DB@{ "type" : "database" }
    C->>+A: POST /users/register <br> {user, email, password}

    A->>A: encriptar password
    

    A->>+DB: buscar usuario por email
    DB-->>-A: {user_id, is_verified, updated_at}
    

    break usuario ya registrado y verifcado
        A-->>C: HTTP 400 <br> usuario ya registrado
    end
    break usuario registrado no verficado, <br> y creado en menos de 1 semana
        A-->>C: HTTP 400 <br> se intento registras hace poco, <br> intentelo en 1 semana
    end

    alt usuario registrado no verificado <br> creado hace mas de 1 semana
        A->>+DB: actualizar usuario
    else 
        A->>+DB: insertar usuario
    end
    DB-->>-A: {user_id}

    A->>A: enviar correo con <br> token y enlace de verificacion
    A-->>-C: HTTP 201 <br> correo enviado
    
    C->>C: Abrir correo enviado
    C-->>+A: GET /user/verify?token <br> abrir enlace de verificacion

    A->>A: verificar token y <br> obtener datos de usuario

    break token invalido
        A-->>C: HTTP 400 <br> vista(token invalido)
    end
    break token de mas de 1 hora de antiguedad
        A-->>C: HTTP 400 <br> vista(token expirado)
    end
    
    A->>+DB: actualizar usuario <br> como verificado
    DB-->>-A: {numero de registros actualizados}

    A-->>-C: HTTP 200 <br> vista(usuario verificado)


    