# **Manual de Usuario - Sistema de Gestión Logística (DjangoERP)**

## Índice

- [1. Introducción](#1-introducción)
  - [1.1. Propósito](#11-propósito)

- [2. Requisitos del sistema](#2-requisitos-del-sistema)

- [3. Inicio de sesión y roles de usuario](#3-inicio-de-sesión-y-roles-de-usuario)
  - [3.1. Acceso al sistema](#31-acceso-al-sistema)
    - [3.1.1. Registro de usuario](#311-registro-de-usuario)
    - [3.1.2. Inicio de sesión](#312-inicio-de-sesión)
  - [3.2. Creación de usuarios con roles de trabajo (Superusuario y panel de administración)](#32-creación-de-usuarios-con-roles-de-trabajo-superusuario-y-panel-de-administración)
    - [3.2.1. Crear un superusuario](#321-crear-un-superusuario)
    - [3.2.2. Gestionar usuarios desde el panel de administración](#322-gestionar-usuarios-desde-el-panel-de-administración)
  - [3.3. Roles de usuario](#33-roles-de-usuario)
  - [3.4. Cerrar sesión](#34-cerrar-sesión)

- [4. Guía de uso](#4-guía-de-uso)
  - [4.1. Gestión de Inventario (Encargado de Inventario y Gerente)](#41-gestión-de-inventario-encargado-de-inventario-y-gerente)
    - [4.1.1. Ver el inventario](#411-ver-el-inventario)
    - [4.1.2. Añadir un producto](#412-añadir-un-producto)
    - [4.1.3. Editar un producto](#413-editar-un-producto)
    - [4.1.4. Eliminar un producto](#414-eliminar-un-producto)
    - [4.1.5. Registrar un pedido](#415-registrar-un-pedido)
    - [4.1.6. Recibir stock](#416-recibir-stock)
    - [4.1.7. Descargar registros](#417-descargar-registros)
  - [4.2. Gestión de Contabilidad (Contable y Gerente)](#42-gestión-de-contabilidad-contable-y-gerente)
    - [4.2.1. Ver el estado financiero](#421-ver-el-estado-financiero)
    - [4.2.2. Descargar historial de transacciones](#422-descargar-historial-de-transacciones)
  - [4.3. Informes (Gerente)](#43-informes-gerente)
    - [4.3.1. Acceder a la página de Gerente](#431-acceder-a-la-página-de-gerente)
    - [4.3.2. Descripción de la vista](#432-descripción-de-la-vista)
    - [4.3.3. Descargar informes](#433-descargar-informes)

- [5. Preguntas frecuentes (FAQ)](#5-preguntas-frecuentes-faq)
  - [5.1. ¿Qué sucede con los datos antiguos?](#51-qué-sucede-con-los-datos-antiguos)
  - [5.2. ¿Puedo descargar informes de períodos más largos?](#52-puedo-descargar-informes-de-períodos-más-largos)
  - [5.3. ¿Qué hago si no puedo acceder a una sección?](#53-qué-hago-si-no-puedo-acceder-a-una-sección)
  
- [6. Solución de problemas](#6-solución-de-problemas)
  - [6.1. No puedo iniciar sesión](#61-no-puedo-iniciar-sesión)
  - [6.2. El dropdown no funciona](#62-el-dropdown-no-funciona)
  - [6.3. No se descargan los informes](#63-no-se-descargan-los-informes)




## **1. Introducción**
**DjangoERP** es un sistema de gestión logística diseñado para facilitar la administración de inventarios, contabilidad y generación de informes en una empresa. Este software permite a los usuarios gestionar productos, registrar movimientos de stock, realizar pedidos, controlar el presupuesto y generar informes detallados, todo desde una interfaz web intuitiva.

### **1.1. Propósito**
El propósito de este sistema es optimizar las operaciones logísticas, proporcionando herramientas para:
- Gestionar el inventario de productos.
- Registrar transacciones financieras.
- Generar informes de movimientos y estados financieros.
- Automatizar tareas como la limpieza de datos antiguos.

---

## **2. Requisitos del sistema**
Para usar DjangoERP, necesitas:
- Un navegador web moderno (Google Chrome, Firefox, Edge, etc.).
- Acceso a internet.
- Credenciales de usuario proporcionadas por el administrador del sistema.
- Permisos adecuados según tu rol (Encargado de Inventario, Contable o Gerente).

---

## **3. Inicio de sesión y roles de usuario**

### **3.1. Acceso al sistema**
1. Inicia el servidor de DjangoERP ejecutando el comando `python manage.py runserver` desde la terminal, en la carpeta donde se encuentra el archivo `manage.py`.
2. Abre tu navegador y accede a la ruta principal del sistema: `/Logistics/` (por ejemplo, `http://localhost:8000/Logistics/`).
3. En esta vista principal, puedes:
   - **Iniciar sesión** si ya tienes una cuenta.
   - **Registrarte** como nuevo usuario.

#### **3.1.1. Registro de usuario**
1. En la página principal (`/Logistics/`), haz clic en la opción **Registrarse**.
2. Completa el formulario de registro con los siguientes datos:
   - Nombre
   - Correo electrónico
   - Teléfono
   - Contraseña (deberás confirmarla ingresándola dos veces)
3. Haz clic en **Registrar**.
   - Si el registro es válido, tu usuario será guardado en la base de datos con el rol por defecto **Cliente**.
   - Serás redirigido a la página de inicio de sesión.

#### **3.1.2. Inicio de sesión**
1. En la página principal (`/Logistics/`), ingresa tu nombre de usuario (o correo) y contraseña.
2. Haz clic en **Iniciar sesión**.
   - Si las credenciales son correctas, serás redirigido a una vista personalizada según tu rol.

### **3.2. Creación de usuarios con roles de trabajo (Superusuario y panel de administración)**

Para crear usuarios con roles específicos (como Encargado de Inventario, Contable o Gerente), debes crear un superusuario y usar el panel de administración.

#### **3.2.1. Crear un superusuario**
1. Abre el **Símbolo del sistema (CMD)** en Windows:
   - Escribe "CMD" en el buscador de Windows y presiona Enter.
2. Navega a la carpeta del proyecto donde se encuentra el archivo `manage.py`:
   - Usa el comando `cd` para moverte a la ruta del programa (por ejemplo, `cd C:\ruta\al\proyecto`).
3. Ejecuta el siguiente comando para crear un superusuario: `python manage.py createsuperuser`
4. Sigue las instrucciones en pantalla para asignar:
- Correo electrónico
- Nombre de usuario
- Contraseña
5. Una vez creado, el superusuario tendrá acceso completo al sistema.

#### **3.2.2. Gestionar usuarios desde el panel de administración**
1. Con el servidor en ejecución, abre tu navegador y escribe en la URL: `/Logistics/admin/` (por ejemplo, `http://localhost:8000/Logistics/admin/`).
2. Inicia sesión con las credenciales del superusuario que acabas de crear.
3. En el panel de administración, busca la tabla **User** (Usuarios).
4. Haz clic en **Añadir usuario** para crear un nuevo usuario:
- Ingresa el nombre, correo, teléfono y contraseña.
- Asigna un rol específico (Cliente, Encargado de Inventario, Contable o Gerente).
5. Guarda el usuario.
- El nuevo usuario podrá iniciar sesión y acceder a las funcionalidades según su rol.

### **3.3. Roles de usuario**
Cada rol tiene una vista personalizada con funciones específicas:
- **Cliente**: Rol por defecto al registrarse. Tiene acceso limitado (puede ver información básica, pero no gestionar inventario ni finanzas).
- **Encargado de Inventario**: Gestiona productos, stock y pedidos.
- **Contable**: Administra el presupuesto y registra transacciones.
- **Gerente**: Supervisa el inventario, las finanzas y genera informes completos.

### **3.4. Cerrar sesión**
1. En la barra superior de cualquier vista, haz clic en tu nombre de usuario.
2. Selecciona **Cerrar sesión** en el menú desplegable.

---

## **4. Guía de uso**

### **4.1. Gestión de Inventario (Encargado de Inventario y Gerente)**

#### **4.1.1. Ver el inventario**
1. Inicia sesión como Encargado de Inventario o Gerente.
2. Serás redirigido a la página de Inventario (`/Logistics/inventario/`).
3. La tabla muestra todos los productos con los siguientes detalles:
- ID
- Nombre
- Descripción
- Precio
- Stock
- Imagen
- Acciones (editar/eliminar, solo para Encargado de Inventario).

#### **4.1.2. Añadir un producto**
1. Haz clic en el botón **Añadir Producto**.
2. Se abrirá un formulario.
3. Completa los campos:
- Nombre (obligatorio)
- Descripción (opcional)
- Precio (obligatorio)
- Stock (obligatorio)
- Imagen (opcional pero recomendado)
4. Haz clic en **Guardar**.
- Si el producto se añade correctamente, aparecerá un mensaje de éxito y se actualizará la tabla.

#### **4.1.3. Editar un producto**
1. En la tabla de productos, haz clic en **Editar** en la fila del producto que deseas modificar.
2. Se abrirá un formulario con los datos actuales del producto.
3. Modifica los campos necesarios.
4. Haz clic en **Guardar Cambios**.
- El producto se actualizará y aparecerá un mensaje de éxito.

#### **4.1.4. Eliminar un producto**
1. En la tabla de productos, haz clic en **Eliminar** en la fila del producto.
2. Confirma la eliminación en la ventana emergente.
- El producto será eliminado y la tabla se actualizará.

#### **4.1.5. Registrar un pedido**
1. Haz clic en el botón **Pedidos**.
2. En la vista de Pedidos, haz clic en el botón **Añadir Pedido**.
3. Selecciona los productos que deseas incluir usando el campo de búsqueda.
4. Especifica la cantidad para cada producto seleccionado.
5. (Opcional) Añade una descripción del pedido.
6. Haz clic en **Confirmar Pedido**.
- El pedido se registrará y el stock de los productos se actualizará.

#### **4.1.6. Recibir stock**
1. Haz clic en el botón **Recibir Stock**.
2. Selecciona los productos que deseas añadir al inventario.
3. Especifica la cantidad para cada producto.
4. Haz clic en **Confirmar Recepción**.
- El stock de los productos seleccionados se actualizará.

#### **4.1.7. Descargar registros**
- **Registro de Movimientos**:
1. Haz clic en el botón **Registro de Movimientos**.
2. Selecciona un período en el menú desplegable:
  - Últimas 24 horas
  - Últimos 3 días
  - Última semana
3. Se descargará un PDF con los movimientos de stock del período seleccionado.
- **Registro de Inventario**:
1. Haz clic en el botón **Registro de Inventario**.
2. Se descargará un PDF con el estado actual del inventario.

---

### **4.2. Gestión de Contabilidad (Contable y Gerente)**

#### **4.2.1. Ver el estado financiero**
1. Inicia sesión como Contable o Gerente.
2. Serás redirigido a la página de Contabilidad (`/Logistics/contabilidad/`).
3. Selecciona una de las opciones:
- **Saldo**: Muestra el monto actual del presupuesto.
- **Movimientos**: Muestra una tabla con las transacciones (fecha, tipo, monto, descripción, ID de pedido).
- **Ganancias**: Muestra las ganancias o pérdidas totales desde el inicio.

#### **4.2.2. Descargar historial de transacciones**
1. Haz clic en el botón **Descargar Historial**.
2. Selecciona un período en el menú desplegable:
- Últimas 24 horas
- Últimos 3 días
- Última semana
3. Se descargará un PDF con el historial de transacciones del período seleccionado.

---

### **4.3. Informes (Gerente)**

#### **4.3.1. Acceder a la página de Gerente**
1. Inicia sesión como Gerente.
2. Serás redirigido a la página de Gerente (`/Logistics/gerente/`).

#### **4.3.2. Descripción de la vista**
En esta vista tendrás la opción de navegar entre las vistas de los otros roles, pudiendo supervisar los datos pertinentes de cada departamento. Además:

#### **4.3.3. Descargar informes**
1. En la sección "Informes", haz clic en el botón **Descargar Informes**.
2. Selecciona un período en el menú desplegable:
- Últimas 24 horas
- Últimos 3 días
- Última semana
3. Se descargará un archivo ZIP que contiene:
- Historial de transacciones (PDF)
- Registro de inventario (PDF)
- Registro de movimientos de stock (PDF)

---

## **5. Preguntas frecuentes (FAQ)**

### **5.1. ¿Qué sucede con los datos antiguos?**
El sistema realiza una limpieza automática mensual, eliminando transacciones y movimientos de stock con más de 30 días de antigüedad. Esto asegura que la base de datos no crezca indefinidamente.

### **5.2. ¿Puedo descargar informes de períodos más largos?**
Actualmente, los informes están limitados a períodos de 24 horas, 3 días o 1 semana. Si necesitas un informe más extenso, contacta al administrador del sistema.

### **5.3. ¿Qué hago si no puedo acceder a una sección?**
Verifica que tu rol tenga los permisos necesarios. Por ejemplo, solo los Gerentes pueden acceder a la sección de informes. Si el problema persiste, contacta al administrador.

---

## **6. Solución de problemas**

### **6.1. No puedo iniciar sesión**
- Asegúrate de que tu nombre de usuario y contraseña sean correctos.
- Verifica que tu cuenta esté activa (contacta al administrador si no estás seguro).

### **6.2. El dropdown no funciona**
- Asegúrate de que estás usando un navegador compatible y que JavaScript está habilitado.
- Borra la caché del navegador y vuelve a intentarlo.

### **6.3. No se descargan los informes**
- Verifica que haya datos disponibles para el período seleccionado.
- Asegúrate de que tu navegador permita descargas automáticas.

---

