<script>
import { serviciosService, sedesService } from '../services/api.js';

export default {
    name: "TablaServicios",
    data() {
        return {
            servicios: [],
            sedes: [],
            loading: false,
            error: null,
            selectedServicios: []
        };
    },
    mounted() {
        this.loadData();
    },
    methods: {
        async loadData() {
            this.loading = true;
            this.error = null;
            
            try {
                const [serviciosRes, sedesRes] = await Promise.all([
                    serviciosService.getServicios(),
                    sedesService.getSedes()
                ]);
                
                this.servicios = serviciosRes.data.results || [];
                this.sedes = sedesRes.data.results || [];
            } catch (error) {
                this.error = 'Error al cargar los servicios: ' + error.message;
                console.error('Error loading servicios:', error);
            } finally {
                this.loading = false;
            }
        },
        
        getSedeName(sedeId) {
            const sede = this.sedes.find(s => s.id === sedeId);
            return sede ? sede.nombre : 'No asignada';
        },
        
        toggleServicioSelection(servicioId) {
            const index = this.selectedServicios.indexOf(servicioId);
            if (index > -1) {
                this.selectedServicios.splice(index, 1);
            } else {
                this.selectedServicios.push(servicioId);
            }
        },
        
        selectAllServicios() {
            if (this.selectedServicios.length === this.servicios.length) {
                this.selectedServicios = [];
            } else {
                this.selectedServicios = this.servicios.map(servicio => servicio.id);
            }
        }
    }
};
</script>

<template>
    <div v-if="loading" class="loading-message">
        Cargando servicios...
    </div>
    
    <div v-if="error" class="error-message">
        {{ error }}
    </div>
    
    <table class="tabla" v-if="!loading">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input 
                        id="checkHeaderServicios" 
                        type="checkbox" 
                        @change="selectAllServicios"
                        :checked="selectedServicios.length === servicios.length && servicios.length > 0"
                    />
                </th>
                <th class="tabla--headers">ID</th>
                <th class="tabla--headers">Nombre del Servicio</th>
                <th class="tabla--headers">Sede</th>
                <th class="tabla--headers">Acciones</th>
            </tr>
        </thead>

        <tbody>
            <tr v-if="servicios.length === 0" class="tabla--fila">
                <td colspan="5" style="text-align: center; padding: 20px; color: #666;">
                    No hay servicios registrados. Agregue el primer servicio usando el botón "Agregar".
                </td>
            </tr>
            
            <tr v-for="servicio in servicios" :key="servicio.id" class="tabla--fila">
                <td>
                    <input 
                        class="checkRow" 
                        type="checkbox" 
                        @change="toggleServicioSelection(servicio.id)"
                        :checked="selectedServicios.includes(servicio.id)"
                    />
                </td>
                <td>{{ servicio.id }}</td>
                <td>{{ servicio.nombre }}</td>
                <td>{{ getSedeName(servicio.sede) }}</td>
                <td><button class="btn-actualizar">Actualizar</button></td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
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

.tabla {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
}

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

.tabla--fila td {
    background-color: white;
    color: #555; 
    padding: 8px 6px;
    border-bottom: 1px solid #e5e5e5;
}

.tabla--fila:hover td {
    background-color: #f5f7fa;
}

.tabla input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
}
</style>