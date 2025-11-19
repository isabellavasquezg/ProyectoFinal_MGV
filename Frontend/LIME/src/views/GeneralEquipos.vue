<script>
import TablasEquipos from '../components/TablasEquipos.vue';
import FiltrosMenu from '../components/FiltrosMenu.vue';
export default {
    components: {
        FiltrosMenu,
        TablasEquipos
    },
    name: "GeneralEquipos",
    data() {
        return {
            seccion:"General"
        };
    },
    methods: {
        cambiarSeccion(seccionNueva){
            this.seccion = seccionNueva;
        }
    },
};
</script>
<template>
<div class="background"> 
    <div class="slidebar">
    </div>
    <div class="menuPrincipal">
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones">Equipos</button>
            <button class="navbar--opciones">Responsables</button>
            <button class="navbar--opciones">Sedes</button>
            <button class="navbar--opciones">Servicios</button>
        </div>
        <div class="menuPrincipal--secciones">
                <button class="secciones--botones" @click="cambiarSeccion('General')">General</button>
                <button class="secciones--botones" @click="cambiarSeccion('Registro')">Registro Historico</button>
                <button class="secciones--botones" @click="cambiarSeccion('MetrologiaA')">Metrologia administrativa</button>
                <button class="secciones--botones" @click="cambiarSeccion('MetrologiaT')">Metrologia Tecnica</button>
                <button class="secciones--botones" @click="cambiarSeccion('Documentacion')">Documentación</button>
                <button class="secciones--botones" @click="cambiarSeccion('Condicion')">Coondicion Funcionamiento</button>
        </div>
        <div class="menuPrincipal--tablaPrincipal">
            <div class="tablaPrincipal--filtros">
                <FiltrosMenu :seccion="seccion" />
                <div class="tablaPricipal--menuBotones">
                        <button class="menuBotones--botones" type="button">Agregar</button>
                        <button class="menuBotones--botones" type="button">Eliminar</button>
                </div>
            </div>
            <div class="tablaPrincipal--contenedor">
                <TablasEquipos :seccion="seccion" />    
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
        width: 13%;
        height: 100%;
    }
    /*------------------Menu Principal------------------- */
    .menuPrincipal{
        width: 87%;
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
        margin-top: 0;
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
</style>