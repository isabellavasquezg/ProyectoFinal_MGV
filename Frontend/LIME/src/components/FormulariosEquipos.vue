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
        sedeSeleccionada: {
            type: [String, Number, null],
            default: null
        },
        seriesInesistentes: {
            type: Array,
            required: true
        },
        todasSeries: {
            type: Array,
            required: true
        },
        listaResposables: {
            type: Array,
            required: true
        },
        listaServicios: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            serieSeleccionada: "",
            mostrarLista: false,
            textoBusqueda: "",

            servicioSeleccionado: "",
            mostrarListaServicio: false,
            textoBusquedaServicio: "",

            responsableSeleccionado: "",
            mostrarListaResponsable: false,
            textoBusquedaResponsable: "",
        };
    },

    computed: {
        seriesFiltradas() {
            const texto = this.textoBusqueda.toLowerCase();

            const lista = 
                (this.seccion === "MetrologiaT" || this.seccion === "General")
                ? this.todasSeries
                : this.seriesInesistentes;

            return lista
                .map(x => typeof x === "string" ? x : x.serie_equipo || x.nombre_sede || "")
                .filter(x => x.toLowerCase().includes(texto));
        },

        serviciosFiltrados() {
            const t = this.textoBusquedaServicio.toLowerCase();

            return this.listaServicios
                .map(s => typeof s === "string" ? s : s.nombre_servicio || "")
                .filter(s => s.toLowerCase().includes(t));
        },
        responsablesFiltrados() {
            const t = this.textoBusquedaResponsable.toLowerCase();

            return this.listaResposables
                .map(r => typeof r === "string" ? r : r.nombre_responsable || "")
                .filter(r => r.toLowerCase().includes(t));
        },
        bloquearCamposServicio() {
            return this.serieSeleccionada === ""; 
            
        }
    },


    watch: {
        textoBusqueda(valor) {
            this.mostrarLista = valor.length > 0;
        }
    },

    methods: {
        limpiarFormulario() {
            // 🔹 1. limpiar TODOS los v-model que existen en cualquier sección
            this.textoBusqueda = "";
            this.textoBusquedaServicio = "";
            this.textoBusquedaResponsable = "";

            this.serieSeleccionada = "";
            this.servicioSeleccionado = "";
            this.responsableSeleccionado = "";

            // 🔹 2. OCULTAR TODAS LAS LISTAS AUTOCOMPLETE
            this.mostrarLista = false;
            this.mostrarListaServicio = false;
            this.mostrarListaResponsable = false;

            // 🔹 3. limpiar automáticamente TODOS los <input ref="...">
            //    no importa de qué sección sean
            Object.keys(this.$refs).forEach(ref => {
                const campo = this.$refs[ref];

                // si el ref existe y el elemento tiene "value"
                if (campo && campo.value !== undefined) {
                    campo.value = "";
                }
            });

        },
        guardarFormulario() {
            let datosFormulario={};
            if(this.seccion==="General"){
                datosFormulario = {
                    sede: this.textoBusqueda || "",
                    servicio: this.textoBusquedaServicio || "",
                    responsable: this.textoBusquedaResponsable || "",
                };
            }else{
                datosFormulario={
                    serie:this.textoBusqueda || "",
                }
            }
                for (const ref in this.$refs) {
                    const campo = this.$refs[ref];
                    if (campo && "value" in campo) {
                        datosFormulario[ref] = campo.value;
                    }
                }

            console.log("Datos a enviar:", datosFormulario);
            this.$emit("guardar-formulario", datosFormulario);
        },
        cerrarTodasLasListas() {
            this.mostrarLista = false;
            this.mostrarListaServicio = false;
            this.mostrarListaResponsable = false;
        },
        
        seleccionarSerie(serie) {
            this.serieSeleccionada = serie;
            this.textoBusqueda = serie;
            this.mostrarLista = false;
            if (this.seccion==="General"){
                this.$emit("actualizar-sede", serie);
            }
            
        },
        seleccionarServicio(serv) {
            this.servicioSeleccionado = serv;
            this.textoBusquedaServicio = serv;
            this.mostrarListaServicio = false;
        },

        seleccionarResponsable(resp) {
            this.responsableSeleccionado = resp;
            this.textoBusquedaResponsable = resp;
            this.mostrarListaResponsable = false;
        },

        validarEntrada() {
            if (this.seccion === "MetrologiaT" || this.seccion==="General") {
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
                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT SEDE -->
                            <input
                                ref="sede"
                                class="formularioAgregar--inputs"
                                placeholder="nombre de sede"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >

                            <!-- LISTA AUTOCOMPLETE -->
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0" class="autocomplete-list">
                                <li 
                                    v-for="(sede, index) in seriesFiltradas"
                                    :key="index"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarSerie(sede)"
                                >
                                    {{ sede }}
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT SERVICIO -->
                            <input
                                ref="servicio"
                                class="formularioAgregar--inputs"
                                placeholder="Servicio"
                                :disabled="bloquearCamposServicio"
                                v-model="textoBusquedaServicio"
                                @focus="cerrarTodasLasListas(); mostrarListaServicio = true"
                            >

                            <!-- LISTA SERVICIOS -->
                            <ul v-if="mostrarListaServicio && serviciosFiltrados.length > 0" class="autocomplete-list">
                                <li
                                    v-for="(serv, i) in serviciosFiltrados"
                                    :key="'serv'+i"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarServicio(serv)"
                                >
                                    {{ serv }}
                                </li>
                            </ul>
                        </div>
                    </div>

                    <input ref="numeroSerie" class="formularioAgregar--inputs" placeholder="Número de Serie">
                    <input ref="marca" class="formularioAgregar--inputs" placeholder="Marca">
                    <input ref="modelo" class="formularioAgregar--inputs" placeholder="Modelo">
                    <input ref="nombreEquipo" class="formularioAgregar--inputs" placeholder="Nombre Equipo">

                    <div class="formularioAgregar--input-wrapper">
                        <div class="autocomplete-container">
                            <!-- INPUT RESPONSABLE -->
                            <input
                                ref="responsable"
                                class="formularioAgregar--inputs"
                                placeholder="Responsable Servicio"
                                :disabled="bloquearCamposServicio"
                                v-model="textoBusquedaResponsable"
                                @focus="cerrarTodasLasListas(); mostrarListaResponsable = true"
                            >

                            <!-- LISTA RESPONSABLES -->
                            <ul v-if="mostrarListaResponsable && responsablesFiltrados.length > 0" class="autocomplete-list">
                                <li
                                    v-for="(resp, i) in responsablesFiltrados"
                                    :key="'resp'+i"
                                    class="autocomplete-item"
                                    @mousedown.prevent="seleccionarResponsable(resp)"
                                >
                                    {{ resp }}
                                </li>
                            </ul>
                        </div>
                    </div>

                    <input ref="codigoInventario" class="formularioAgregar--inputs" placeholder="Código Inventario">
                </div>

                <div class="formularioAgregar--columnas">
                    <input ref="codigoIPS" class="formularioAgregar--inputs" placeholder="Código IPS">
                    <input ref="codigoECRI" class="formularioAgregar--inputs" placeholder="Código ECRI">
                    <input ref="ubicacion" class="formularioAgregar--inputs" placeholder="Ubicación">
                    <input ref="clasificacionMisional" class="formularioAgregar--inputs" placeholder="Clasificación Misional">
                    <input ref="clasificacionIPS" class="formularioAgregar--inputs" placeholder="Clasificación IPS">
                    <input ref="clasificacionRiesgo" class="formularioAgregar--inputs" placeholder="Clasificación Riesgo">
                    <input ref="registroInvima" class="formularioAgregar--inputs" placeholder="Registro Invima">
                </div>
            </form>

            <div class="formularioAgregar--contenedorbotones">
                <button type="button" class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button type="button" class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
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

                    <input ref="vidautil" class="formularioAgregar--inputs" placeholder="Vida Util" :disabled="bloqueCampos"></input>
                    <input ref="fechaadquisicion" class="formularioAgregar--inputs" placeholder="Fecha Adquisicion" :disabled="bloqueCampos"></input>
                    <input ref="propietarioequipo" class="formularioAgregar--inputs" placeholder="Propietario Equipo" :disabled="bloqueCampos"></input>
                    <input ref="fechafarbicacion" class="formularioAgregar--inputs" placeholder="Fecha de Fabricacion" :disabled="bloqueCampos"></input>
                    <input ref="nit" class="formularioAgregar--inputs" placeholder="NIT" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="privedorequipo" class="formularioAgregar--inputs" placeholder="Proveedor Equipo" :disabled="bloqueCampos"></input>
                    <input ref="estadogarantia" class="formularioAgregar--inputs" placeholder="Estado de Garantía" :disabled="bloqueCampos"></input>
                    <input ref="terminaciongarantia" class="formularioAgregar--inputs" placeholder="Terminación Garantía" :disabled="bloqueCampos"></input>
                    <input ref="formaadquisicion" class="formularioAgregar--inputs" placeholder="Forma Adquisición" :disabled="bloqueCampos"></input>
                    <input ref="tipodocumento" class="formularioAgregar--inputs" placeholder="Tipo Documento" :disabled="bloqueCampos"></input>
                    <input ref="numerodocumento" class="formularioAgregar--inputs" placeholder="Número Documento" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
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
                    <input ref="tienemantenimiento" class="formularioAgregar--inputs" placeholder="Tiene Mantenimiento" :disabled="bloqueCampos"></input>
                    <input ref="frecuenciamto" class="formularioAgregar--inputs" placeholder="Frecuencia Mto" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="tienecalibracion" class="formularioAgregar--inputs" placeholder="Tiene Calibración" :disabled="bloqueCampos"></input>
                    <input ref="frecuenciacalibracion" class="formularioAgregar--inputs" placeholder="Frecuencia Calibración" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
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

                    <input ref="magnitud" class="formularioAgregar--inputs" placeholder="Magnitud"></input>
                    <input ref="rangoequipo" class="formularioAgregar--inputs" placeholder="Rango Equipo"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="resolucion" class="formularioAgregar--inputs" placeholder="Resolución"></input>
                    <input ref="rangotrabajo" class="formularioAgregar--inputs" placeholder="Rango Trabajo"></input>
                    <input ref="errormaximo" class="formularioAgregar--inputs" placeholder="Error Máximo"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones">
                <button class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas();mostrarLista = true"
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
                    <input ref="manualmantenimiento" class="formularioAgregar--inputs" placeholder="Manual Mantenimiento" :disabled="bloqueCampos"></input>
                    <input ref="hojavida" class="formularioAgregar--inputs" placeholder="Hoja de Vida" :disabled="bloqueCampos"></input>
                    <input ref="reg.importacion" class="formularioAgregar--inputs" placeholder="Reg. Importación" :disabled="bloqueCampos"></input>
                    <input ref="manualoperacion" class="formularioAgregar--inputs" placeholder="Manual Operación" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="guiarapida" class="formularioAgregar--inputs" placeholder="Guía Rápida" :disabled="bloqueCampos"></input>
                    <input ref="intructivo" class="formularioAgregar--inputs" placeholder="Instructivo Uso" :disabled="bloqueCampos"></input>
                    <input ref="protocolo" class="formularioAgregar--inputs" placeholder="Protocolo Mantenimiento" :disabled="bloqueCampos"></input>
                    <input ref="frecuanciam" class="formularioAgregar--inputs" placeholder="Frec. Metrológica" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
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
                    <input ref="voltaje" class="formularioAgregar--inputs" placeholder="Voltaje" :disabled="bloqueCampos"></input>
                    <input ref="corriente" class="formularioAgregar--inputs" placeholder="Corriente" :disabled="bloqueCampos"></input>
                    <input ref="humedad" class="formularioAgregar--inputs" placeholder="Humedad Relativa" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="temperatura" class="formularioAgregar--inputs" placeholder="Temperatura" :disabled="bloqueCampos"></input>
                    <input ref="dimensiones" class="formularioAgregar--inputs" placeholder="Dimensiones" :disabled="bloqueCampos"></input>
                    <input ref="peso" class="formularioAgregar--inputs" placeholder="Peso" :disabled="bloqueCampos"></input>
                    <input ref="otros" class="formularioAgregar--inputs" placeholder="Otros" :disabled="bloqueCampos"></input>
                </div>
            </form>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===false">
                <button class="formularioAgregar--botones" @click="guardarFormulario"
                >Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
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