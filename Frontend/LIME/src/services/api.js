import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Configurar axios con la URL base
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    }
});

export const equiposService = {
    // Obtener todos los equipos
    getEquipos() {
        return apiClient.get('/equipos/');
    },
    
    // Obtener un equipo por ID
    getEquipo(id) {
        return apiClient.get(`/equipos/${id}/`);
    },
    
    // Crear nuevo equipo
    createEquipo(equipo) {
        return apiClient.post('/equipos/', equipo);
    },
    
    // Actualizar equipo
    updateEquipo(id, equipo) {
        return apiClient.put(`/equipos/${id}/`, equipo);
    },
    
    // Eliminar equipo
    deleteEquipo(id) {
        return apiClient.delete(`/equipos/${id}/`);
    },
    
    // Obtener registro histórico de un equipo
    getHistorico(equipoId) {
        return apiClient.get(`/equipos/${equipoId}/historico/`);
    },
    
    // Obtener documentos de un equipo
    getDocumentos(equipoId) {
        return apiClient.get(`/equipos/${equipoId}/documentos/`);
    },
    
    // Obtener metrología administrativa
    getMetrologiaAdmin(equipoId) {
        return apiClient.get(`/equipos/${equipoId}/metrologia_admin/`);
    },
    
    // Obtener metrología técnica
    getMetrologiaTecnica(equipoId) {
        return apiClient.get(`/equipos/${equipoId}/metrologia_tecnica/`);
    },
    
    // Obtener condiciones de funcionamiento
    getCondiciones(equipoId) {
        return apiClient.get(`/equipos/${equipoId}/condiciones/`);
    }
};

export const sedesService = {
    getSedes() {
        return apiClient.get('/sedes/');
    },
    
    createSede(sede) {
        return apiClient.post('/sedes/', sede);
    }
};

export const serviciosService = {
    getServicios() {
        return apiClient.get('/servicios/');
    },
    
    getServiciosBySede(sedeId) {
        return apiClient.get(`/servicios/?sede=${sedeId}`);
    },
    
    createServicio(servicio) {
        return apiClient.post('/servicios/', servicio);
    }
};

export const responsablesService = {
    getResponsables() {
        return apiClient.get('/responsables/');
    },
    
    createResponsable(responsable) {
        return apiClient.post('/responsables/', responsable);
    }
};

export default {
    equipos: equiposService,
    sedes: sedesService,
    servicios: serviciosService,
    responsables: responsablesService
};