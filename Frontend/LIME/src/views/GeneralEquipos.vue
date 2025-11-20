<script>
import axios from "axios";
// Importamos los componentes que usa esta vista
import TablasEquipos from '../components/TablasEquipos.vue';
import FiltrosMenu from '../components/FiltrosMenu.vue';

export default {

    // Registramos los componentes
    components: {
        FiltrosMenu,
        TablasEquipos
    },

    name: "GeneralEquipos",

    data() {
        return {
            seccion:"General",
            filas: [],
            nombre:"equipos"
        };
    },

    methods: {
        async listarEquipos(nombre) {
            try {
                const res = await axios.get(`http://127.0.0.1:8000/api/${nombre}/`);
                this.filas = res.data.result;
            } catch (err) {
                console.error(err);
                alert("Error al listar equipos");
            }
        },
        cambiarSeccion(seccionNueva){
            this.seccion = seccionNueva;
        }
    },
    mounted() {
        this.listarEquipos(this.nombre);
    },
};
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
                <button class="secciones--botones" @click="cambiarSeccion('General'); listarEquipos('equipos')">General</button>
                <button class="secciones--botones" @click="cambiarSeccion('Registro'); listarEquipos('registros')">Registro Historico</button>
                <button class="secciones--botones" @click="cambiarSeccion('MetrologiaA'); listarEquipos('metrologiaA')">Metrologia administrativa</button>
                <button class="secciones--botones" @click="cambiarSeccion('MetrologiaT'); listarEquipos('metrologiaT')">Metrologia Tecnica</button>
                <button class="secciones--botones" @click="cambiarSeccion('Documentacion'); listarEquipos('documentos')">Documentación</button>
                <button class="secciones--botones" @click="cambiarSeccion('Condicion'); listarEquipos('condicion')">Coondicion Funcionamiento</button>
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
                        <button class="menuBotones--botones" type="button">Eliminar</button>
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
    /* Estilos base */
    body{
        margin: 0;
        font-family: sans-serif;
    }

    /* Fondo general del layout */
    .background{
        background-color: #eeeeee;
        height: 100vh;
        width: 100vw;
        display:flex;
        flex-direction: row;
    }

    /* Barra lateral izquierda */
    .slidebar{
        background-color: #0a346c;
        width: 7%;
        height: 100%;
    }

    /* Contenedor principal */
    .menuPrincipal{
        width: 93%;
        height: 100%;
        display:flex;
        flex-direction: column;
    }

    /* Navbar superior */
    .menuPrincipal--navbar{
        padding-left: 35%;
        box-sizing: border-box;
        background-color: #ffffffbb;
        height: 7%;
        width: 100%;
        align-items: center;
        box-shadow: 0px 8px 10px -5px rgba(0, 0, 0, 0.2);
        display:flex;
        flex-direction: row;
    }

    /* Botones de navegación */
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

    /* Contenedor principal donde va tabla y filtros */
    .menuPrincipal--tablaPrincipal{
        margin: 2% 2%;
        margin-top: 0;
        box-sizing: border-box;
        width: 96%;
        height: 84%;
        background-color: #ffffff;
        display:flex;
        flex-direction: column;
    }

    /* Botones para cambiar sección */
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

    /* Contenedor de filtros */
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

    /* Contenedor de botones de acciones */
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

    /* Contenedor de la tabla */
    .tablaPrincipal--contenedor{
        height: 85%;
        width: 100%;
        overflow-x: auto; 
        max-height: 100%;
    }
</style>
