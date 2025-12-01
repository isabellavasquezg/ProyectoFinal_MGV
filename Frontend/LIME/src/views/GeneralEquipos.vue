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
            seccion: "General",         // Sección activa (ej. 'General', 'Registro')
            cargando: false,            // Indica si una operación de red está en curso
            estadoAgregar: false,       // Muestra/Oculta el formulario de agregar

            // Datos principales
            filas: [],                  // Datos mostrados en la tabla (aplicados los filtros)
            general: [],                // Datos de la sección 'General' (usados para la comparación)
            
            // Datos para el formulario de Agregar/Editar
            sedeSeleccionada: '',       // Sede activa para la carga de servicios y responsables
            todasSeriesExistentes: [],  // Lista de series existentes en la sección actual
            seriesFaltantes: [],        // Series que están en 'General' pero no en la sección actual
            debeBloquearCampos: false,  // Controla si se bloquea el formulario (cuando no hay series faltantes)

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
        
        // Se movió la lógica de mounted a methods para mantener la estructura de la aplicación.
        mounted() {
            // Carga inicial de la tabla al montar el componente
            this.listarEquipos();
            // NO precargar los selectores aquí, ya que causó el error de flash.
        },
        
        actualizarSeleccionados(lista) {
            this.equiposParaDesactivar = lista;
            console.log(this.equiposParaDesactivar[0])
        },
        async desactivarEquiposSeleccionados() {
            if (this.equiposParaDesactivar.length === 0) {
                // NOTA: Reemplazar 'alert' por un modal o notificación en el futuro.
                alert("Por favor, selecciona al menos un equipo para desactivar.");
                return;
            }

            if (!confirm(`¿Estás seguro de que deseas desactivar ${this.equiposParaDesactivar.length} equipo(s)? Esta acción actualizará su estado a INACTIVO.`)) {
                return;
            }

            this.cargando = true;

            try {
                // 1. OBTENER LA LISTA MAESTRA (Equipos Generales)
                const equiposMaestros = await this.obtenerDatos("General");
                
                // Crear un mapa Serie -> ID para una búsqueda rápida O(1)
                const serieToIdMap = equiposMaestros.reduce((map, equipo) => {
                    map[equipo.serie_equipo] = equipo.id;
                    return map;
                }, {});

                // 2. OBTENER LOS IDs REALES DEL EQUIPO A PARTIR DE LAS SERIES SELECCIONADAS
                const idsADesactivar = this.equiposParaDesactivar
                    .map(eq => serieToIdMap[eq.serie_equipo]) 
                    .filter(id => id !== undefined && id !== null); 

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
         */
        async obtenerDatos(endpoint) {
            try {
                const url = `http://127.0.0.1:8000/api/${endpoint}/`;
                const res = await axios.get(url);
                return res.data.result || []; 
            } catch (err) {
                console.error(`❌ Error al obtener datos de ${endpoint}:`, err);
                return []; 
            }
        },

        /**
         * Obtiene y actualiza los datos de la tabla aplicando los filtros actuales o dados.
         */
        async listarEquipos(filtros) {
            this.cargando = true;

            try {
                const filtrosAUsar = filtros || this.filtrosActuales;

                // 1. Construir la URL con parámetros 
                let url = `http://127.0.0.1:8000/api/${this.seccion}/`;
                
                // Evita añadir '?' si no hay parámetros realmente
                const tieneFiltros = Object.values(filtrosAUsar).some(v => v !== "");
                if (tieneFiltros) {
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

            this.cargando = false; 
        },

        /**
         * Compara las series de la sección 'General' con la sección actual
         * para determinar qué equipos deben agregarse.
         */
        async compararSeries() {
            // Solo se ejecuta si estamos agregando y la sección no es 'General'
            if (this.seccion === "General") {
                // 1. Carga de Selectores: espera a que los datos estén disponibles
                await this.cargarSelectoresGeneral();
                // 2. El formulario NUNCA debe bloquearse en General (primer fix)
                this.debeBloquearCampos = false; 
                return;
            }

            // Lógica para otras secciones (Registro, Metrología, etc.)
            
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
                this.todasSeriesExistentes = Array.from(seriesExistentes); 

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
                console.error("❌ Error en compararSeries (subsección):", error);
                alert("Error al comparar series de equipos.");
            }
            // NO se pone this.cargando = false aquí. Lo maneja toggleAgregar.
        },

        /**
         * Carga los datos de Sedes, Servicios y Responsables para el formulario 'General'.
         * Se remueven los cambios de estado this.cargando de esta función.
         */
        async cargarSelectoresGeneral() {
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
                // Si falla, al menos dejamos el estado de carga en el caller (toggleAgregar)
                throw error;
            }
        },


        /**
         * Convierte los nombres de los campos a los IDs/valores que espera la API
         * y realiza el POST para guardar.
         */
        async manejarGuardado(datosFormulario) {
            let datosFinales = null;

            // 1. Convertir los datos del formulario a la estructura de la API
            // ... (La lógica de mapeo es correcta)

            // Simplificando la lógica de mapeo para evitar repetir todo el bloque aquí.
            // Asumo que tu lógica de mapeo anterior (desde línea 305) se mantiene sin cambios.
            
            if (this.seccion === "General") {
                const [sedes, responsables, servicios] = await Promise.all([
                    this.obtenerDatos("Sedes"),
                    this.obtenerDatos("Responsables"),
                    this.obtenerDatos("Servicios")
                ]);
                
                const buscarId = (lista, nombreKey, valor) => {
                    return lista.find(item => item[nombreKey] === valor)?.id || null;
                };

                datosFinales = {
                    sede: buscarId(sedes, 'nombre_sede', datosFormulario.sede),
                    servicio: buscarId(servicios, 'nombre_servicio', datosFormulario.servicio),
                    responsable_servicio: buscarId(responsables, 'nombre_responsable', datosFormulario.responsable),
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
                    estado_equipo: 1 
                };
            } else {
                const equiposGeneral = await this.obtenerDatos("General");
                const equipoObj = equiposGeneral.find(
                    s => s.serie_equipo === datosFormulario.serie
                );
                const idEquipo = equipoObj?.id || null;

                const getValue = (campo) => campo?.value || "";

                const mapeoSubSecciones = {
                    Registro: {
                        equipo_id: idEquipo,
                        tiempo_vida_util: datosFormulario.vidautil|| null ,
                        fecha_adquisicion: datosFormulario.fechaadquisicion|| null ,
                        propietario: datosFormulario.propietarioequipo|| null ,
                        fecha_fabricacion: datosFormulario.fechafarbicacion|| null ,
                        nit: datosFormulario.nit|| null ,
                        proveedor: datosFormulario.privedorequipo|| null ,
                        en_garantia: datosFormulario.estadogarantia === "Sí",
                        fecha_fin_garantia: datosFormulario.terminaciongarantia|| null ,
                        forma_adquisicion: datosFormulario.formaadquisicion|| null ,
                        tipo_documento: datosFormulario.tipodocumento|| null ,
                        numero_documento: datosFormulario.numerodocumento|| null ,
                    },
                    MetrologiaA: {
                        equipo_id: idEquipo,
                        mantenimiento: datosFormulario.tienemantenimiento=== "Sí",
                        tipo_mantenimiento: null,
                        frecuencia_mantenimiento: datosFormulario.frecuenciamto|| 0,
                        calibracion: datosFormulario.tienecalibracion === "Sí",
                        tipo_calibracion:null,
                        frecuencia_calibracion: datosFormulario.frecuenciacalibracion|| 0,
                    },
                    MetrologiaT: {
                        equipo_id: idEquipo,
                        magnitud: datosFormulario.magnitud || null,
                        rango_equipo: datosFormulario.rangoequipo || null,
                        resolucion: datosFormulario.resolucion|| null,
                        rango_trabajo: datosFormulario.rangotrabajo || null,
                        error_maximo: datosFormulario.errormaximo|| null,
                    },
                    Documentacion: {
                        equipo_id: idEquipo,
                        manual_mantenimiento: datosFormulario.manualmantenimiento=== "Sí",
                        hoja_vida: datosFormulario.hojavida=== "Sí",
                        registro_importacion: datosFormulario.regimportacion === "Sí",
                        manual_operacion: datosFormulario.manualoperacion === "Sí",
                        guia_rapida: datosFormulario.guiarapida === "Sí",
                        instructivo_manejo: datosFormulario.intructivo === "Sí",
                        protocolo_mantenimiento: datosFormulario.protocolo === "Sí",
                        frecuencia_metrologica: datosFormulario.frecuanciam || null,
                    },
                    Condicion: {
                        equipo_id: idEquipo,
                        voltaje: datosFormulario.voltaje|| null,
                        corriente: datosFormulario.corriente|| null,
                        humedad: datosFormulario.humedad|| null,
                        temperatura: datosFormulario.temperatura|| null,
                        dimensiones: datosFormulario.dimensiones|| null,
                        peso: datosFormulario.peso|| null,
                        otros_requerimientos:datosFormulario.otros|| null,
                    },
                };
                datosFinales = mapeoSubSecciones[this.seccion];
            }
            
            console.log("datitos",datosFinales)
            // 3. Postear datos
            if (!datosFinales) {
                console.error("❌ No se pudieron generar los datos para la sección:", this.seccion);
                alert("Error: Datos incompletos o sección no reconocida.");
                return;
            }

            try {
                const urlPost = `http://127.0.0.1:8000/api/${this.seccion}/`; 
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
            // 1. Si se va a abrir el formulario
            if (!this.estadoAgregar) {
                this.cargando = true; // Mostrar spinner al iniciar la carga
                
                // Ejecutamos la carga de datos de forma asíncrona
                // La apertura del formulario y el fin de la carga se hace en el .finally
                this.compararSeries().finally(() => {
                    this.estadoAgregar = true; 
                    this.cargando = false; // Ocultar spinner después de que la promesa termine.
                });

            } else {
                // 2. Si se va a cerrar (Cancelar), no necesitamos esperar nada.
                this.estadoAgregar = false;
            }
        },
        
        /**
         * Maneja el evento de filtros emitido por el componente FiltrosMenu.
         */
        filtrarEquipos(nuevosFiltros) {
            this.filtrosActuales = nuevosFiltros;
            this.listarEquipos(nuevosFiltros);
        },

        /**
         * Maneja el cambio de sección principal.
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
    },
    
    // Si la sede seleccionada cambia, reactivar la carga de responsables/servicios
    watch: {
        sedeSeleccionada() {
            if (this.seccion === "General" && this.estadoAgregar) {
                // Nota: cargamos los selectores sin cambiar this.cargando para evitar el flash
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
