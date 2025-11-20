<script>
export default {
    name: "TablasEquipos",
    props: {
        seccion: {
            type: String,
            required: true
        }
    },
    methods: {
        cambiarSeccion(seccionNueva){
            this.seccion = seccionNueva;
        }  
    },
    computed: {
        fontSizeDinamico() {
            switch (this.seccion) {
            case "General":
                return "12px";
            case "Registro":
                return "12px";
            case "MetrologiaA":
                return "13px";
            case "MetrologiaT":
                return "13px";
            case "Documentacion":
                return "12px";
            default:
                return "12px";
            }
        }
    }
};
</script>
<template> 
    <table class="tabla" v-if="seccion=='General'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Nombre Equipo</th>
                <th class="tabla--headers">Codigo Inventario</th>
                <th class="tabla--headers">Codigo IPS</th>
                <th class="tabla--headers">Codigo ECRI</th>
                <th class="tabla--headers">Responsable Servicio</th>
                <th class="tabla--headers">Ubicación</th>
                <th class="tabla--headers">Marca</th>
                <th class="tabla--headers">Modelo</th>
                <th class="tabla--headers">Serie</th>
                <th class="tabla--headers">Clasificación Misional</th>
                <th class="tabla--headers">Clasificación IPS</th>
                <th class="tabla--headers">Clasificación Riesgo</th>
                <th class="tabla--headers">Registro Invima</th>
                <th class="tabla--headers">Estado</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>Principal</td>
                <td>22223</td>
                <td>Urgencias</td>
                <td>Monitor de Signos</td>
                <td>IPS-001</td>
                <td>ECRI-1010</td>
                <td>Juan Pérez</td>
                <td>Sala 3</td>
                <td>Philips</td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>Norte</td>
                <td>2222s3</td>
                <td>Hospitalización</td>
                <td>Bomba de Infusión</td>
                <td>IPS-002</td>
                <td>ECRI-2201</td>
                <td>Laura Gómez</td>
                <td>Habitación 12</td>
                <td>Mindray</td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    <table class="tabla" v-if="seccion=='Registro'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Numero de Serie</th>
                <th class="tabla--headers">Vida Util</th>
                <th class="tabla--headers">Fecha Adquisicion</th>
                <th class="tabla--headers">Propietario Equipo</th>
                <th class="tabla--headers">Fecha de Fabricacion</th>
                <th class="tabla--headers">NIT</th>
                <th class="tabla--headers">Proveedro Equipo</th>
                <th class="tabla--headers">Estado Garantia</th>
                <th class="tabla--headers">Terminación Garantia</th>
                <th class="tabla--headers">Forma Adquisicion</th>
                <th class="tabla--headers">Tipo Documento</th>
                <th class="tabla--headers">Numero Documento</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>Urgencias</td>
                <td>Monitor de Signos</td>
                <td>IPS-001</td>
                <td>ECRI-1010</td>
                <td>Juan Pérez</td>
                <td>Sala 3</td>
                <td>Philips</td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>Hospitalización</td>
                <td>Bomba de Infusión</td>
                <td>IPS-002</td>
                <td>ECRI-2201</td>
                <td>Laura Gómez</td>
                <td>Habitación 12</td>
                <td>Mindray</td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    <table class="tabla" v-if="seccion=='MetrologiaA'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Numero de Serie</th>
                <th class="tabla--headers">Realiza Mantenimientos</th>
                <th class="tabla--headers">Frecuencia Mantenimiento</th>
                <th class="tabla--headers">Realiza Calibración</th>
                <th class="tabla--headers">Frecuencia Calibración</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    <table class="tabla" v-if="seccion=='MetrologiaT'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Numero de Serie</th>
                <th class="tabla--headers">Magnitud</th>
                <th class="tabla--headers">Rango del Equipo</th>
                <th class="tabla--headers">Resolución</th>
                <th class="tabla--headers">Rango de Trabajo</th>
                <th class="tabla--headers">Error Maximo Permitido</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>Philips</td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>Mindray</td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    <table class="tabla" v-if="seccion=='Documentacion'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Numero de Serie</th>
                <th class="tabla--headers">Hoja de vida</th>
                <th class="tabla--headers">Registro de Importación</th>
                <th class="tabla--headers">Manual de Operación</th>
                <th class="tabla--headers">Manual de Servicio</th>
                <th class="tabla--headers">Guia Rapida de Uso</th>
                <th class="tabla--headers">Instructivo de Manejo Rapido</th>
                <th class="tabla--headers">Protoclo Mto Prev.</th>
                <th class="tabla--headers">Frec. Metrologica Fabricante</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>Hospitalización</td>
                <td>Bomba de Infusión</td>
                <td>Habitación 12</td>
                <td>Philips</td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>Hospitalización</td>
                <td>Bomba de Infusión</td>
                <td>Habitación 12</td>
                <td>Mindray</td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    <table class="tabla" v-if="seccion=='Condicion'" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input id="checkHeader" type="checkbox" />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Numero de Serie</th>
                <th class="tabla--headers">Voltaje</th>
                <th class="tabla--headers">Corriente</th>
                <th class="tabla--headers">Humedad Relativa</th>
                <th class="tabla--headers">Temperatura</th>
                <th class="tabla--headers">Dimensiones</th>
                <th class="tabla--headers">Peso</th>
                <th class="tabla--headers">Otro</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <!-- Fila 1 -->
            <tr class="tabla--fila">
                <td><input class="checkRow" type="checkbox" /></td>
                <td>Bomba de Infusión</td>
                <td>Habitación 12</td>
                <td>Philips</td>
                <td>MX400</td>
                <td>12345ABC</td>
                <td>Alta</td>
                <td>A</td>
                <td>Medio</td>
                <td>2020INV-123</td>
                <td>Activo</td>
                <td><button>Actualizar</button></td>
            </tr>

            <!-- Fila 2 -->
            <tr class="tabla--fila">
                <td><input class="checkRow"type="checkbox" /></td>
                <td>Bomba de Infusión</td>
                <td>Habitación 12</td>
                <td>Mindray</td>
                <td>BEN-800</td>
                <td>98765XYZ</td>
                <td>Media</td>
                <td>B</td>
                <td>Bajo</td>
                <td>2021INV-442</td>
                <td>En Mantenimiento</td>
                <td><button>Actualizar</button></td>
            </tr>
        </tbody>
    </table>
</template>
<style>
    /* --- Tabla general --- */
    .tabla {
        width: 100%;
        border-collapse: collapse;
        font-family: sans-serif;
        font-size: 12px;
    }

    /* --- Encabezado --- */
    .tabla--header {
        background-color: #0a346c; /* azul oscuro elegante */
        color: white;
        text-align: left;
    }

    .tabla--headers,
    .tabla--headersCheck {
        padding: 10px 8px;
        border-bottom: 2px solid #0a2540;
        font-weight: bold;
    }

    /* --- Filas del cuerpo --- */
    .tabla--fila td {
        background-color: white;
        color: #555; 
        padding: 8px 6px;
        border-bottom: 1px solid #e5e5e5;
    }

    /* --- Hover en filas --- */
    .tabla--fila:hover td {
        background-color: #f5f7fa;
    }

    /* --- Checkbox alineado --- */
    .tabla input[type="checkbox"] {
        width: 16px;
        height: 16px;
        cursor: pointer;
    }
</style>