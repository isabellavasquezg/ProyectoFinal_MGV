<script>
</script>
<template>
<div class="background"> 
    <div class="slidebar">
    </div>
    <div class="menuPrincipal">
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones" @click="$router.push('/')">Equipos</button>
            <button class="navbar--opciones" @click="$router.push('/Responsables')">Responsables</button>
            <button class="navbar--opciones" @click="$router.push('/Servicios')">Servicios</button>
        </div>
        <div class="menuPrincipal--tablaPrincipal">
            <div class="tablaPrincipal--filtros">
                <form class="tablaPrincipal--formFiltros">
                    <input class="filtros--inputs" type="text" placeholder="Sede" />
                    <input class="filtros--inputs" type="text" placeholder="Servicio" />
                    <input class="filtros--inputs" type="text" placeholder="Ubicación Sede" />
                    <button class="filtros--boton" type="submit">Filtrar</button>
                </form>
                <div class="tablaPricipal--menuBotones">
                        <button class="menuBotones--botones" type="button">Agregar</button>
                        <button class="menuBotones--botones" type="button">Eliminar</button>
                </div>
            </div>
            <div class="tablaPrincipal--contenedor">
                                <table class="tabla">
                    <thead>
                        <tr class="tabla--header">
                            <th class="tabla--headersCheck">
                                <input id="checkHeader" type="checkbox" />
                            </th>
                            <th class="tabla--headers">Nombre de Sede</th>
                            <th class="tabla--headers">Telefono Sede</th>
                            <th class="tabla--headers">Servicio</th>
                            <th class="tabla--headers">Ubicación Sede</th>
                            <th class="tabla--headers">Cantidad de Servicios</th>
                            <th class="tabla--headers">Acciones</th>
                        </tr> 
                    </thead>
                    <tbody>
            
                        <tr class="tabla--fila">
                            <td><input class="checkRow" type="checkbox" /></td>
                            <td>A</td>
                            <td>Medio</td>
                            <td>2020INV-123</td>
                            <td>Activo</td>
                            <td>WS</td>
                            <td><button>Actualizar</button></td>
                        </tr>

                    
                        <tr class="tabla--fila">
                            <td><input class="checkRow"type="checkbox" /></td>
                            <td>Media</td>
                            <td>B</td>
                            <td>Bajo</td>
                            <td>2021INV-442</td>
                            <td>WS</td>
                            <td><button>Actualizar</button></td>
                        </tr>
                    </tbody>
                </table>     
            </div>
        </div>
    </div>
</div>
</template>
<style>
    body{
        margin: 0;
        font-family: sans-serif;
    }
    .background{
        background-color: #eeeeee;
        height: 100vh;
        width: 100vw;
        display:flex;
        flex-direction: row;
    }
    /*------------------Slidebar------------------- */
    .slidebar{
        background-color: #0a346c;
        width: 7%;
        height: 100%;
    }
    /*------------------Menu Principal------------------- */
    .menuPrincipal{
        width: 93%;
        height: 100%;
        display:flex;
        flex-direction: column;
    }
    /*------------------Navbar------------------- */
    .menuPrincipal--navbar{
        padding-left: 30%;
        box-sizing: border-box;
        background-color: #ffffffbb;
        height: 7%;
        width: 100%;
        align-items: center;
        box-shadow: 0px 8px 10px -5px rgba(0, 0, 0, 0.2);
        display:flex;
        flex-direction: row;
    }
    .navbar--opciones{
        background-color: transparent;
        color: #0a346c;
        border: none;
        font-size: 16px;
        margin-left: 20px;
        cursor: pointer;
        padding: 10px 15px;
        transition: background-color 0.3s, color 0.3s;
    }
    .navbar--opciones:hover{
        border-bottom: 2px solid #00a89d;
    }
    .navbar--opciones:active{
        transform: scale(0.98);
    }
    /*------------------Tabla Principal------------------- */
    .menuPrincipal--tablaPrincipal{
        margin: 2% 2%;
        box-sizing: border-box;
        width: 96%;
        height: 84%;
        background-color: #ffffff;
        display:flex;
        flex-direction: column;
    }
    .menuPrincipal--secciones{
        border-radius: 10px 10px 0 0;
        margin: 0 2%;
        margin-top:1%;
        box-sizing: border-box;
        height: 6%;
        width: 96%;
        background-color: #ffffff;
        display:flex;
        flex-direction: row;
        align-items: center;
    }
    .secciones--botones{
        padding: 0 2%;
        height: 100%;
        border-radius: 5px 10px 0 0;
        border:none;
        background-color: #ffffff;
        color:#00a89d;
    }
    .secciones--botones:first-child{
        border-radius: 10px 10px 0 0;
    }
    .secciones--botones:hover{
        color: #ffffff;
        background-color: #00a89d;
    }
    .secciones--botones:active{
        transform: scale(0.98);
    }
    .tablaPrincipal--filtros{
        padding-left: 3%;
        height: 15%;
        width: 100%;
        box-sizing: border-box;
        border-bottom: 1px solid #cccccc;
        display:flex;
        flex-direction: row;
        align-items: center;
    }
    .tablaPrincipal--formFiltros{
        height: 60%;
        width: 80%;
        display:flex;
        flex-direction: row;
        align-items: center;
    }
    .filtros--inputs{
        font-size: 13px;
        margin-right:1%;
        width: 18%;
        border: none;
        border-bottom: 1px solid #cccccc;
    }
    .filtros--inputs:focus{
        outline: none;
        border-bottom: 1px solid #00a89d;
    }
    .filtros--boton{
        border-radius: 5px;
        height: 50%;
        background-color: #00a89d;
        margin-left: 2%;
        color: #ffffff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.1s;
    }
    .filtros--boton:hover{
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .filtros--boton:active{
        transform: scale(0.98);
    }
    .tablaPricipal--menuBotones{
        width: 20%;
        height: 60%;
        display:flex;
        flex-direction: column;
        align-items: center;
    }
    .menuBotones--botones{
        width: 40%;
        height: 40%;
        margin-bottom:2%;
        border-radius: 5px;
        background-color: #00a89d;
        color: #ffffff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.1s;
    }
    .menuBotones--botones:hover{
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .menuBotones--botones:active{
        transform: scale(0.98);
    }
    .tablaPrincipal--contenedor{
        height: 85%;
        width: 100%;
    }
            /* --- Tabla general --- */
    .tabla {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 12px;
    }

    /* --- Encabezado --- */
    .tabla--header {
        background-color: #0a346c; /* azul oscuro elegante */
        color: white;
        text-align: left;
    }

    .tabla--headers,
    .tabla--headersCheck {
        padding: 10px 8px;
        border-bottom: 2px solid #0a2540;
        font-weight: bold;
    }

    /* --- Filas del cuerpo --- */
    .tabla--fila td {
        background-color: white;
        color: #555; 
        padding: 8px 6px;
        border-bottom: 1px solid #e5e5e5;
    }

    /* --- Hover en filas --- */
    .tabla--fila:hover td {
        background-color: #f5f7fa;
    }

    /* --- Checkbox alineado --- */
    .tabla input[type="checkbox"] {
        width: 16px;
        height: 16px;
        cursor: pointer;
    }
</style>