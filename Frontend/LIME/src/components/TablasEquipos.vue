<script>
/**
 * Componente dinámico para mostrar diferentes tablas de equipos
 * según la sección activa. Incorpora lógica de selección múltiple
 * (checkboxes) y menú de opciones por fila.
 */
export default {
    name: "TablasEquipos",

    // Propiedades recibidas del componente padre
    props: {
        seccion: {
            type: String,
            required: true,
            // Validación para asegurar que la sección sea una de las esperadas
            validator: (value) => [
                'General', 'Registro', 'MetrologiaA', 'MetrologiaT', 'Documentacion', 'Condicion'
            ].includes(value)
        },
        filas: { 
            type: Array,
            required: true,
            default: () => []
        },
    },

    data() {
        return {
            // Copia interna de las filas con estado reactivo de la UI
            filasConEstado: [],
            // Estado del checkbox principal para seleccionar/deseleccionar todas
            seleccionarTodos: false,
            
            // Configuración de encabezados para cada sección (COLUMNAS DINÁMICAS)
            columnas: {
                General: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'marca_equipo', label: 'Marca' },
                    { key: 'modelo_equipo', label: 'Modelo' },
                    { key: 'nombre_equipo', label: 'Nombre Equipo' },
                    { key: 'nombre_responsable', label: 'Responsable Servicio' },
                    { key: 'codigo_inventario', label: 'Código Inventario' },
                    { key: 'codigo_ips', label: 'Código IPS' },
                    { key: 'codigo_ecri', label: 'Código ECRI' },
                    { key: 'ubicacion_fisica', label: 'Ubicación' },
                    { key: 'clasificacion_misional', label: 'Clasificación Misional' },
                    { key: 'clasificacion_ips', label: 'Clasificación IPS' },
                    { key: 'clasificacion_riesgo', label: 'Clasificación Riesgo' },
                    { key: 'registro_invima', label: 'Registro Invima' },
                ],
                Registro: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'tiempo_vida_util', label: 'Vida Útil' },
                    { key: 'fecha_adquisicion', label: 'Fecha Adquisición' },
                    { key: 'propietario', label: 'Propietario Equipo' },
                    { key: 'fecha_fabricacion', label: 'Fecha de Fabricación' },
                    { key: 'nit', label: 'NIT' },
                    { key: 'proveedor', label: 'Proveedor Equipo' },
                    { key: 'en_garantia', label: 'Estado de Garantía', isBoolean: true },
                    { key: 'fecha_fin_garantia', label: 'Terminación Garantía' },
                    { key: 'forma_adquisicion', label: 'Forma Adquisición' },
                    { key: 'tipo_documento', label: 'Tipo Documento' },
                    { key: 'numero_documento', label: 'Número Documento' },
                ],
                MetrologiaA: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'mantenimiento_requerido', label: 'Tiene Mantenimiento', isBoolean: true },
                    { key: 'frecuencia_mantenimiento', label: 'Frecuencia Mto' },
                    { key: 'calibracion_requerida', label: 'Tiene Calibración', isBoolean: true },
                    { key: 'frecuencia_calibracion', label: 'Frecuencia Calibración' },
                ],
                MetrologiaT: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'magnitud', label: 'Magnitud' },
                    { key: 'rango_equipo', label: 'Rango Equipo' },
                    { key: 'resolucion', label: 'Resolución' },
                    { key: 'rango_trabajo', label: 'Rango Trabajo' },
                    { key: 'error_maximo', label: 'Error Máximo' },
                ],
                Documentacion: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'hoja_vida', label: 'Hoja de Vida', isBoolean: true },
                    { key: 'registro_importacion', label: 'Reg. Importación', isBoolean: true },
                    { key: 'manual_operacion', label: 'Manual Operación', isBoolean: true },
                    { key: 'manual_mantenimiento', label: 'Manual Mantenimiento', isBoolean: true },
                    { key: 'guia_rapida', label: 'Guía Rápida', isBoolean: true },
                    { key: 'instructivo_manejo', label: 'Instructivo Uso', isBoolean: true },
                    { key: 'protocolo_mantenimiento', label: 'Protocolo Mantenimiento', isBoolean: true },
                    { key: 'frecuencia_metrologica', label: 'Frec. Metrológica' },
                ],
                Condicion: [
                    { key: 'nombre_sede', label: 'Sede' },
                    { key: 'nombre_servicio', label: 'Servicio' },
                    { key: 'serie_equipo', label: 'Número de Serie' },
                    { key: 'voltaje', label: 'Voltaje' },
                    { key: 'corriente', label: 'Corriente' },
                    { key: 'humedad', label: 'Humedad Relativa' },
                    { key: 'temperatura', label: 'Temperatura' },
                    { key: 'dimensiones', label: 'Dimensiones' },
                    { key: 'peso', label: 'Peso' },
                    { key: 'otros_requerimientos', label: 'Otros' },
                ],
            }
        };
    },
    
    // Propiedad computada para obtener las columnas de la sección actual
    computed: {
        columnasActuales() {
            return this.columnas[this.seccion] || [];
        },
        equiposSeleccionados() {
            return this.filasConEstado.filter(fila => fila.seleccionado);
        },
    },

    watch: {
        /**
         * Observa cambios en la prop 'filas' y actualiza el estado interno 'filasConEstado'.
         * Esto permite que el componente añada las propiedades reactivas (mostrarOpciones, seleccionado)
         * sin modificar las props directamente.
         */
        filas: {
            handler(newFilas) {
                this.filasConEstado = this.inicializarFilas(newFilas);
            },
            immediate: true,  // Ejecuta la primera vez al montar el componente
            deep: true,       // Observa cambios dentro del array (por si se edita una fila)
        },
        equiposSeleccionados: {
            handler(nuevosSeleccionados) {
                this.$emit('seleccionados-actualizados', nuevosSeleccionados);
            },
            deep: true,
        }
    },

    methods: {
        /**
         * @param {Array} filas - El array de datos de equipos.
         * @returns {Array} Una nueva lista de filas con los estados de UI agregados.
         * Agrega las propiedades 'mostrarOpciones' y 'seleccionado' a cada fila.
         */
        inicializarFilas(filas) {
            return filas.map(fila => ({
                ...fila, 
                // Evita sobrescribir si ya existe (mantener estado de checkbox al filtrar)
                mostrarOpciones: fila.mostrarOpciones || false, 
                seleccionado: fila.seleccionado || false 
            }));
        },

        /**
         * Muestra/oculta el dropdown de opciones para la fila dada.
         * También cierra cualquier otro dropdown que pueda estar abierto.
         * @param {number} index - Índice de la fila a alternar.
         */
        toggleDropdown(index) {
            // 1. Cerrar todos los demás dropdowns
            this.filasConEstado.forEach((fila, i) => {
                if (i !== index) {
                    fila.mostrarOpciones = false;
                }
            });

            // 2. Alternar el estado del dropdown actual
            this.filasConEstado[index].mostrarOpciones =
                !this.filasConEstado[index].mostrarOpciones;
        },

        /**
         * Alterna el estado de selección de TODAS las filas
         * basándose en el estado del checkbox principal (seleccionarTodos).
         */
        toggleSeleccionarTodos() {
            this.filasConEstado.forEach(fila => {
                fila.seleccionado = this.seleccionarTodos;
            });
        },

        /**
         * Revisa el estado de los checkboxes de las filas.
         * Si todas están seleccionadas, marca el checkbox principal. Si no, lo desmarca.
         */
        actualizarSeleccionarTodos() {
            this.seleccionarTodos = this.filasConEstado.every(f => f.seleccionado);
        },

        // --- MÉTODOS DE ACCIÓN (A SER REEMPLAZADOS POR EMITIR EVENTOS) ---
        /** @param {Object} equipo - Fila de datos del equipo. */
        verEquipo(equipo) {
            console.log('Ver equipo:', equipo.serie_equipo);
            // En una aplicación real, se emitiría un evento: this.$emit('ver-equipo', equipo);
        },
        /** @param {Object} equipo - Fila de datos del equipo. */
        trasladarEquipo(equipo) {
            console.log('Trasladar equipo:', equipo.serie_equipo);
            // En una aplicación real, se emitiría un evento: this.$emit('trasladar-equipo', equipo);
        },
        /** @param {Object} equipo - Fila de datos del equipo. */
        editarEquipo(equipo) {
            console.log('Editar equipo:', equipo.serie_equipo);
            // En una aplicación real, se emitiría un evento: this.$emit('editar-equipo', equipo);
        }
    },
};
</script>

<template>
    <table class="tabla">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input 
                        id="checkHeader" 
                        type="checkbox" 
                        v-model="seleccionarTodos" 
                        @change="toggleSeleccionarTodos"
                    />
                </th>

                <th 
                    v-for="columna in columnasActuales" 
                    :key="columna.key" 
                    class="tabla--headers"
                >
                    {{ columna.label }}
                </th>
                
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(fila, index) in filasConEstado" :key="fila.serie_equipo">
                <td>
                    <input 
                        class="checkRow"
                        type="checkbox" 
                        v-model="fila.seleccionado" 
                        @change="actualizarSeleccionarTodos"
                    />
                </td>

                <td v-for="columna in columnasActuales" :key="columna.key">
                    <template v-if="columna.isBoolean">
                        {{ fila[columna.key] ? 'Sí' : 'No' }}
                    </template>
                    <template v-else>
                        {{ fila[columna.key] }}
                    </template>
                </td>

                <td class="dropdown-cell">
                    <div class="dropdown">

                        <button class="tabla--boton" @click="toggleDropdown(index)">
                            Opciones
                        </button>

                        <div v-show="fila.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(fila)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(fila)">Editar</a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style>
    /* --------------------- ESTILOS GENERALES --------------------- */

    /* Tabla base */
    .tabla {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 10px;
    }

    /* Encabezado principal */
    .tabla--header {
        border-radius: 10px 10px 0 0;
        background-color: #008073;
        color: white;
        text-align: left;
    }

    /* Celdas de encabezado */
    .tabla--headers,
    .tabla--headersCheck {
        padding: 10px 8px;
        border-bottom: 2px solid #01a393;
        font-weight: bold;
    }

    /* Filas */
    .tabla--fila td {
        background-color: white;
        color: #555;
        padding: 8px 6px;
        border-bottom: 1px solid #e5e5e5;
    }

    /* Hover */
    .tabla--fila:hover td {
        background-color: #f5f7fa;
    }

    /* Checkbox */
    .tabla input[type="checkbox"] {
        width: 16px;
        height: 16px;
        cursor: pointer;
    }

    /* Botón de acciones */
    .tabla--boton {
        font-size: 10px;
        height: 22px;
        width: 70px;
        background-color: #0a346c;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
    }

    /* Dropdown */
    .dropdown-cell {
        position: relative;
        overflow: visible;
    }

    .dropdown {
        position: relative;
        display: inline-block;
    }

    /* Menú desplegable */
    .dropdown-menu {

        position: absolute;
        right: 1%;
        top: 100%;
        z-index: 100;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border-radius: 4px;
        min-width: 120px;
        padding: 5px 0;
        margin-top: 5px;
        border: 1px solid #ddd;
    }

    /* Items del menú */
    .dropdown-item {
        display: block;
        padding: 8px 15px;
        text-decoration: none;
        color: #333;
        white-space: nowrap;
        transition: background-color 0.2s;
    }

    .dropdown-item:hover {
        background-color: #f0f0f0;
        color: #0a346c;
    }
</style>
