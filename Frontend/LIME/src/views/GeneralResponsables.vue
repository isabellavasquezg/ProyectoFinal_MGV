<script>
import axios from 'axios'; // Asegúrate de importar axios

export default {
    name: "GeneralEquipos",
    data() {
        return {
            // 'filas' ahora contendrá el array AGRUPADO por sede
            filasAgrupadas: [], 
        };
    },
    methods: {
        // Función auxiliar para agrupar los datos
        agruparPorSede(responsables) {
            // Usamos reduce() para transformar la lista plana en un objeto agrupado
            const grupos = responsables.reduce((acc, responsable) => {
                // Asume que la API devuelve 'nombre_sede' (basado en la respuesta anterior)
                const nombreSede = responsable.sede__nombre_sede; 
                
                // Si el grupo no existe, inicialízalo
                if (!acc[nombreSede]) {
                    acc[nombreSede] = {
                        sede: nombreSede,
                        responsables: [] // Array para guardar los responsables de esta sede
                    };
                }
                
                // Agrega el responsable al grupo de la sede
                acc[nombreSede].responsables.push(responsable.nombre_responsable);
                return acc;
            }, {}); // Comienza con un objeto vacío

            // Devuelve un array con los valores del objeto (los grupos de sedes)
            return Object.values(grupos);
        },
        
        async listarEquipos() {
            try {
                const res = await axios.get(`http://127.0.0.1:8000/api/Responsables/`);
                
                // Asume que la lista de responsables viene en res.data.laboratoristas o res.data.result
                const responsables = res.data.result;
                // ¡Agrupa los responsables por sede!
                this.filasAgrupadas = this.agruparPorSede(responsables);
            } catch (err) {
                console.error(err);
                alert("Error al listar equipos");
            }
        },
    },
    mounted() {
        this.listarEquipos();
    },
};
</script>
<template>
<div class="background"> 
    <!-- Barra lateral izquierda -->
    <div class="slidebar"></div>
    <!-- Contenedor principal -->
    <div class="menuPrincipal">
        <!-- Barra superior de navegación -->
        <div class="menuPrincipal--navbar">
            <button class="navbar--opciones" @click="$router.push('/')">Equipos</button>
            <button class="navbar--opciones" @click="$router.push('/Responsables')">Responsables</button>
            <button class="navbar--opciones" @click="$router.push('/Servicios')">Servicios</button>
        </div>
        <div class="menuPrincipal--tablaPrincipal--responsables">
            <div class="tablaprincipal--encabezado">
                <h3 class="encabezado--titulo">RESPONSABLES</h3>
                <div class="contendedor--boton">
                    <button class="encabezado--agregarsede">Agregar Sede</button>
                </div>
            </div>
            <div class="tablaprincipal-contenederolistas">
                <div v-for="grupo in filasAgrupadas" :key="grupo.sede" class="grupo-sede">
                    
                    <h3 class="encabezado-sede">{{ grupo.sede }}</h3>
                    
                    <ul class="contenederolistas--listainfo">
                        <li class="listainfo--titulo">ID</li>
                        <li class="listainfo--titulo">Nombre del Responsable</li>
                        <li class="listainfo--elementos-fila">{{ grupo.responsable}}</li>
                    </ul>

                </div>
            </div>
        </div>
    </div>
</div>
</template>
<style>
    .menuPrincipal--tablaPrincipal--responsables{
        margin: 2% 2%;
        overflow: hidden;
        box-sizing: border-box;
        width: 96%;
        height: 84%;
        background-color: #f7f7f7a1;
        display:flex;
        flex-direction: column;
        align-items: flex-start;
        overflow-x: scroll;
        border-radius: 12px 12px 12px 12px;
        box-shadow: 2px 3px 3px rgba(0, 0, 0, 0.15), -2px -3px 3px rgba(0, 0, 0, 0.15);
    }
    .tablaprincipal--encabezado{
        display:flex;
        flex-direction: row;
        width: 100%;
        height: 10%;
        background-color: #008073;
    }
    .encabezado--titulo{
        background-color: transparent;
        width: 85%;
        height: 100%;
    }
    .encabezado--titulo{
        margin:0;
        display: flex;
        align-items: center;
        padding-left:40%;
        color:#ffffff;
    }
    .contendedor--boton{
        box-sizing: border-box;
        width: 15%;
        height: 100%;
        display:flex;
        align-items: center;
        justify-content: center;
    }
    .encabezado--agregarsede{
        background-color:#008073;
        color:#ffffff;
        width: 70%;
        height: 50%;
        font-size: 12px;
        border:none;
        border-radius: 10px;
        cursor: pointer;

    }
    .encabezado--agregarsede:active{
        transform: scale(0.96);
    }
    .tablaprincipal-contenederolistas{
        width: 100%;
        height: 90%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
    }
    .contenederolistas--listainfo{
        box-sizing: border-box;
        width: 15% ;
        height: 50%;
        margin: 0 20px;
        padding-top: 5%;
        list-style-type: none;
    }
    .listainfo--titulo{
        font-weight: bold;
        border-radius: 7px 7px 0 0;
        color:#ffffff;
        padding: 4% 0;
        background-color: #008073;
        display:flex;
        justify-content: center;
    }
    .subtitulo{
        font-weight: 400;
        background-color: #02aa99;
        border-radius: 0;
    }
    .listainfo--elementos{
        padding: 4% 0;
        padding-left: 20%;
    }
</style>