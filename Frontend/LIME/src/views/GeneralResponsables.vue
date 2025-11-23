<script>
</script>
<template>
<div class="background"> 
    <!-- Barra lateral izquierda -->
    <div class="slidebar"></div>
    <!-- Contenedor principal -->
    <div class="menuPrincipal">
        <!-- Barra superior de navegación -->
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones" @click="$router.push('/')">Equipos</button>
            <button class="navbar--opciones" @click="$router.push('/Responsables')">Responsables</button>
            <button class="navbar--opciones" @click="$router.push('/Servicios')">Servicios</button>
        </div>
        <div class="menuPrincipal--tablaPrincipal--responsables">
            <div class="responsables--listacontenedor">
                
            </div>
        </div>
    </div>
</div>
</template>
<style>
    .menuPrincipal--tablaPrincipal--responsables{
        margin: 2% 2%;
        box-sizing: border-box;
        width: 96%;
        height: 84%;
        background-color: #f7f7f7a1;
        display:flex;
        flex-direction: row;
        align-items: center;
        overflow-x: scroll;
        border-radius: 12px 12px 12px 12px;
        box-shadow: 2px 3px 3px rgba(0, 0, 0, 0.15), -2px -3px 3px rgba(0, 0, 0, 0.15);
    }
</style>