<script>
export default {
    name: "FiltroMenu",
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
        placeholderDinamico1() {
            switch (this.seccion) {
                case 'General':
                    return 'Marca';
                case 'Registro':
                    return 'Tiempo vida Util';
                case 'MetrologiaA':
                    return 'Frec. Manteniemiento';
                case 'MetrologiaT':
                    return 'Magnitud';
                case 'Documentacion':
                    return 'Hoja de Vida';
                default:
                    return 'Peso'; // Placeholder por defecto
            }
        },
        placeholderDinamico2() {
            switch (this.seccion) {
                case 'General':
                    return 'Modelo';
                case 'Registro':
                    return 'Fecha Fabricacion';
                case 'MetrologiaA':
                    return 'Frec. Calibración';
                case 'MetrologiaT':
                    return 'Rango Equipo';
                case 'Documentacion':
                    return 'Guia de Usuario';
                default:
                    return 'Voltaje'; // Placeholder por defecto
            }
        },
        placeholderDinamico3() {
            switch (this.seccion) {
                case 'General':
                    return 'Estado';
                case 'Registro':
                    return 'Adquisicion';
                case 'MetrologiaA':
                    return 'calibración';
                case 'MetrologiaT':
                    return 'Rango Trabajo';
                case 'Documentacion':
                    return 'Manual de Operación';
                default:
                    return 'Corriente'; // Placeholder por defecto
            }
        },

    }
};
</script>
<template>
    <form class="tablaPrincipal--formFiltros">
        <input class="filtros--inputs" type="text" placeholder="Sede" />
        <input class="filtros--inputs" type="text" placeholder="Servicio" />
        <input class="filtros--inputs" type="text" placeholder="Numero de Serie" />
        <input class="filtros--inputs" type="text" :placeholder="placeholderDinamico1" />
        <input class="filtros--inputs" type="text" :placeholder="placeholderDinamico2" />
        <input class="filtros--inputs" type="text" :placeholder="placeholderDinamico3" />
        <button class="filtros--boton" type="submit">Filtrar</button>
    </form>
</template>
<style>
    .tablaPrincipal--formFiltros{
        height: 60%;
        width: 80%;
        display:flex;
        flex-direction: row;
        align-items: center;
    }
    .filtros--inputs{
        font-size: 13px;
        margin-right:1%;
        width: 18%;
        border: none;
        border-bottom: 1px solid #cccccc;
    }
    .filtros--inputs:focus{
        outline: none;
        border-bottom: 1px solid #00a89d;
    }
    .filtros--boton{
        border-radius: 5px;
        height: 50%;
        background-color: #00a89d;
        margin-left: 2%;
        color: #ffffff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.1s;
    }
    .filtros--boton:hover{
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .filtros--boton:active{
        transform: scale(0.98);
    }
</style>