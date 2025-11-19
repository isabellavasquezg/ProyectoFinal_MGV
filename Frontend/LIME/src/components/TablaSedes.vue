<script>
import { sedesService } from '../services/api.js';

export default {
    name: "TablaSedes",
    data() {
        return {
            sedes: [],
            loading: false,
            error: null,
            selectedSedes: []
        };
    },
    mounted() {
        this.loadSedes();
    },
    methods: {
        async loadSedes() {
            this.loading = true;
            this.error = null;
            
            try {
                const response = await sedesService.getSedes();
                this.sedes = response.data.results || [];
            } catch (error) {
                this.error = 'Error al cargar las sedes: ' + error.message;
                console.error('Error loading sedes:', error);
            } finally {
                this.loading = false;
            }
        },
        
        toggleSedeSelection(sedeId) {
            const index = this.selectedSedes.indexOf(sedeId);
            if (index > -1) {
                this.selectedSedes.splice(index, 1);
            } else {
                this.selectedSedes.push(sedeId);
            }
        },
        
        selectAllSedes() {
            if (this.selectedSedes.length === this.sedes.length) {
                this.selectedSedes = [];
            } else {
                this.selectedSedes = this.sedes.map(sede => sede.id);
            }
        }
    }
};
</script>

<template>
    <!-- Mensaje de carga -->
    <div v-if="loading" class="loading-message">
        Cargando sedes...
    </div>
    
    <!-- Mensaje de error -->
    <div v-if="error" class="error-message">
        {{ error }}
    </div>
    
    <!-- Tabla de Sedes -->
    <table class="tabla" v-if="!loading">
        <thead>
            <tr class="tabla--header">
                <th class="tabla--headersCheck">
                    <input 
                        id="checkHeaderSedes" 
                        type="checkbox" 
                        @change="selectAllSedes"
                        :checked="selectedSedes.length === sedes.length && sedes.length > 0"
                    />
                </th>
                <th class="tabla--headers">ID</th>
                <th class="tabla--headers">Nombre de la Sede</th>
                <th class="tabla--headers">Acciones</th>
            </tr>
        </thead>

        <tbody>
            <tr v-if="sedes.length === 0" class="tabla--fila">
                <td colspan="4" style="text-align: center; padding: 20px; color: #666;">
                    No hay sedes registradas. Agregue la primera sede usando el botón "Agregar".
                </td>
            </tr>
            
            <tr v-for="sede in sedes" :key="sede.id" class="tabla--fila">
                <td>
                    <input 
                        class="checkRow" 
                        type="checkbox" 
                        @change="toggleSedeSelection(sede.id)"
                        :checked="selectedSedes.includes(sede.id)"
                    />
                </td>
                <td>{{ sede.id }}</td>
                <td>{{ sede.nombre }}</td>
                <td><button class="btn-actualizar">Actualizar</button></td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
/* Estilos similares a TablasEquipos */
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