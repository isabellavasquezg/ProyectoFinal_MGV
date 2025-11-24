<script>
    export default {
    name: "TablasEquipos",

    // Recibe la sección activa y las filas de datos desde el padre
    props: {
        // Recibe la sección actual para determinar los placeholders dinámicos
        seccion: {
            type: String,
            required: true
        }
    },

    data() {
        return {
        };
    },
    watch: {
    },

    methods: {
    },
};
</script>
<template>
    <div class="contenedorfromulario" v-if="seccion==='General'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS INFORMACIÓN GENERAL</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Marca"></input>
                <input class="formularioAgregar--inputs" placeholder="Modelo"></input>
                <input class="formularioAgregar--inputs" placeholder="Nombre Equipo"></input>
                <input class="formularioAgregar--inputs" placeholder="Responsable Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Código Inventario"></input>
                
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Código IPS"></input>
                <input class="formularioAgregar--inputs" placeholder="Código ECRI"></input>
                <input class="formularioAgregar--inputs" placeholder="Ubicación"></input>
                <input class="formularioAgregar--inputs" placeholder="Clasificación Misional"></input>
                <input class="formularioAgregar--inputs" placeholder="Clasificación IPS"></input>
                <input class="formularioAgregar--inputs" placeholder="Clasificación Riesgo"></input>
                <input class="formularioAgregar--inputs" placeholder="Registro Invima"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
    <div class="contenedorfromulario" v-if="seccion==='Registro'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS INFORMACIÓN DE REGISTRO</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Vida Util"></input>
                <input class="formularioAgregar--inputs" placeholder="Fecha Adquisicion"></input>
                <input class="formularioAgregar--inputs" placeholder="Propietario Equipo"></input>
                <input class="formularioAgregar--inputs" placeholder="Fecha de Fabricacion"></input>
                <input class="formularioAgregar--inputs" placeholder="NIT"></input>
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Proveedor Equipo"></input>
                <input class="formularioAgregar--inputs" placeholder="Estado de Garantía"></input>
                <input class="formularioAgregar--inputs" placeholder="Terminación Garantía"></input>
                <input class="formularioAgregar--inputs" placeholder="Forma Adquisición"></input>
                <input class="formularioAgregar--inputs" placeholder="Tipo Documento"></input>
                <input class="formularioAgregar--inputs" placeholder="Número Documento"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
    <div class="contenedorfromulario" v-if="seccion==='MetrologiaA'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS METROLOGÍA (ADMINISTRATIVA)</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Tiene Mantenimiento"></input>
                <input class="formularioAgregar--inputs" placeholder="Tipo Mantenimiento"></input>
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Frecuencia Mto"></input>
                <input class="formularioAgregar--inputs" placeholder="Tiene Calibración"></input>
                <input class="formularioAgregar--inputs" placeholder="Tipo Calibración"></input>
                <input class="formularioAgregar--inputs" placeholder="Frecuencia Calibración"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
    <div class="contenedorfromulario" v-if="seccion==='MetrologiaT'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS METROLOGÍA (TÉCNICA)</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Magnitud"></input>
                <input class="formularioAgregar--inputs" placeholder="Rango Equipo"></input>
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Resolución"></input>
                <input class="formularioAgregar--inputs" placeholder="Rango Trabajo"></input>
                <input class="formularioAgregar--inputs" placeholder="Error Máximo"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
    <div class="contenedorfromulario" v-if="seccion==='Documentacion'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS DOCUMENTACIÓN</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Hoja de Vida"></input>
                <input class="formularioAgregar--inputs" placeholder="Reg. Importación"></input>
                <input class="formularioAgregar--inputs" placeholder="Manual Operación"></input>
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Manual Mantenimiento"></input>
                <input class="formularioAgregar--inputs" placeholder="Guía Rápida"></input>
                <input class="formularioAgregar--inputs" placeholder="Instructivo Uso"></input>
                <input class="formularioAgregar--inputs" placeholder="Protocolo Mantenimiento"></input>
                <input class="formularioAgregar--inputs" placeholder="Frec. Metrológica"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
    <div class="contenedorfromulario" v-if="seccion==='Condicion'">
        <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS CONDICIÓN</h2>
        <form class="tablaprincipal--formularioAgregar">
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Sede"></input>
                <input class="formularioAgregar--inputs" placeholder="Servicio"></input>
                <input class="formularioAgregar--inputs" placeholder="Número de Serie"></input>
                <input class="formularioAgregar--inputs" placeholder="Voltaje"></input>
                <input class="formularioAgregar--inputs" placeholder="Corriente"></input>
            </div>
            <div class="formularioAgregar--columnas">
                <input class="formularioAgregar--inputs" placeholder="Humedad Relativa"></input>
                <input class="formularioAgregar--inputs" placeholder="Temperatura"></input>
                <input class="formularioAgregar--inputs" placeholder="Dimensiones"></input>
                <input class="formularioAgregar--inputs" placeholder="Peso"></input>
                <input class="formularioAgregar--inputs" placeholder="Otros"></input>
            </div>
        </form>
        <div class="formularioAgregar--contenedorbotones">
            <button class="formularioAgregar--botones">Guardar</button>
            <button class="formularioAgregar--botones">Limpiar</button>
        </div>
    </div>
</template>
<style>
    .contenedorfromulario{
        width: 100%;
        height: 100%;
    }
    .tablaprincipal--formularioAgregar{
        box-sizing: border-box;
        height: 65%;
        margin-top: 1%;
        display: flex;
        flex-direction: row;
    }
    .formularioAgregar--columnas{
        display:flex;
        flex-direction: column;
    }
    .tablaPrincipal--tituloAgregar{
        box-sizing: border-box;
        height: 15%;
        margin-top:0;
        background-color: #008073;
        padding: 1% 0;
        /* CORRECCIÓN: Centrado de Texto */
        text-align: center;
        color: #ffffff;
    }
    .formularioAgregar--columnas{
        width: 50%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .formularioAgregar--inputs{
        background-color: #ffffff;
        border: none;
        border-bottom: 1px solid #a2a2a2;
        width: 40%;
        /* CORRECCIÓN: Reducir altura del input para evitar desbordamiento */
        height: 10%; 
        /* CORRECCIÓN: Ajustar margen para que encajen 8 elementos */
        margin-bottom: 2%; 
    }
    .formularioAgregar--inputs:focus{
        outline: none;
        border-bottom: 1px solid #008073;
    }
    .formularioAgregar--contenedorbotones{
        height: 20%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-end;
    }
    .formularioAgregar--botones{
        width: 8%;
        height: 60%;
        border-radius: 5px;
        margin-right: 3% ;
        background-color: #0a346c;
        color: #ffffff;
        border: none;
    }
    .formularioAgregar--botones:hover{
        transform: scale(1.01);
        box-shadow: 2px 2px 0 #031f438b;
    }
    .formularioAgregar--botones:active{
        transform:scale(0.98);
    }
</style>