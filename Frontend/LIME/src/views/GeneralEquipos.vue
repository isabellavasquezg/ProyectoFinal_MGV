<script>
import axios from "axios";
import FormulariosEquipos from "../components/FormulariosEquipos.vue";
import TablasEquipos from '../components/TablasEquipos.vue';
import FiltrosMenu from '../components/FiltrosMenu.vue';

/**
 * Vista principal de Gestión de Equipos.
 * Maneja la lógica de cambio de sección, filtrado, carga de datos 
 * desde la API y gestión de la adición de nuevos equipos.
 */
export default {
    name: "GeneralEquipos",
    components: {
        FormulariosEquipos,
        FiltrosMenu,
        TablasEquipos
    },

    data() {
        return {
            // Estado de la UI
            equiposParaDesactivar: [],
            seccion: "General",         // Sección activa (ej. 'General', 'Registro')
            cargando: false,            // Indica si una operación de red está en curso
            estadoAgregar: false,       // Muestra/Oculta el formulario de agregar

            // Datos principales
            filas: [],                  // Datos mostrados en la tabla (aplicados los filtros)
            general: [],                // Datos de la sección 'General' (usados para la comparación)
            
            // Datos para el formulario de Agregar/Editar
            sedeSeleccionada: '',       // Sede activa para la carga de servicios y responsables
            todasSeriesExistentes: [],  // Lista de series existentes en la sección actual
            seriesFaltantes: [],        // Series que están en 'General' pero no en la sección actual
            debeBloquearCampos: false,  // Controla si se bloquea el formulario (cuando no hay series faltantes)

            // Listas de apoyo para los selectores del formulario
            listaResponsables: [],
            listaServicios: [],

            // Estado de filtros
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
        actualizarSeleccionados(lista) {
            this.equiposParaDesactivar = lista;
            console.log(this.equiposParaDesactivar[0])
        },
        async desactivarEquiposSeleccionados() {
            if (this.equiposParaDesactivar.length === 0) {
                alert("Por favor, selecciona al menos un equipo para desactivar.");
                return;
            }

            if (!confirm(`¿Estás seguro de que deseas desactivar ${this.equiposParaDesactivar.length} equipo(s)? Esta acción actualizará su estado a INACTIVO.`)) {
                return;
            }

            this.cargando = true;

            try {
                // 1. OBTENER LA LISTA MAESTRA (Equipos Generales)
                // Necesitamos esta lista para mapear la serie a su ID de Equipo principal.
                const equiposMaestros = await this.obtenerDatos("General");
                
                // Crear un mapa Serie -> ID para una búsqueda rápida O(1)
                const serieToIdMap = equiposMaestros.reduce((map, equipo) => {
                    map[equipo.serie_equipo] = equipo.id;
                    return map;
                }, {});

                // 2. OBTENER LOS IDs REALES DEL EQUIPO A PARTIR DE LAS SERIES SELECCIONADAS
                const idsADesactivar = this.equiposParaDesactivar
                    .map(eq => serieToIdMap[eq.serie_equipo]) // Mapea la serie al ID
                    .filter(id => id !== undefined && id !== null); // Elimina posibles nulos o no encontrados

                if (idsADesactivar.length === 0) {
                    alert("Error: No se pudieron encontrar los IDs maestros para los equipos seleccionados.");
                    this.cargando = false;
                    return;
                }

                // 3. Crear el payload y enviar la solicitud PUT
                const payload = {
                    ids: idsADesactivar,
                    estado_equipo: 0 // 0 = Desactivado
                };
                console.log("hello",idsADesactivar[0])
                // Usamos el endpoint de estado (asumimos que ya está configurado en Django)
                const urlDesactivar = `http://127.0.0.1:8000/api/General/Estado/`; 
                
                const res = await axios.put(urlDesactivar, payload); 

                console.log("✅ Desactivación exitosa:", res.data);
                alert(res.data.message);
                
                // 4. Limpiar la selección y recargar la tabla
                this.equiposParaDesactivar = [];
                this.filas = this.filas.map(fila => ({ ...fila, seleccionado: false }));
                
                await this.listarEquipos(); 

            } catch (error) {
                console.error("❌ Error al desactivar equipos:", error.response?.data || error);
                alert("Hubo un error al intentar desactivar los equipos. Revisa la consola.");
            } finally {
                this.cargando = false;
            }
        },
        /**
         * Función genérica para obtener datos de una sección de la API.
         * @param {string} endpoint - El nombre de la sección (ej. 'General', 'Sedes').
         * @returns {Promise<Array>} Los datos del endpoint o un array vacío en caso de error.
         */
        async obtenerDatos(endpoint) {
            try {
                const url = `http://127.0.0.1:8000/api/${endpoint}/`;
                const res = await axios.get(url);
                return res.data.result || []; 
            } catch (err) {
                console.error(`❌ Error al obtener datos de ${endpoint}:`, err);
                // NOTA: Es mejor manejar el error en el padre para no saturar con alerts
                // alert(`Error al listar ${endpoint}`);
                return []; 
            }
        },

        /**
         * Obtiene y actualiza los datos de la tabla aplicando los filtros actuales o dados.
         * @param {Object} [filtros] - Filtros opcionales. Por defecto usa this.filtrosActuales.
         */
        async listarEquipos(filtros) {
            this.cargando = true;

            try {
                const filtrosAUsar = filtros || this.filtrosActuales;

                // 1. Construir la URL con parámetros (simplificado y más limpio)
                const params = new URLSearchParams(filtrosAUsar).toString();
                let url = `http://127.0.0.1:8000/api/${this.seccion}/`;
                
                // Evita añadir '?' si no hay parámetros realmente
                const tieneFiltros = Object.values(filtrosAUsar).some(v => v !== "");
                if (tieneFiltros) {
                    // Usamos un filtro más explícito para evitar URL largas si todo está vacío
                    const paramsActivos = {};
                    for (const [key, value] of Object.entries(filtrosAUsar)) {
                        if (value !== '') {
                            // Mapea los nombres de filtro a los nombres esperados por la API
                            if (key === 'numeroSerie') paramsActivos.serie = value;
                            else if (key.startsWith('dinamico')) paramsActivos[`f${key.slice(-1)}`] = value;
                            else paramsActivos[key] = value;
                        }
                    }
                    const queryString = new URLSearchParams(paramsActivos).toString();
                    if (queryString) {
                        url += `?${queryString}`;
                    }
                }

                // 2. Realizar la petición
                const res = await axios.get(url);
                this.filas = res.data.result || [];
                
            } catch (err) {
                console.error("❌ Error al listar equipos:", err);
                alert("Error al listar equipos. Consulta el log.");
                this.filas = [];
            }

            // `this.$nextTick()` no es necesario después de una asignación de datos. 
            // Vue maneja la reactividad automáticamente. 
            this.cargando = false; 
        },

        /**
         * Compara las series de la sección 'General' con la sección actual
         * para determinar qué equipos deben agregarse.
         */
        async compararSeries() {
            // Solo se ejecuta si estamos agregando y la sección no es 'General'
            if (this.seccion === "General") {
                // Lógica de carga de Selectores para 'General'
                await this.cargarSelectoresGeneral();
                this.debeBloquearCampos = true; // No se puede añadir si no hay sedes/servicios
                return;
            }

            this.cargando = true;
            try {
                // 1. Cargar ambas listas concurrentemente
                const [equiposGeneral, equiposSeccion] = await Promise.all([
                    this.obtenerDatos("General"),
                    this.obtenerDatos(this.seccion)
                ]);

                this.general = equiposGeneral;
                
                // 2. Crear un Set de series existentes para búsquedas rápidas (O(1))
                const seriesExistentes = new Set(
                    equiposSeccion.map(equipo => equipo.serie_equipo)
                );
                this.todasSeriesExistentes = Array.from(seriesExistentes); // Para el Formulario

                // 3. Identificar series faltantes
                this.seriesFaltantes = this.general
                    .filter(equipoGeneral => !seriesExistentes.has(equipoGeneral.serie_equipo))
                    .map(equipoGeneral => equipoGeneral.serie_equipo);
                
                // 4. Actualizar el estado de bloqueo del formulario
                this.debeBloquearCampos = this.seriesFaltantes.length === 0;

                if (this.seriesFaltantes.length === 0) {
                    console.log(`✅ Todas las series de 'General' ya tienen datos en '${this.seccion}'.`);
                } else {
                    console.log(`⚠️ ${this.seriesFaltantes.length} series faltantes en '${this.seccion}'.`);
                }

            } catch (error) {
                console.error("❌ Error en compararSeries:", error);
                alert("Error al comparar series de equipos.");
            }
            this.cargando = false;
        },

        /**
         * Carga los datos de Sedes, Servicios y Responsables para el formulario 'General'.
         */
        async cargarSelectoresGeneral() {
            this.cargando = true;
            try {
                // Carga paralela de listas maestras
                const [sedes, responsables, servicios] = await Promise.all([
                    this.obtenerDatos("Sedes"),
                    this.obtenerDatos("Responsables"),
                    this.obtenerDatos("Servicios")
                ]);

                // Asigna los nombres de sede como series (para el dropdown del formulario)
                this.todasSeriesExistentes = sedes.map(s => s.nombre_sede); 

                // Filtra servicios y responsables según la sede seleccionada
                const serviciosFiltrados = servicios.filter(s =>
                    s.nombre_sede === this.sedeSeleccionada
                ).map(s => s.nombre_servicio);
                this.listaServicios = serviciosFiltrados;

                const responsablesFiltrados = responsables.filter(s =>
                    s.nombre_sede === this.sedeSeleccionada
                ).map(s => s.nombre_responsable);
                this.listaResponsables = responsablesFiltrados;

            } catch (error) {
                console.error("❌ Error al cargar selectores:", error);
                alert("Error al cargar sedes, servicios o responsables.");
            }
            this.cargando = false;
        },


        /**
         * Convierte los nombres de los campos a los IDs/valores que espera la API
         * y realiza el POST para guardar.
         * @param {Object} datosFormulario - Datos recibidos del formulario hijo.
         */
        async manejarGuardado(datosFormulario) {
            let datosFinales = null;

            // 1. Convertir los datos del formulario a la estructura de la API
            if (this.seccion === "General") {
                // Mapear nombres a IDs (General solo necesita cargar esto una vez)
                const [sedes, responsables, servicios] = await Promise.all([
                    this.obtenerDatos("Sedes"),
                    this.obtenerDatos("Responsables"),
                    this.obtenerDatos("Servicios")
                ]);
                
                // Función auxiliar para encontrar el ID a partir del nombre
                const buscarId = (lista, nombreKey, valor) => {
                    return lista.find(item => item[nombreKey] === valor)?.id || null;
                };

                datosFinales = {
                    sede: buscarId(sedes, 'nombre_sede', datosFormulario.sede),
                    servicio: buscarId(servicios, 'nombre_servicio', datosFormulario.servicio),
                    responsable_servicio: buscarId(responsables, 'nombre_responsable', datosFormulario.responsable),
                    
                    // Mapeo directo de nombres (limpieza de la estructura original)
                    nombre_equipo: datosFormulario.nombreEquipo,
                    marca_equipo: datosFormulario.marca,
                    modelo_equipo: datosFormulario.modelo,
                    codigo_inventario: datosFormulario.codigoInventario,
                    serie_equipo: datosFormulario.numeroSerie,
                    codigo_ips: datosFormulario.codigoIPS,
                    codigo_ecri: datosFormulario.codigoECRI,
                    ubicacion_fisica: datosFormulario.ubicacion,
                    clasificacion_misional: datosFormulario.clasificacionMisional,
                    clasificacion_ips: datosFormulario.clasificacionIPS,
                    clasificacion_riesgo: datosFormulario.clasificacionRiesgo,
                    registro_invima: datosFormulario.registroInvima,
                    estado_equipo: 1 // Valor fijo
                };

            } else {
                // 2. Mapear la serie de equipos a un ID de equipo (para otras secciones)
                const equiposGeneral = await this.obtenerDatos("General");
                const equipoObj = equiposGeneral.find(
                    s => s.serie_equipo === datosFormulario.serie
                );
                const idEquipo = equipoObj?.id || null;

                // Función auxiliar para obtener el valor o una cadena vacía
                const getValue = (campo) => campo?.value || "";

                // Estructuras de datos para las sub-secciones
                const mapeoSubSecciones = {
                    Registro: {
                        equipo: idEquipo,
                        tiempo_vida_util: getValue(datosFormulario.vidautil),
                        fecha_adquisicion: getValue(datosFormulario.fechaadquisicion),
                        propietario_equipo: getValue(datosFormulario.propietarioequipo),
                        fecha_fabricacion: getValue(datosFormulario.fechafarbicacion),
                        nit: getValue(datosFormulario.nit),
                        proveedor_equipo: getValue(datosFormulario.privedorequipo),
                        estado_garantia: getValue(datosFormulario.estadogarantia),
                        terminacion_garantia: getValue(datosFormulario.terminaciongarantia),
                        forma_adquisicion: getValue(datosFormulario.formaadquisicion),
                        tipo_documento: getValue(datosFormulario.tipodocumento),
                        numero_documento: getValue(datosFormulario.numerodocumento),
                    },
                    MetrologiaA: {
                        equipo: idEquipo,
                        tiene_mantenimiento: getValue(datosFormulario.tienemantenimiento),
                        frecuencia_mto: getValue(datosFormulario.frecuenciamto),
                        tiene_calibracion: getValue(datosFormulario.tienecalibracion),
                        frecuencia_calibracion: getValue(datosFormulario.frecuenciacalibracion),
                    },
                    MetrologiaT: {
                        equipo: idEquipo,
                        magnitud: getValue(datosFormulario.magnitud),
                        rango_equipo: getValue(datosFormulario.rangoequipo),
                        resolucion: getValue(datosFormulario.resolucion),
                        rango_trabajo: getValue(datosFormulario.rangotrabajo),
                        error_maximo: getValue(datosFormulario.errormaximo),
                    },
                    Documentacion: {
                        equipo: idEquipo,
                        manual_mantenimiento: getValue(datosFormulario.manualmantenimiento),
                        hoja_vida: getValue(datosFormulario.hojavida),
                        reg_importacion: getValue(datosFormulario["reg.importacion"]), // Nombre de campo con punto (cuidado)
                        manual_operacion: getValue(datosFormulario.manualoperacion),
                        guia_rapida: getValue(datosFormulario.guiarapida),
                        instructivo: getValue(datosFormulario.intructivo),
                        protocolo_mantenimiento: getValue(datosFormulario.protocolo),
                        frecuencia_metrologica: getValue(datosFormulario.frecuanciam),
                    },
                    Condicion: {
                        equipo: idEquipo,
                        voltaje: getValue(datosFormulario.voltaje),
                        corriente: getValue(datosFormulario.corriente),
                        humedad: getValue(datosFormulario.humedad),
                        temperatura: getValue(datosFormulario.temperatura),
                        dimensiones: getValue(datosFormulario.dimensiones),
                        peso: getValue(datosFormulario.peso),
                        otros: getValue(datosFormulario.otros),
                    },
                };
                datosFinales = mapeoSubSecciones[this.seccion];
            }
            
            // 3. Postear datos
            if (!datosFinales) {
                console.error("❌ No se pudieron generar los datos para la sección:", this.seccion);
                alert("Error: Datos incompletos o sección no reconocida.");
                return;
            }

            try {
                const urlPost = `http://127.0.0.1:8000/api/${this.seccion}/`; // Usar la sección actual para el POST
                const respuesta = await axios.post(urlPost, datosFinales);

                console.log("📌 Registro guardado:", respuesta.data);
                alert("Equipo registrado correctamente");
            } catch (error) {
                console.error("❌ Error al guardar:", error.response?.data || error);
                alert("Hubo un error al guardar. Revisa la consola.");
            }

            // 4. Acciones post-guardado
            await this.listarEquipos();  
            this.toggleAgregar();  
        },

        /** Alterna la visibilidad del formulario de agregar/cancelar */
        toggleAgregar() {
            this.estadoAgregar = !this.estadoAgregar;
            // Si vamos a mostrar el formulario, cargamos los datos necesarios
            if (this.estadoAgregar) {
                this.compararSeries();
            }
        },
        
        /**
         * Maneja el evento de filtros emitido por el componente FiltrosMenu.
         * @param {Object} nuevosFiltros - El objeto de filtros del componente hijo.
         */
        filtrarEquipos(nuevosFiltros) {
            this.filtrosActuales = nuevosFiltros;
            this.listarEquipos(nuevosFiltros);
        },

        /**
         * Maneja el cambio de sección principal.
         * @param {string} seccionNueva - El identificador de la nueva sección.
         */
        cambiarSeccion(seccionNueva) {
            this.seccion = seccionNueva;

            // Reinicia solo los filtros dinámicos al cambiar de sección
            this.filtrosActuales = {
                ...this.filtrosActuales, 
                dinamico1: '',
                dinamico2: '',
                dinamico3: '',
            };
            
            // Cierra el formulario de agregar si estaba abierto
            if (this.estadoAgregar) {
                this.estadoAgregar = false;
            }
            
            // Carga la nueva tabla
            this.listarEquipos();
        }
    },

    mounted() {
        // Carga inicial de la tabla al montar el componente
        this.listarEquipos();
        // Si la sección inicial es 'General', precargar los selectores
        if (this.seccion === 'General') {
            this.cargarSelectoresGeneral();
        }
    },
    
    // Si la sede seleccionada cambia, reactivar la carga de responsables/servicios
    watch: {
        sedeSeleccionada() {
            if (this.seccion === "General" && this.estadoAgregar) {
                this.cargarSelectoresGeneral();
            }
        }
    }
};
</script>
<template>
<div v-if="cargando" class="pantalla-carga">
    <div class="spinner"></div>
    <p>Cargando, por favor espera...</p>
</div>
<div class="background" v-else> 
    <div class="slidebar"></div>
    <div class="menuPrincipal">
        
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones" @click="$router.push('/')">Equipos</button>
            <button class="navbar--opciones" @click="$router.push('/Responsables')">Responsables</button>
            <button class="navbar--opciones" @click="$router.push('/Servicios')">Servicios</button>
        </div>

        <div class="menuPrincipal--secciones">
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'General' }" 
                @click="cambiarSeccion('General')"
            >General</button>
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'Registro' }" 
                @click="cambiarSeccion('Registro')"
            >Registro Histórico</button>
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'MetrologiaA' }" 
                @click="cambiarSeccion('MetrologiaA')"
            >Metrologia Administrativa</button>
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'MetrologiaT' }" 
                @click="cambiarSeccion('MetrologiaT')"
            >Metrologia Técnica</button>
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'Documentacion' }" 
                @click="cambiarSeccion('Documentacion')"
            >Documentación</button>
            <button 
                class="secciones--botones" 
                :class="{ 'active': seccion === 'Condicion' }" 
                @click="cambiarSeccion('Condicion')"
            >Condición Funcionamiento</button>
        </div>

        <div class="menuPrincipal--tablaPrincipal">
            
            <div class="tablaPrincipal--filtros">
                <FiltrosMenu :seccion="seccion" @aplicar-filtros="filtrarEquipos"/>
                
                <div class="tablaPricipal--menuBotones">
                    <button 
                        class="menuBotones--botones agregar" 
                        :class="{ 'activate': estadoAgregar }" 
                        type="button" 
                        @click="toggleAgregar"
                    ></button>
                    <button class="menuBotones--botones" type="button" @click="desactivarEquiposSeleccionados">Desactivar ({{ equiposParaDesactivar.length }})</button>
                </div>
            </div>
            
            <div class="tablaPrincipal--contenedor">
                <TablasEquipos 
                    v-if="!estadoAgregar"
                    :seccion="seccion" 
                    :filas="filas" 
                    @seleccionados-actualizados="actualizarSeleccionados"
                />    
                
                <FormulariosEquipos
                    v-else
                    :todasSeries="todasSeriesExistentes"
                    :listaServicios="listaServicios"
                    :listaResposables="listaResponsables"
                    :seriesInesistentes="seriesFaltantes"
                    :bloqueCampos="debeBloquearCampos"
                    :seccion="seccion"
                    @actualizar-sede="sedeSeleccionada = $event"
                    @guardar-formulario="manejarGuardado"
                />
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
        overflow-y: auto;
    }
    .pantalla-carga {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}

/* Spinner */
.spinner {
    width: 60px;
    height: 60px;
    border: 6px solid #ddd;
    border-top-color: #008073;
    border-radius: 50%;
    animation: girar 1s linear infinite;
}

@keyframes girar {
    to {
        transform: rotate(360deg);
    }
}
</style>
