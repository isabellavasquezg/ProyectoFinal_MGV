<script>
</script>
<template>
<div class="background"> 
    <div class="slidebar">
    </div>
    <div class="menuPrincipal">
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones">General</button>
            <button class="navbar--opciones">Registro Historico</button>
            <button class="navbar--opciones">Información Metrologica</button>
            <button class="navbar--opciones">Documentación</button>
            <button class="navbar--opciones">Información Técnica</button>
        </div>
        <div class="menuPrincipal--tablaPrincipal">
            <div class="tablaPrincipal--filtros">
                <form class="tablaPrincipal--formFiltros">
                    <input class="filtros--inputs" type="text" placeholder="Sede" />
                    <input class="filtros--inputs" type="text" placeholder="Servicio" />
                    <input class="filtros--inputs" type="text" placeholder="Serie" />
                    <input class="filtros--inputs" type="text" placeholder="Marca" />
                    <input class="filtros--inputs" type="text" placeholder="Modelo" />
                    <input class="filtros--inputs" type="text" placeholder="Estado" />
                    <input class="filtros--inputs" type="text" placeholder="Nombre Equipo" />
                    <button type="submit">Filtrar</button>
                </form>
                <div class="menubotones">
                        <button type="button">Agregar</button>
                        <button type="button">Eliminar</button>
                </div>
            </div>
            <div class="contenedorTabla">
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
    .slidebar{
        background-color: #0a346c;
        width: 13%;
        height: 100%;
    }
    .menuPrincipal{
        width: 87%;
        height: 100%;
        display:flex;
        flex-direction: column;
    }
    .menuPrincipal--navbar{
        padding-left: 20%;
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
    .menuPrincipal--tablaPrincipal{
        margin: 2% 2%;
        margin-top: 1%;
        box-sizing: border-box;
        width: 96%;
        height: 90%;
        background-color: #ffffff;
        border-radius: 10px;
        display:flex;
        flex-direction: column;
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
    .contenedorTabla{
        height: 85%;
        width: 100%;
    }
</style>