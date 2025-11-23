<script>
export default {
    name: "TablasEquipos",

    // Recibe la sección activa y las filas de datos desde el padre
    props: {
        seccion: {
            type: String,
            required: true
        },
        filas: { 
            type: Array,
            required: true,
            default: () => []
        },
    },

    data() {
        return {
            // Copia interna de filas, pero con estado adicional (mostrarOpciones)
            equiposConEstado: [],
        };
    },

    watch: {
        // Observa cambios en filas y vuelve a inicializar el estado interno
        filas: {
            handler(newFilas) {
                this.equiposConEstado = this.inicializarFilas(newFilas);
            },
            immediate: true,  // Ejecuta al montar el componente
        }
    },

    methods: {
        /**
         * Agrega la propiedad mostrarOpciones a cada fila
         * para gestionar individualmente el menú desplegable.
         */
        inicializarFilas(filas) {
            return filas.map(fila => ({
                ...fila, 
                mostrarOpciones: false
            }));
        },

        // Cambia la sección actual (aunque normalmente esto lo maneja el padre)
        cambiarSeccion(seccionNueva){
            this.seccion = seccionNueva;
        },

        toggleDropdown(index) {
            this.equiposConEstado.forEach((fila, i) => {
                if (i !== index) {
                    fila.mostrarOpciones = false;
                }
            });

            this.equiposConEstado[index].mostrarOpciones =
                !this.equiposConEstado[index].mostrarOpciones;
        },

        // Acciones básicas del menú de opciones (por ahora solo impresiones)
        verEquipo(equipo) {
            console.log('Ver equipo:', equipo.serie_equipo);
        },
        trasladarEquipo(equipo) {
            console.log('Trasladar equipo:', equipo.serie_equipo);
        },
        editarEquipo(equipo) {
            console.log('Editar equipo:', equipo.serie_equipo);
        }
    },
};
</script>

<template>
    <!-- ========================================================= -->
    <!-- ====================== SECCIÓN GENERAL =================== -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='General'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox"/>
                </th>

                <!-- Encabezados de columnas de Equipos Generales -->
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Marca</th>
                <th class="tabla--headers">Modelo</th>
                <th class="tabla--headers">Nombre Equipo</th>
                <th class="tabla--headers">Responsable Servicio</th>
                <th class="tabla--headers">Código Inventario</th>
                <th class="tabla--headers">Código IPS</th>
                <th class="tabla--headers">Código ECRI</th>
                <th class="tabla--headers">Ubicación</th>
                <th class="tabla--headers">Clasificación Misional</th>
                <th class="tabla--headers">Clasificación IPS</th>
                <th class="tabla--headers">Clasificación Riesgo</th>
                <th class="tabla--headers">Registro Invima</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(eq, index) in equiposConEstado" :key="eq.serie_equipo">
                <!-- Checkbox por fila -->
                <td><input class="checkRow" type="checkbox"/></td>

                <!-- Datos del equipo -->
                <td>{{ eq.nombre_sede }}</td>
                <td>{{ eq.nombre_servicio }}</td>
                <td>{{ eq.serie_equipo }}</td>
                <td>{{ eq.marca_equipo }}</td>
                <td>{{ eq.modelo_equipo }}</td>
                <td>{{ eq.nombre_equipo }}</td>
                <td>{{ eq.nombre_responsable }}</td>
                <td>{{ eq.codigo_inventario }}</td>
                <td>{{ eq.codigo_ips }}</td>
                <td>{{ eq.codigo_ecri }}</td>
                <td>{{ eq.ubicacion_fisica }}</td>
                <td>{{ eq.clasificacion_misional }}</td>
                <td>{{ eq.clasificacion_ips }}</td>
                <td>{{ eq.clasificacion_riesgo }}</td>
                <td>{{ eq.registro_invima }}</td>

                <!-- Botón + menú de acciones -->
                <td class="dropdown-cell">
                    <div class="dropdown">

                        <button class="tabla--boton" @click="toggleDropdown(index)">
                            Opciones
                        </button>

                        <div v-show="eq.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(eq)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(eq)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(eq)">Editar</a>
                        </div>

                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ========================================================= -->
    <!-- ================= SECCIÓN REGISTRO DE EQUIPOS ============ -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='Registro'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck"><input id="checkHeader" type="checkbox" /></th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Vida Util</th>
                <th class="tabla--headers">Fecha Adquisicion</th>
                <th class="tabla--headers">Propietario Equipo</th>
                <th class="tabla--headers">Fecha de Fabricacion</th>
                <th class="tabla--headers">NIT</th>
                <th class="tabla--headers">Proveedor Equipo</th>
                <th class="tabla--headers">Estado de Garantía</th>
                <th class="tabla--headers">Terminación Garantía</th>
                <th class="tabla--headers">Forma Adquisición</th>
                <th class="tabla--headers">Tipo Documento</th>
                <th class="tabla--headers">Número Documento</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(re, index) in equiposConEstado" :key="re.serie_equipo">
                <td><input class="checkRow" type="checkbox" /></td>

                <!-- Datos del registro -->
                <td>{{ re.nombre_sede }}</td>
                <td>{{ re.nombre_servicio }}</td>
                <td>{{ re.serie_equipo }}</td>
                <td>{{ re.tiempo_vida_util }}</td>
                <td>{{ re.fecha_adquisicion }}</td>
                <td>{{ re.propietario }}</td>
                <td>{{ re.fecha_fabricacion }}</td>
                <td>{{ re.nit }}</td>
                <td>{{ re.proveedor }}</td>
                <td>{{ re.en_garantia ? 'Sí' : 'No' }}</td>
                <td>{{ re.fecha_fin_garantia }}</td>
                <td>{{ re.forma_adquisicion }}</td>
                <td>{{ re.tipo_documento }}</td>
                <td>{{ re.numero_documento }}</td>

                <!-- Dropdown acciones -->
                <td class="dropdown-cell">
                    <div class="dropdown">
                        <button class="tabla--boton" @click="toggleDropdown(index)">Opciones</button>

                        <div v-show="re.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(re)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(re)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(re)">Editar</a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ========================================================= -->
    <!-- ============ SECCIÓN METROLOGÍA (ADMINISTRATIVA) ========= -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='MetrologiaA'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck"><input type="checkbox"/></th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Tiene Mantenimiento</th>
                <th class="tabla--headers">Tipo Mantenimiento</th>
                <th class="tabla--headers">Frecuencia Mto</th>
                <th class="tabla--headers">Tiene Calibración</th>
                <th class="tabla--headers">Tipo Calibración</th>
                <th class="tabla--headers">Frecuencia Calibración</th>
                <th class="tabla--headers">Acciones</th>
            </tr>
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(ma, index) in equiposConEstado" :key="ma.serie_equipo">
                <td><input class="checkRow" type="checkbox" /></td>

                <td>{{ ma.nombre_sede }}</td>
                <td>{{ ma.nombre_servicio }}</td>
                <td>{{ ma.serie_equipo }}</td>
                <td>{{ ma.mantenimiento_requerido ? 'Sí' : 'No' }}</td>
                <td>{{ ma.tipo_mantenimiento }}</td>
                <td>{{ ma.frecuencia_mantenimiento }}</td>
                <td>{{ ma.calibracion_requerida ? 'Sí' : 'No' }}</td>
                <td>{{ ma.tipo_calibracion }}</td>
                <td>{{ ma.frecuencia_calibracion }}</td>

                <!-- Dropdown -->
                <td class="dropdown-cell">
                    <div class="dropdown">
                        <button class="tabla--boton" @click="toggleDropdown(index)">Opciones</button>

                        <div v-show="ma.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(ma)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(ma)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(ma)">Editar</a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ========================================================= -->
    <!-- ========== SECCIÓN METROLOGÍA (TÉCNICA) ================== -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='MetrologiaT'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck"><input type="checkbox"/></th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Magnitud</th>
                <th class="tabla--headers">Rango Equipo</th>
                <th class="tabla--headers">Resolución</th>
                <th class="tabla--headers">Rango Trabajo</th>
                <th class="tabla--headers">Error Máximo</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(mt, index) in equiposConEstado" :key="mt.serie_equipo">
                <td><input class="checkRow" type="checkbox" /></td>

                <td>{{ mt.nombre_sede }}</td>
                <td>{{ mt.nombre_servicio }}</td>
                <td>{{ mt.serie_equipo }}</td>
                <td>{{ mt.magnitud }}</td>
                <td>{{ mt.rango_equipo }}</td>
                <td>{{ mt.resolucion }}</td>
                <td>{{ mt.rango_trabajo }}</td>
                <td>{{ mt.error_maximo }}</td>

                <td class="dropdown-cell">
                    <div class="dropdown">
                        <button class="tabla--boton" @click="toggleDropdown(index)">Opciones</button>

                        <div v-show="mt.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(mt)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(mt)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(mt)">Editar</a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ========================================================= -->
    <!-- ================== SECCIÓN DOCUMENTACIÓN ================= -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='Documentacion'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck"><input type="checkbox"/></th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Hoja de Vida</th>
                <th class="tabla--headers">Reg. Importación</th>
                <th class="tabla--headers">Manual Operación</th>
                <th class="tabla--headers">Manual Mantenimiento</th>
                <th class="tabla--headers">Guía Rápida</th>
                <th class="tabla--headers">Instructivo Uso</th>
                <th class="tabla--headers">Protocolo Mantenimiento</th>
                <th class="tabla--headers">Frec. Metrológica</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(doc, index) in equiposConEstado" :key="doc.serie_equipo">
                <td><input class="checkRow" type="checkbox" /></td>

                <td>{{ doc.nombre_sede }}</td>
                <td>{{ doc.nombre_servicio }}</td>
                <td>{{ doc.serie_equipo }}</td>
                <td>{{ doc.hoja_vida ? 'Sí' : 'No' }}</td>
                <td>{{ doc.registro_importacion ? 'Sí' : 'No' }}</td>
                <td>{{ doc.manual_operacion ? 'Sí' : 'No' }}</td>
                <td>{{ doc.manual_mantenimiento ? 'Sí' : 'No' }}</td>
                <td>{{ doc.guia_rapida ? 'Sí' : 'No' }}</td>
                <td>{{ doc.instructivo_manejo ? 'Sí' : 'No' }}</td>
                <td>{{ doc.protocolo_mantenimiento ? 'Sí' : 'No' }}</td>
                <td>{{ doc.frecuencia_metrologica }}</td>

                <td class="dropdown-cell">
                    <div class="dropdown">
                        <button class="tabla--boton" @click="toggleDropdown(index)">Opciones</button>

                        <div v-show="doc.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(doc)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(doc)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(doc)">Editar</a>
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- ========================================================= -->
    <!-- ================== SECCIÓN CONDICIÓN ===================== -->
    <!-- ========================================================= -->
    <table class="tabla" v-if="seccion=='Condicion'">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck"><input type="checkbox"/></th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Número de Serie</th>
                <th class="tabla--headers">Voltaje</th>
                <th class="tabla--headers">Corriente</th>
                <th class="tabla--headers">Humedad Relativa</th>
                <th class="tabla--headers">Temperatura</th>
                <th class="tabla--headers">Dimensiones</th>
                <th class="tabla--headers">Peso</th>
                <th class="tabla--headers">Otros</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr class="tabla--fila" v-for="(con, index) in equiposConEstado" :key="con.serie_equipo">
                <td><input class="checkRow" type="checkbox" /></td>

                <td>{{ con.nombre_sede }}</td>
                <td>{{ con.nombre_servicio }}</td>
                <td>{{ con.serie_equipo }}</td>
                <td>{{ con.voltaje }}</td>
                <td>{{ con.corriente }}</td>
                <td>{{ con.humedad }}</td>
                <td>{{ con.temperatura }}</td>
                <td>{{ con.dimensiones }}</td>
                <td>{{ con.peso }}</td>
                <td>{{ con.otros_requerimientos }}</td>

                <!-- Dropdown acciones -->
                <td class="dropdown-cell">
                    <div class="dropdown">
                        <button class="tabla--boton" @click="toggleDropdown(index)">
                            Opciones
                        </button>

                        <div v-show="con.mostrarOpciones" class="dropdown-menu">
                            <a href="#" class="dropdown-item" @click.prevent="verEquipo(con)">Ver</a>
                            <a href="#" class="dropdown-item" @click.prevent="trasladarEquipo(con)">Traslado</a>
                            <a href="#" class="dropdown-item" @click.prevent="editarEquipo(con)">Editar</a>
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
        left: 0;
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
