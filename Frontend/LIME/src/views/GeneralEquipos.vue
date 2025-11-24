<script>
import axios from "axios";
// Importamos los componentes que usa esta vista
import FormulariosEquipos from "../components/FormulariosEquipos.vue";
import TablasEquipos from '../components/TablasEquipos.vue';
import FiltrosMenu from '../components/FiltrosMenu.vue';

export default {

    // Registramos los componentes
    components: {
        FormulariosEquipos,
        FiltrosMenu,
        TablasEquipos
    },

    name: "GeneralEquipos",

    data() {
        return {
            seccion:"General",
            filas: [],
            estadoAgregar:false,

            // Filtros que siempre estarán disponibles
            filtrosActuales: {
                sede: '',
                servicio: '',
                numeroSerie: '',
                dinamico1: '',
                dinamico2: '',
                dinamico3: '',
            }
        };
    },

    methods: {

        // Método que lista equipos con filtros o sin filtros
        async listarEquipos(filtros) {

            const filtrosAUsar = filtros || this.filtrosActuales;

            // Verifica si todos los filtros están vacíos
            const todosVacios = Object.values(filtrosAUsar).every(v => v === "");

            // Crear URL base sin parámetros
            let url = `http://127.0.0.1:8000/api/${this.seccion}/`;

            // Si hay filtros → agregarlos
            if (!todosVacios) {
                const params = new URLSearchParams({
                    sede: filtrosAUsar.sede,
                    servicio: filtrosAUsar.servicio,
                    serie: filtrosAUsar.numeroSerie,
                    f1: filtrosAUsar.dinamico1,
                    f2: filtrosAUsar.dinamico2,
                    f3: filtrosAUsar.dinamico3,
                }).toString();

                url += `?${params}`;
            }

            try {
                const res = await axios.get(url);
                this.filas = res.data.result;
            } catch (err) {
                console.error(err);
                alert("Error al listar equipos");
            }
        },
        toggleAgregar(){
            this.estadoAgregar=!this.estadoAgregar

        },
        // Manejar filtros emitidos desde el componente hijo
        filtrarEquipos(nuevosFiltros) {

            // Guardar los filtros recibidos
            this.filtrosActuales = nuevosFiltros;

            // Ejecutar búsqueda con ellos
            this.listarEquipos(nuevosFiltros);
        },

        // Cambio de sección
        cambiarSeccion(seccionNueva) {

            // Actualizamos la nueva sección de API
            this.seccion = seccionNueva;

            // Solo limpiar los filtros dinámicos
            this.filtrosActuales = {
                ...this.filtrosActuales,  // conserva sede, servicio, serie
                dinamico1: '',
                dinamico2: '',
                dinamico3: '',
            };
            if (this.estadoAgregar===true){
                 this.estadoAgregar=false
            }
           

            // Nueva consulta con los filtros persistentes
            this.listarEquipos(this.filtrosActuales);
        }
    },

    mounted() {
        this.listarEquipos();
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
                <FiltrosMenu :seccion="seccion" @aplicar-filtros="filtrarEquipos"/>
                <!-- Botones de acciones (agregar y eliminar) -->
                <div class="tablaPricipal--menuBotones">
                        <button class="menuBotones--botones agregar" :class="{ 'activate': estadoAgregar === true }" type="button" @click="toggleAgregar()"></button>
                        <button class="menuBotones--botones"  type="button">Desactivar</button>
                </div>
            </div>
            <!-- Contenedor donde se muestra la tabla -->
            <div class="tablaPrincipal--contenedor" v-if="estadoAgregar===false">
                <TablasEquipos :seccion="seccion" :filas="filas" />    
            </div>
            <div class="tablaPrincipal--contenedor" v-if="estadoAgregar===true">  
                <FormulariosEquipos :seccion="seccion"/>
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
        background-color: #ffffff;
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
    /*-----INICIO NAVBAR MENU----------*/ 
    /* Navbar superior */
    .menuPrincipal--navbar{
        padding-left: 35%;
        box-sizing: border-box;
        background-color: #f7f7f7a1;
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
    }

    .navbar--opciones:hover{
        border-bottom: 2px solid #00a89d;
    }

    .navbar--opciones:active{
        transform: scale(0.95);
    }
    /*-----FIN NAVBAR MENU----------*/ 


    /* Contenedor principal donde va tabla y filtros */
    .menuPrincipal--tablaPrincipal{
        margin: 2% 2%;
        margin-top: 0;
        box-sizing: border-box;
        width: 93%;
        height: 84%;
        background-color: #f7f7f7a1;
        display:flex;
        flex-direction: column;
        border-radius: 0 12px 12px 12px;
        box-shadow: 2px 3px 3px rgba(0, 0, 0, 0.15), -2px 0 3px rgba(0, 0, 0, 0.15);
    }

    /*-----INICIO SECCIONES DE CARPETA MENU --------*/
    /* Botones para cambiar sección */
    .menuPrincipal--secciones{
        border-radius: 10px 10px 0 0;
        margin: 0 2%;
        margin-top:1%;
        box-sizing: border-box;
        height: 6%;
        width: 96%;
        background-color: transparent;
        display:flex;
        flex-direction: row;
        align-items: flex-end;
    }

    .secciones--botones{
        padding: 0 2%;
        margin-right: -20px;
        height: 70%;
        border-radius: 5px 10px 0 0;
        border:none;
        background-color: #88b5b0;
        color:#ffffff;
        border-radius: 12px 12px 0 0; 
        box-shadow: 2px 0 3px rgba(0, 0, 0, 0.15), -2px 0 3px rgba(0, 0, 0, 0.15);
    }
    .secciones--botones:first-child{
        z-index: 6;
    }
    .secciones--botones:nth-child(2){
        z-index: 5;
    }
    .secciones--botones:nth-child(3){
        z-index: 4
    }
    .secciones--botones:nth-child(4){
        z-index: 3
    }
    .secciones--botones:nth-child(5){
        z-index: 2
    }
    .secciones--botones:last-child{
        z-index: 1
    }
    .secciones--botones.active{
        background-color:#008073;
        z-index: 7;
        height: 90%;
    }

    .secciones--botones:hover{
        color: #ffffff;
        background-color: #008073;
        height: 80%;
        z-index: 6;
    }

    .secciones--botones:active{
        transform: scale(0.98);
    }
    /*-----FIN SECCIONES DE CARPETA MENU --------*/

    /*-----INICIO CONTENEDOR FILTROS DE BISQUEDA------*/
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
        background-color: #008073;
        color: #ffffff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.1s;
    }

    .menuBotones--botones:hover{
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transform: scale(1.01);
    }

    .menuBotones--botones:active{
        transform: scale(0.98);
    }
    .menuBotones--botones.activate{
        background-color: #ffffff;
        color:#008073;
        box-shadow: 4px 4px 6px rgba(0, 0, 0, 0.1), -4px -4px 6px rgba(0, 0, 0, 0.1);
    }
    .menuBotones--botones, .agregar::after {
        content: "Añadir";
    }
    .menuBotones--botones.activate::after{
        content: "Cancelar";
    }
    /*-----FIN CONTENEDOR FILTROS DE BISQUEDA------*/

    /* Contenedor de la tabla */
    .tablaPrincipal--contenedor{
        box-sizing: border-box;
        padding: 2%;
        padding-bottom: 5%;
        height: 73%;
        width: 100%;
        overflow-x: auto; 
        max-height: 100%;
        display:flex;
        flex-direction: column;
    }
</style>
