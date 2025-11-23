<script>
export default {
    name: "FiltroMenu",

    // ========================
    // PROPIEDADES ENTRANTES
    // ========================
    props: {
        // Recibe la sección actual para determinar los placeholders dinámicos
        seccion: {
            type: String,
            required: true
        }
    },

    // ========================
    // DATOS DEL COMPONENTE
    // ========================
    data() {
        return {
            // Filtros fijos
            filtroSede: '',
            filtroServicio: '',
            filtroNumeroSerie: '',

            // Filtros dinámicos según la sección
            filtroDinamico1: '',
            filtroDinamico2: '',
            filtroDinamico3: '',
        };
    },

    methods: {
        // ========================
        // EMITE AL PADRE TODOS LOS FILTROS
        // ========================
        emitirFiltros() {
            // Construye un objeto con todos los filtros
            const filtros = {
                sede: this.filtroSede,
                servicio: this.filtroServicio,
                numeroSerie: this.filtroNumeroSerie,
                dinamico1: this.filtroDinamico1,
                dinamico2: this.filtroDinamico2,
                dinamico3: this.filtroDinamico3,
            };

            // Emite el evento al padre con los filtros
            this.$emit('aplicar-filtros', filtros);
        }
    },

    // ========================
    // PLACEHOLDERS DINÁMICOS
    // ========================
    computed: {
        placeholderDinamico1() {
            switch (this.seccion) {
                case 'General': return 'Marca';
                case 'Registro': return 'Tiempo vida Util';
                case 'MetrologiaA': return 'Frec. Manteniemiento';
                case 'MetrologiaT': return 'Magnitud';
                case 'Documentacion': return 'Hoja de Vida';
                default: return 'Peso';
            }
        },
        placeholderDinamico2() {
            switch (this.seccion) {
                case 'General': return 'Modelo';
                case 'Registro': return 'Fecha Fabricacion';
                case 'MetrologiaA': return 'Frec. Calibración';
                case 'MetrologiaT': return 'Rango Equipo';
                case 'Documentacion': return 'Guia de Usuario';
                default: return 'Voltaje';
            }
        },
        placeholderDinamico3() {
            switch (this.seccion) {
                case 'General': return 'Estado';
                case 'Registro': return 'Adquisicion';
                case 'MetrologiaA': return 'calibración';
                case 'MetrologiaT': return 'Rango Trabajo';
                case 'Documentacion': return 'Manual de Operación';
                default: return 'Corriente';
            }
        },
    }
};
</script>

<!-- ========================
     PLANTILLA HTML
     ======================== -->
<template>
    <!-- Bloque principal BEM: filtro-menu -->
    <form class="filtro-menu">
        <!-- Elemento: campo de entrada -->
        <input class="filtro-menu__input" type="text"placeholder="Sede"v-model="filtroSede"/>
        <input class="filtro-menu__input" type="text" placeholder="Servicio" v-model="filtroServicio"/>
        <input class="filtro-menu__input" type="text" placeholder="Numero de Serie" v-model="filtroNumeroSerie"/>
        <!-- Inputs con placeholder dinámicos -->
        <input class="filtro-menu__input" type="text" :placeholder="placeholderDinamico1" v-model="filtroDinamico1"/>
        <input class="filtro-menu__input" type="text" :placeholder="placeholderDinamico2" v-model="filtroDinamico2" />
        <input class="filtro-menu__input" type="text" :placeholder="placeholderDinamico3" v-model="filtroDinamico3" />
        <!-- Elemento botón -->
        <button class="filtro-menu__button" type="button" @click="emitirFiltros">Filtrar</button>
    </form>
</template>

<!-- ========================
               ESTILOS 
     ======================== -->
<style>
    /* =========================================
    BLOQUE PRINCIPAL: .filtro-menu
    ========================================= */
    .filtro-menu {
        height: 60%;
        width: 80%;
        display: flex;
        flex-direction: row;
        align-items: center;
        /* Espacio entre campos sin usar margin-right en cada input */
        gap: 1%;
    }

    /* =========================================
    INPUTS DEL BLOQUE: .filtro-menu__input
    ========================================= */
    .filtro-menu__input {
        width: 18%;
        background-color: #f7f7f7a1;
        /* Textos */
        font-size: 13px;
        /* Estilos del borde */
        border: none;
        border-bottom: 1px solid #a2a2a2;
        /* Transición suave */
        transition: border-color 0.2s ease;
    }

    /* Efecto en focus */
    .filtro-menu__input:focus {
        outline: none;
        border-bottom-color: #00a89d;
    }

    /* =========================================
    BOTÓN DEL BLOQUE: .filtro-menu__button
    ========================================= */
    .filtro-menu__button {
        height: 50%;
        background-color: #008073;
        color: #ffffff;

        /* Apariencia */
        border: none;
        border-radius: 5px;

        /* Interacción */
        cursor: pointer;
        padding: 0 12px;

        /* Animación suave */
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    /* Hover */
    .filtro-menu__button:hover {
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transform: scale(1.03);
    }

    /* Click */
    .filtro-menu__button:active {
        transform: scale(0.98);
    }
</style>
