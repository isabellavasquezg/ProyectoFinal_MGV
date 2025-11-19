<script>
import { equiposService, sedesService, serviciosService, responsablesService } from '../services/api.js';

export default {
    name: "TablasEquipos",
    props: {
        seccion: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            equipos: [],
            sedes: [],
            servicios: [],
            responsables: [],
            loading: false,
            error: null,
            selectedEquipos: []
        };
    },
    mounted() {
        this.loadData();
    },
    watch: {
        seccion() {
            this.loadData();
        }
    },
    methods: {
        async loadData() {
            this.loading = true;
            this.error = null;
            
            try {
                const [equiposRes, sedesRes, serviciosRes, responsablesRes] = await Promise.all([
                    equiposService.getEquipos(),
                    sedesService.getSedes(),
                    serviciosService.getServicios(),
                    responsablesService.getResponsables()
                ]);
                
                this.equipos = equiposRes.data.results || [];
                this.sedes = sedesRes.data.results || [];
                this.servicios = serviciosRes.data.results || [];
                this.responsables = responsablesRes.data.results || [];
                
            } catch (error) {
                this.error = 'Error al cargar los datos: ' + error.message;
                console.error('Error loading data:', error);
            } finally {
                this.loading = false;
            }
        },
        
        toggleEquipoSelection(equipoId) {
            const index = this.selectedEquipos.indexOf(equipoId);
            if (index > -1) {
                this.selectedEquipos.splice(index, 1);
            } else {
                this.selectedEquipos.push(equipoId);
            }
        },
        
        selectAllEquipos() {
            if (this.selectedEquipos.length === this.equipos.length) {
                this.selectedEquipos = [];
            } else {
                this.selectedEquipos = this.equipos.map(equipo => equipo.id);
            }
        },
        
        getSedeName(sedeId) {
            const sede = this.sedes.find(s => s.id === sedeId);
            return sede ? sede.nombre : 'No asignada';
        },
        
        getServicioName(servicioId) {
            const servicio = this.servicios.find(s => s.id === servicioId);
            return servicio ? servicio.nombre : 'No asignado';
        },
        
        getResponsableName(responsableId) {
            const responsable = this.responsables.find(r => r.id === responsableId);
            return responsable ? responsable.nombre : 'No asignado';
        }
    },
    computed: {
        fontSizeDinamico() {
            switch (this.seccion) {
                case "General":
                    return "12px";
                case "Registro":
                    return "14px";
                case "MetrologiaA":
                    return "13px";
                case "MetrologiaT":
                    return "15px";
                case "Documentacion":
                    return "11px";
                default:
                    return "12px";
            }
        }
    }
};
</script>

<template> 
    <!-- Mensaje de carga -->
    <div v-if="loading" class="loading-message">
        Cargando datos...
    </div>
    
    <!-- Mensaje de error -->
    <div v-if="error" class="error-message">
        {{ error }}
    </div>
    
    <!-- Tabla General -->
    <table class="tabla" v-if="seccion=='General' && !loading" :style="{ fontSize: fontSizeDinamico }">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input 
                        id="checkHeader" 
                        type="checkbox" 
                        @change="selectAllEquipos"
                        :checked="selectedEquipos.length === equipos.length && equipos.length > 0"
                    />
                </th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Servicio</th>
                <th class="tabla--headers">Nombre Equipo</th>
                <th class="tabla--headers">Código Inventario</th>
                <th class="tabla--headers">Código IPS</th>
                <th class="tabla--headers">Código ECRI</th>
                <th class="tabla--headers">Responsable</th>
                <th class="tabla--headers">Ubicación</th>
                <th class="tabla--headers">Marca</th>
                <th class="tabla--headers">Modelo</th>
                <th class="tabla--headers">Serie</th>
                <th class="tabla--headers">Estado</th>
                <th class="tabla--headers">Acciones</th>
            </tr> 
        </thead>

        <tbody>
            <tr v-if="equipos.length === 0" class="tabla--fila">
                <td colspan="14" style="text-align: center; padding: 20px; color: #666;">
                    No hay equipos registrados. Agregue el primer equipo usando el botón "Agregar".
                </td>
            </tr>
            
            <tr v-for="equipo in equipos" :key="equipo.id" class="tabla--fila">
                <td>
                    <input 
                        class="checkRow" 
                        type="checkbox" 
                        @change="toggleEquipoSelection(equipo.id)"
                        :checked="selectedEquipos.includes(equipo.id)"
                    />
                </td>
                <td>{{ getSedeName(equipo.sede) }}</td>
                <td>{{ getServicioName(equipo.servicio) }}</td>
                <td>{{ equipo.nombre_equipo }}</td>
                <td>{{ equipo.codigo_inventario }}</td>
                <td>{{ equipo.codigo_ips || 'N/A' }}</td>
                <td>{{ equipo.codigo_ecri || 'N/A' }}</td>
                <td>{{ getResponsableName(equipo.responsable) }}</td>
                <td>{{ equipo.ubicacion_fisica }}</td>
                <td>{{ equipo.marca }}</td>
                <td>{{ equipo.modelo }}</td>
                <td>{{ equipo.serie }}</td>
                <td>
                    <span :class="{'estado-activo': equipo.estado === 'activo', 'estado-inactivo': equipo.estado !== 'activo'}">
                        {{ equipo.estado }}
                    </span>
                </td>
                <td><button class="btn-actualizar">Actualizar</button></td>
            </tr>
        </tbody>
    </table> 
    
    <!-- Otras tablas mantienen la estructura similar pero con datos reales -->
    <!-- Por ahora mostramos mensaje para otras secciones -->
    <div v-if="seccion !== 'General' && !loading" class="seccion-pendiente">
        <h3>Sección: {{ seccion }}</h3>
        <p>Esta vista se conectará con los datos específicos de {{ seccion.toLowerCase() }}.</p>
        <p>Total de equipos disponibles: {{ equipos.length }}</p>
    </div>
</template>

<style>
.loading-message {
    text-align: center;
    padding: 40px;
    font-size: 16px;
    color: #666;
}

.error-message {
    text-align: center;
    padding: 20px;
    color: #d32f2f;
    background-color: #ffebee;
    border: 1px solid #ffcdd2;
    border-radius: 4px;
    margin: 20px;
}

.estado-activo {
    color: #2e7d32;
    font-weight: bold;
}

.estado-inactivo {
    color: #d32f2f;
    font-weight: bold;
}

.btn-actualizar {
    background-color: #00a89d;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
}

.btn-actualizar:hover {
    background-color: #008a7f;
}

.seccion-pendiente {
    padding: 40px;
    text-align: center;
    color: #666;
}

.seccion-pendiente h3 {
    color: #00a89d;
    margin-bottom: 10px;
}

/* Tabla general */
.tabla {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
}

/* Encabezado */
.tabla--header {
    background-color: #0a346c;
    color: white;
    text-align: left;
}

.tabla--headers,
.tabla--headersCheck {
    padding: 10px 8px;
    border-bottom: 2px solid #0a2540;
    font-weight: bold;
}

/* Filas del cuerpo */
.tabla--fila td {
    background-color: white;
    color: #555; 
    padding: 8px 6px;
    border-bottom: 1px solid #e5e5e5;
}

/* Hover en filas */
.tabla--fila:hover td {
    background-color: #f5f7fa;
}

/* Checkbox alineado */
.tabla input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
}
</style>