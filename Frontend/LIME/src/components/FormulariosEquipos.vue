<script>
    import axios from "axios";
    export default {
    name: "TablasEquipos",

    // Recibe la sección activa y las filas de datos desde el padre
    props: {
        modoEdicion: {
            type: Boolean,
            default: false
        },
        serieEditar: {
            type: String, 
            default: null
        },
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 3;">
                        <div class="autocomplete-container">
                            <input
                                ref="sede"
                                class="formularioAgregar--inputs"
                                placeholder="nombre de sede"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
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

                    <div class="formularioAgregar--input-wrapper" style="z-index: 2;">
                        <div class="autocomplete-container">
                            <input
                                ref="servicio"
                                class="formularioAgregar--inputs"
                                placeholder="Servicio"
                                :disabled="bloquearCamposServicio"
                                v-model="textoBusquedaServicio"
                                @focus="cerrarTodasLasListas(); mostrarListaServicio = true"
                            >
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

                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input
                                ref="responsable"
                                class="formularioAgregar--inputs"
                                placeholder="Responsable Servicio"
                                :disabled="bloquearCamposServicio"
                                v-model="textoBusquedaResponsable"
                                @focus="cerrarTodasLasListas(); mostrarListaResponsable = true"
                            >
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input v-if="modoEdicion===false"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
                            <input v-if="modoEdicion===true"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :value="serieEditar"
                                readonly>
                            </input>
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0 && modoEdicion===false" class="autocomplete-list">
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

                    <input ref="vidautil" class="formularioAgregar--inputs" placeholder="Vida Util" :disabled="bloqueCampos" type="text"></input>
                    <input ref="fechaadquisicion" class="formularioAgregar--inputs" placeholder="Fecha Adquisicion" :disabled="bloqueCampos" type="text" onfocus="(this.type='date')" onblur="(this.type='text')"></input>
                    
                    <input ref="propietarioequipo" class="formularioAgregar--inputs" placeholder="Propietario Equipo" :disabled="bloqueCampos"></input>
                    
                    <input ref="fechafarbicacion" class="formularioAgregar--inputs" placeholder="Fecha de Fabricacion" :disabled="bloqueCampos" type="text" onfocus="(this.type='date')" onblur="(this.type='text')"></input>
                    
                    <input ref="nit" class="formularioAgregar--inputs" placeholder="NIT" :disabled="bloqueCampos"></input>
                </div>
                <div class="formularioAgregar--columnas">
                    <input ref="privedorequipo" class="formularioAgregar--inputs" placeholder="Proveedor Equipo" :disabled="bloqueCampos"></input>
                    
                    <select ref="estadogarantia" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Estado de Garantía</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>
                    
                    <input ref="terminaciongarantia" class="formularioAgregar--inputs" placeholder="Terminación Garantía" :disabled="bloqueCampos" type="text" onfocus="(this.type='date')" onblur="(this.type='text')"></input>
                    
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input v-if="modoEdicion===false"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
                            <input v-if="modoEdicion===true"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :value="serieEditar"
                                readonly>
                            </input>
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0 && modoEdicion===false"" class="autocomplete-list" >
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
                    
                    <select ref="tienemantenimiento" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Tiene Mantenimiento</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>
                    
                    <input ref="frecuenciamto" class="formularioAgregar--inputs" placeholder="Frecuencia Mto (Entero)" :disabled="bloqueCampos" type="number" min="1"></input>
                </div>
                
                <div class="formularioAgregar--columnas">
                    <select ref="tienecalibracion" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Tiene Calibración</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>
                    
                    <input ref="frecuenciacalibracion" class="formularioAgregar--inputs" placeholder="Frecuencia Calibración (Entero)" :disabled="bloqueCampos" type="number" min="1"></input>
                </div>
                <input ref="campoExtra1" class="formularioAgregar--inputs" placeholder="Otro Campo Metrología" :disabled="bloqueCampos" v-if="false"></input>
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input v-if="modoEdicion===false"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
                            <input v-if="modoEdicion===true"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :value="serieEditar"
                                readonly>
                            </input>
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0 && modoEdicion===false"" class="autocomplete-list" >
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input v-if="modoEdicion===false"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
                            <input v-if="modoEdicion===true"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :value="serieEditar"
                                readonly>
                            </input>
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0 && modoEdicion===false"" class="autocomplete-list" >
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
                    
                    <select ref="manualmantenimiento" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Manual Mantenimiento</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <select ref="hojavida" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Hoja de Vida</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <select ref="regimportacion" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Reg. Importación</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <select ref="manualoperacion" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Manual Operación</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>
                </div>
                <div class="formularioAgregar--columnas">
                    <select ref="guiarapida" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Guía Rápida</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <select ref="intructivo" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Instructivo Uso</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <select ref="protocolo" class="formularioAgregar--inputs" :disabled="bloqueCampos">
                        <option value="" disabled selected>Protocolo Mantenimiento</option>
                        <option value="Sí">Sí</option>
                        <option value="No">No</option>
                    </select>

                    <input ref="frecuanciam" type="text" class="formularioAgregar--inputs" :disabled="bloqueCampos" placeholder="Frecuencia Metrologica"></input>
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
                    <div class="formularioAgregar--input-wrapper" style="z-index: 1;">
                        <div class="autocomplete-container">
                            <input v-if="modoEdicion===false"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :disabled="bloqueCampos"
                                v-model="textoBusqueda"
                                @blur="validarEntrada"
                                @focus="cerrarTodasLasListas(); mostrarLista = true"
                            >
                            <input v-if="modoEdicion===true"
                                ref="serie"
                                class="formularioAgregar--inputs"
                                placeholder="Número de Serie"
                                :value="serieEditar"
                                readonly>
                            </input>
                            <ul v-if="mostrarLista && seriesFiltradas.length > 0 && modoEdicion===false"" class="autocomplete-list" >
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
                <button class="formularioAgregar--botones" @click="guardarFormulario">Guardar</button>
                <button class="formularioAgregar--botones" @click="limpiarFormulario">Limpiar</button>
            </div>
            <div class="formularioAgregar--contenedorbotones" v-if="bloqueCampos===true">
                <h3>No hay equipos, por favor ingresa uno nuevo en General</h3>
            </div>
        </div>
    </div>
</template>
<style>
    /* =============================
   ESTILO GLOBAL DE INPUTS
   ============================= */

/* =============================
   ESTILO GLOBAL DE INPUTS
   ============================= */
.formularioAgregar--input-wrapper  .formularioAgregar--inputs{
    border:none;
    background-color: transparent;
}
.formularioAgregar--inputs,
.formularioAgregar--input-wrapper,
.formularioAgregar--input-wrapper input,
.formularioAgregar--input-wrapper select {      /* <-- AQUÍ ya NO va select.formularioAgregar--inputs */
    width: 90%;
    height: 42px;
    margin-bottom: 14px;
    padding: 0 12px;
    box-sizing: border-box;
    background: #ffffff;

    border: 1px solid #c8c8c8;
    border-radius: 6px;
    font-size: 14px;
    transition: all 0.2s ease;
}

/* Asegura que TODOS los selects luzcan igual que los inputs */
select.formularioAgregar--inputs {
    appearance: none;
    background-image: url("data:image/svg+xml;utf8,<svg fill='gray' height='14' viewBox='0 0 20 20' width='14' xmlns='http://www.w3.org/2000/svg'><path d='M5.516 7.548c-.44-.44-.44-1.152 0-1.592.44-.440 1.152-.44 1.592 0L10 8.848l2.892-2.892c.44-.440 1.152-.44 1.592 0 .44.440.44 1.152 0 1.592l-3.688 3.688c-.44.44-1.152.44-1.592 0L5.516 7.548z'/></svg>");
    background-position: right 12px center;
    background-repeat: no-repeat;
}


/* Input dentro del wrapper */
.formularioAgregar--input-wrapper {
    width: 90%;
    position: relative;
}

.formularioAgregar--input-wrapper input {
    width: 100%;
    height: 42px;
    margin-bottom: 0;
}

/* =============================
   FOCUS
   ============================= */
.formularioAgregar--inputs:focus,
.formularioAgregar--input-wrapper input:focus,
select.formularioAgregar--inputs:focus {
    outline: none;
    border-color: #008073;
    box-shadow: 0 0 4px rgba(0,128,115,0.4);
}

/* =============================
   AUTOCOMPLETE LIST
   ============================= */

.autocomplete-list {
    position: absolute;
    top: 46px; /* justo debajo del input */
    left: 0;
    width: 100%;
    background: #fff;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
    max-height: 180px;
    overflow-y: auto;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
}

.autocomplete-item {
    padding: 10px 12px;
    cursor: pointer;
    font-size: 14px;
}

.autocomplete-item:hover {
    background-color: #f3f3f3;
}

/* =============================
   LAYOUT GENERAL (se mantiene)
   ============================= */

.contenedorfromulario{
    width: 100%;
}

.tablaprincipal--formularioAgregar{
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    margin-top: 1%;
}

.tablaPrincipal--tituloAgregar{
    padding: 12px 0;
    margin-top:0;
    background-color: #008073;
    text-align: center;
    color: #ffffff;
}

.formularioAgregar--columnas{
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.formularioAgregar--contenedorbotones{
    display: flex;
    justify-content: center;
    align-items: flex-end;
    margin-top: 20px;
}

.formularioAgregar--botones{
    width: 120px;
    height: 40px;
    border-radius: 6px;
    margin-right: 20px;
    background-color: #0a346c;
    color: #ffffff;
    border: none;
    transition: 0.2s;
}

.formularioAgregar--botones:hover{
    transform: scale(1.03);
    box-shadow: 3px 3px 0 #031f438b;
}

.formularioAgregar--botones:active{
    transform:scale(0.98);
}

</style>