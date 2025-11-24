<script>
    export default {
    name: "TablasEquipos",

    // Recibe la sección activa y las filas de datos desde el padre
    props: {
        // Recibe la sección actual para determinar los placeholders dinámicos
        seccion: {
            type: String,
            required: true
        },
        bloqueCampos: {
            type: Boolean,
            required: true
        },
        seriesInesistentes: {
            type: Array,
            required: true
        },
        todasSeries: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            serieSeleccionada: "",
            mostrarLista: false,
            textoBusqueda: ""
        };
    },

    computed: {
        seriesFiltradas() {
            const texto = this.textoBusqueda.toLowerCase();

            // 👉 Si la sección es MetrologíaT usar TODAS las series
            if (this.seccion === "MetrologiaT") {
                return this.todasSeries.filter(s =>
                    s.toLowerCase().includes(texto)
                );
            }

            // 👉 Para todas las demás vistas usar seriesInesistentes
            return this.seriesInesistentes.filter(s =>
                s.toLowerCase().includes(texto)
            );
        }
    },


    watch: {
        textoBusqueda(valor) {
            this.mostrarLista = valor.length > 0;
        }
    },

    methods: {
        seleccionarSerie(serie) {
            this.serieSeleccionada = serie;
            this.textoBusqueda = serie;
            this.mostrarLista = false;
        },

        validarEntrada() {
            if (this.seccion === "MetrologiaT") {
                // Validación solo para MetrologíaT
                if (!this.todasSeries.includes(this.textoBusqueda)) {
                    this.textoBusqueda = "";
                    this.serieSeleccionada = "";
                }
                return;
            }

            // Validación para las demás secciones
            if (!this.seriesInesistentes.includes(this.textoBusqueda)) {
                this.textoBusqueda = "";
                this.serieSeleccionada = "";
            }
        }
    }
};
</script>
<template>
    <div>
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
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT -->
                            <input
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(serie, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(serie)"
                                >
                                    {{ serie }}
                                </li>
                            </ul>
                        </div>
                    </div>

                    <input class="formularioAgregar--inputs" placeholder="Vida Util" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Fecha Adquisicion" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Propietario Equipo" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Fecha de Fabricacion" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="NIT" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input class="formularioAgregar--inputs" placeholder="Proveedor Equipo" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Estado de Garantía" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Terminación Garantía" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Forma Adquisición" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Tipo Documento" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Número Documento" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones">Guardar</button>
                <button class="formularioAgregar--botones">Limpiar</button>
            </div>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===true">
                <h3>No hay equipos, por favor ingresa uno nuevo en General</h3>
            </div>
        </div>

        <div class="contenedorfromulario" v-if="seccion==='MetrologiaA'">
            <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS METROLOGÍA (ADMINISTRATIVA)</h2>
            <form class="tablaprincipal--formularioAgregar">
                <div class="formularioAgregar--columnas">
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT -->
                            <input
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(serie, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(serie)"
                                >
                                    {{ serie }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <input class="formularioAgregar--inputs" placeholder="Tiene Mantenimiento" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Tipo Mantenimiento" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Frecuencia Mto" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input class="formularioAgregar--inputs" placeholder="Tiene Calibración" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Tipo Calibración" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Frecuencia Calibración" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones">Guardar</button>
                <button class="formularioAgregar--botones">Limpiar</button>
            </div>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===true">
                <h3>No hay equipos, por favor ingresa uno nuevo en General</h3>
            </div>
        </div>

        <div class="contenedorfromulario" v-if="seccion==='MetrologiaT'">
            <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS METROLOGÍA (TÉCNICA)</h2>
            <form class="tablaprincipal--formularioAgregar">
                <div class="formularioAgregar--columnas">
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT -->
                            <input
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(serie, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(serie)"
                                >
                                    {{ serie }}
                                </li>
                            </ul>
                        </div>
                    </div>

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
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT -->
                            <input
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(serie, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(serie)"
                                >
                                    {{ serie }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <input class="formularioAgregar--inputs" placeholder="Manual Mantenimiento" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Hoja de Vida" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Reg. Importación" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Manual Operación" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input class="formularioAgregar--inputs" placeholder="Guía Rápida" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Instructivo Uso" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Protocolo Mantenimiento" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Frec. Metrológica" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones">Guardar</button>
                <button class="formularioAgregar--botones">Limpiar</button>
            </div>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===true">
                <h3>No hay equipos, por favor ingresa uno nuevo en General</h3>
            </div>
        </div>

        <div class="contenedorfromulario" v-if="seccion==='Condicion'">
            <h2 class="tablaPrincipal--tituloAgregar">INGRESO DE EQUIPOS CONDICIÓN</h2>
            <form class="tablaprincipal--formularioAgregar">
                <div class="formularioAgregar--columnas">
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT -->
                            <input
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(serie, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(serie)"
                                >
                                    {{ serie }}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <input class="formularioAgregar--inputs" placeholder="Voltaje" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Corriente" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Humedad Relativa" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input class="formularioAgregar--inputs" placeholder="Temperatura" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Dimensiones" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Peso" :disabled="bloqueCampos"></input>
                    <input class="formularioAgregar--inputs" placeholder="Otros" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones">Guardar</button>
                <button class="formularioAgregar--botones">Limpiar</button>
            </div>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===true">
                <h3>No hay equipos, por favor ingresa uno nuevo en General</h3>
            </div>
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
        height: auto;
        padding: 12px 0;
        margin-top:0;
        background-color: #008073;
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
    .formularioAgregar--input-wrapper {
        width: 40%;                 /* IGUAL a los otros inputs */
        height: 10%;                /* IGUAL a los otros inputs */
        margin-bottom: 2%;          /* IGUAL a los otros inputs */
        position: relative;         /* Necesario para que el UL se posicione bien */
    }

    .autocomplete-container input {
        width: 100%;
        height: 100%;               /* Misma altura que los demás */
    }

    /* LISTA */
    .autocomplete-list {
        position: absolute;
        top: 100%;                  /* Debajo del input */
        left: 0;
        width: 100%;                /* MISMO ancho exacto del input */
        background: white;
        border: 1px solid #ddd;
        margin-top: 2px;
        border-radius: 4px;
        max-height: 160px;
        overflow-y: auto;
        z-index: 999;
    }


    .autocomplete-item {
        padding: 8px 12px;
        cursor: pointer;
    }

    .autocomplete-item:hover {
        background-color: #f2f2f2;
    }


</style>