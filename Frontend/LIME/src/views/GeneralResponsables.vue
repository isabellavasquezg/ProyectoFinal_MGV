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
        <!-- Botones para cambiar entre secciones -->
        <div class="menuPrincipal--secciones">
                <button class="secciones--botones" :class="{ 'active': seccion === 'General' }"  @click="cambiarSeccion('General'); listarEquipos()">General</button>
                <button class="secciones--botones" :class="{ 'active': seccion === 'Registro' }" @click="cambiarSeccion('Registro'); listarEquipos()">Registro Historico</button>
                <button class="secciones--botones" :class="{ 'active': seccion === 'MetrologiaA' }" @click="cambiarSeccion('MetrologiaA'); listarEquipos()">Metrologia Administrativa</button>
                <button class="secciones--botones" :class="{ 'active': seccion === 'MetrologiaT' }" @click="cambiarSeccion('MetrologiaT'); listarEquipos()">Metrologia Tecnica</button>
                <button class="secciones--botones" :class="{ 'active': seccion === 'Documentacion' }" @click="cambiarSeccion('Documentacion'); listarEquipos()">Documentación</button>
                <button class="secciones--botones" :class="{ 'active': seccion === 'Condicion' }" @click="cambiarSeccion('Condicion'); listarEquipos()">Coondicion Funcionamiento</button>
        </div>
        <!-- Contenedor principal de tabla + filtros -->
        <div class="menuPrincipal--tablaPrincipal">
            <!-- Filtros y botones laterales -->
            <div class="tablaPrincipal--filtros">
                <!-- Componente de filtros dinámico por sección -->
                <FiltrosMenu :seccion="seccion" />
                <!-- Botones de acciones (agregar y eliminar) -->
                <div class="tablaPricipal--menuBotones">
                        <button class="menuBotones--botones" type="button">Agregar</button>
                        <button class="menuBotones--botones" type="button">Desactivar</button>
                </div>
            </div>
            <!-- Contenedor donde se muestra la tabla -->
            <div class="tablaPrincipal--contenedor">
                <TablasEquipos :seccion="seccion" :filas="filas" />    
            </div>

        </div>
    </div>
</div>
</template>
<style>
</style>